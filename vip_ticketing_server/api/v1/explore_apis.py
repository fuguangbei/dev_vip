# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from explore.models import *
import vip.utils as utils
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from notifications.notifications import *


@require_GET
def get_posts(request):
    '''
	分页获取发现内容
	:param request:
	:return: 200 发现列表
	404 找不到对应页面的数据, 超出范围
	400 page参数上传有误
	'''
    page_number = request.GET.get('p')
    posts = Post.objects.all().order_by('-date')
    json_list = []
    for post in posts:
        post_detail = post.to_json()
        decorated_time = utils.parse_time(post.date)
        post_detail['date'] = decorated_time
        json_list.append(post_detail)
    if page_number is None:
        return JsonResponse(json_list, safe=False)
    else:
        try:
            page_number = int(page_number)
        except:
            return HttpResponseBadRequest("参数不正确")

        json_list, has_next = utils.paginate(json_list, page_number)
        if json_list is False:
            return HttpResponseNotFound("页码超出范围")

        return JsonResponse({
            'list': json_list,
            'has_next': has_next
        }, safe=False)


@require_GET
def get_highlights(request):
    model_list = Highlight.objects.filter(display=True)
    json_list = [i.to_json() for i in model_list]
    return JsonResponse(json_list[0:5], safe=False)


@require_GET
def get_post(request, id):
    try:
        model_post = Post.objects.get(pk=id)
        post_detail = model_post.to_json()
        decorated_time = utils.parse_time(model_post.date)
        post_detail['date'] = decorated_time
        if request.user.is_authenticated():
            current_user = request.user.userexplore
            post_liked = True if model_post in current_user.explore_likes.all() else False
            post_detail['liked'] = post_liked
    except ObjectDoesNotExist:
        return HttpResponseNotFound("找不到发现{0}".format(id))
    return JsonResponse(post_detail, safe=False)


@require_GET
def get_comments(request, id):
    comments = ExploreComments.objects.filter(corresponding_post_id=id).order_by('-publish_time')
    json_list = []
    for comment in comments:
        comment_detail = comment.to_json()
        decorated_time = utils.parse_time(comment.publish_time)
        comment_detail['date'] = decorated_time
        json_list.append(comment_detail)

    return JsonResponse({
        'count': comments.count(),
        'data': json_list,
    })
# def get_comments(request, id):
#     '''
# 	分页获取发现评论
# 	:param request:
# 	:return: 200 发现评论列表
# 	404 找不到对应页面的数据,超出范围
# 	400 page参数上传有误
# 	'''
#     page_number = request.GET.get('p')
#     if page_number is None:
#         page_number = 1
#     else:
#         try:
#             page_number = int(page_number)
#         except:
#             return HttpResponseBadRequest("参数不正确")
#     try:
#         model_comments = ExploreComments.objects.filter(corresponding_post_id=id)
#     except ObjectDoesNotExist:
#         return HttpResponseNotFound("找不到评论{0}".format(id))
#     pages = Paginator(model_comments.order_by('-publish_time'), 10)
#     if page_number not in pages.page_range:
#         return HttpResponseNotFound("页码超出范围")
#     page = pages.page(page_number)
#     model_list = page.object_list
#     json_list = [i.to_json() for i in model_list]
#
#     return JsonResponse({
#         'list': json_list,
#         'has_next': page.has_next(),
#         'count': model_comments.count()
#     }, safe=False)
    #return JsonResponse(comments, safe=False)


@csrf_exempt
@require_POST
@login_required
def comment_post(request, id):
    comment = request.POST.get('text')
    if comment is None:
        return HttpResponseBadRequest("请正确填写评论")
    if utils.contains_sensitive(comment):
        return HttpResponseBadRequest('评论中包含敏感词')
    if len(comment) > ExploreComments._meta.get_field('content').max_length:
        return HttpResponseBadRequest('发现评论长度超过限制')
    # if words_filter(comment):
    #     return words_filter(comment)
    try:
        post = Post.objects.get(pk=id)
        user = request.user
    except ObjectDoesNotExist:
        return HttpResponseNotFound("找不到对应发现")

    try:
        new_comment = ExploreComments()
        new_comment.content = comment
        new_comment.corresponding_post = post
        new_comment.corresponding_user = user
        new_comment.save()
    except ValueError:
        return HttpResponseBadRequest("评论参数传值有错,提交评论失败")
    return HttpResponse("添加评论成功")


@login_required
def get_liked_post(request):
    user = request.user.userexplore
    liked_explore = user.explore_likes.all().order_by('-date')
    likes = []
    for explore in liked_explore:
        explore_detail = explore.to_json()
        decorated_time = utils.parse_time(explore.date)
        explore_detail['date'] = decorated_time
        likes.append(explore_detail)
    return JsonResponse(likes, safe=False)


@csrf_exempt
@login_required
def like_post(request, id):
    liked_type = 'explore'
    try:
        post = Post.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("找不到发现{0}".format(id))

    utils.update_user(request.user)
    liked = request.user.userexplore.toggle_like_explore(post)
    if liked:
        baidu_push(recipient=request.user, action='ExploreToggle', params={
            'post': post,
            'liked': liked,
            'trigger_user': request.user
        })
    return HttpResponse('{0}收藏成功'.format("" if liked else "取消"))


# def create_word_tree(words_list):
#     wordTree = [None for i in range(0,256)]
#     wordTree = [wordTree, 0]
#     for word in words_list:
#         tree = wordTree[0]
#         for i in range(0, len(word)):
#             little = word[i]
#             index = ord(little)
#             if i == len(word) - 1:
#                 tree[index] = 1
#             else:
#                 tree[index] = [[None for x in range(0, 256)], 1]
#                 tree = tree[index][0]
#     return wordTree
#
#
# def translate(string, tree):
#     temp = tree
#     result = ''
#     for little in string:
#         index = ord(little)
#         temp = temp[0][index]
#         if temp == None:
#             temp = tree
#         else:
#             result += chr(index)
#         if temp == 1:
#             return string.replace(result, '*')
#
# def words_filter(comment):
#     fileP = open('/Users/monst/projects/vip_ticketing/vip_ticketing_server/vip/words.txt')
#     words = fileP.read()
#     tree = create_word_tree(comment)
#     clean_words = translate(words, tree)
#     return clean_words

# class Node(object):
#     def __init__(self):
#         self.children = None
#
# def add_word(root,word):
#     node = root
#     for i in range(len(word)):
#         if node.children == None:
#             node.children = {}
#             node.children[word[i]] = Node()
#         elif word[i] not in node.children:
#             node.children[word[i]] = Node()
#         node = node.children[word[i]]
#
# def init(path):
#     root = Node()
#     fp = open(path,'r')
#     for line in fp:
#         line = line[0:-1]
#         add_word(root,line)
#     fp.close()
#     return root
#
# def is_contain(message, root):
#     for i in range(len(message)):
#         p = root
#         j = i
#         while (j<len(message) and p.children!=None and message[j] in p.children):
#             p = p.children[message[j]]
#             j = j + 1
#         if p.children == None:
#             return True
#     return False
#
# def dfa():
#     root = init('/User/monst/projects/vip_ticketing/vip_ticketing_server/vip/words.txt')
#     message = '不顾'
#     start_time = timezone.now()
#     for i in range(1000):
#         res = is_contain(message,root)
#     end_time = timezone.now()
#     print (end_time - start_time)
#
# def is_contained(message,word_list):
#     for item in word_list:
#         if message.find(item)!=-1:
#             return True
#     return False
#
# def normal():
#     path = '/User/monst/projects/vip_ticketing/vip_ticketing_server/vip/words.txt'
#     fp = open(path,'r')
#     word_list = []
#     message = '不顾'
#     for line in fp:
#         line = line[0:-1]
#         word_list.append(line)
#     fp.close()
#     start_time = timezone.now()
#     for i in range(1000):
#         res = is_contained(message, word_list)
#     end_time = timezone.now()
#     print (end_time - start_time)