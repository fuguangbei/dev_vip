# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from moments.models import *
import vip.utils as utils
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from moments.forms import *
from notifications.notifications import *

@csrf_exempt
@require_POST
@login_required
def publish_post(request):
	params = request.POST
	files = request.FILES
	user = request.user
	content = params.get('text')

	if content is None or not len(content):
		return HttpResponseBadRequest("请填写正确参数")
	if len(content) > Post._meta.get_field('text').max_length :
		return HttpResponseBadRequest("圈子内容长度超过限制")
	if utils.contains_sensitive(content):
		return HttpResponseBadRequest('圈子评论包含敏感词')

	try:
		new_post = Post()
		new_post.text = content
		new_post.publisher = user
		new_post.author = user
		if 'banner' in params:
			return HttpResponseBadRequest("banner传值类型错误, 请选择正确文件类型")
		if 'banner' in files:
			form = MomentsBannerForm(params, files)
			if not form.is_valid():
				return HttpResponseBadRequest("上传图片损坏或格式错误, 添加失败")
			new_post.banner = form.cleaned_data['banner']
		new_post.save()
	except ValueError:
		return HttpResponseBadRequest("圈子参数传值有错,提交圈子失败")
	return HttpResponse("发表圈子成功")


@login_required
@require_POST
@csrf_exempt
def forward_post(request, id):
	current_user = request.user
	caption = request.POST.get('caption') or ""
	# print "[API] user {0} is forwarding post {1}".format(current_user, id)
	if len(caption) > Post._meta.get_field('forward_notes').max_length :
		return HttpResponseBadRequest("圈子转发内容长度超过限制")
	if utils.contains_sensitive(caption):
		return HttpResponseBadRequest('圈子转发内容包含敏感词')

	try:
		forwarding_moment = Post.objects.get(pk=id)
		if current_user == forwarding_moment.author:
			return HttpResponseBadRequest("不能转发自己发表的圈子,转发失败")
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到圈子{0}, 转发失败".format(id))
	new_moment = Post()
	for i in forwarding_moment._meta.fields:
		key = i.name
		if key in ['id', 'date']:
			continue
		value = getattr(forwarding_moment, key)
		setattr(new_moment, key, value)
	new_moment.publisher = current_user
	new_moment.forward_notes = caption
	new_moment.save()
	return HttpResponse('成功转发圈子{0}'.format(id))


@require_GET
def get_posts(request):
	'''
	分页获取圈子内容
	:param request:
	:return: 200 圈子列表
	404 找不到对应页面的数据, 超出范围
	400 page参数上传有误
	'''
	page_number = request.GET.get('p')
	target = request.GET.get('self')
	current_user = request.user

	if target in ['false', "f", "F", "False", None]:
		target = False
	else:
		target = True
	if not target:
		from vip.switches import MOMENTS_VERIFICATION
		if MOMENTS_VERIFICATION:
			posts = Post.objects.filter(display=True).order_by('-date')
		else:
			posts = Post.objects.all().order_by('-date')
	else:
		if not current_user.is_authenticated():
			return HttpResponseForbidden("对不起, 您还未登录")
		posts = Post.objects.filter(publisher=request.user).order_by('-date')

	json_list = []

	for post in posts:
		post_detail = post.to_json()
		decorated_time = utils.parse_time(post.date)
		post_detail['date'] = decorated_time
		if current_user.is_authenticated():
			post_liked = True if post in current_user.usermoments.moments_likes.all() else False
			belong_to_current_user = True if post.publisher == current_user else False
			is_original = True if post.author == current_user else False
			post_detail['liked'] = post_liked
			post_detail['belong_to_current_user'] = belong_to_current_user
			post_detail['is_original'] = is_original
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
def get_post(request, id):
	try:
		model_post = Post.objects.get(pk=id)
		post_detail = model_post.to_json()
		users = User.objects.exclude(is_superuser=True)
		liked_count = 0
		for user in users:
			utils.update_user(user)
			if model_post in user.usermoments.moments_likes.all():
				liked_count += 1
			else:
				liked_count += 0
		if request.user.is_authenticated():
			current_user = request.user
			post_liked = True if model_post in current_user.usermoments.moments_likes.all() else False
			belong_to_current_user = True if model_post.publisher == current_user else False
			is_original = True if model_post.author == current_user else False
			post_detail['liked'] = post_liked
			post_detail['liked_count'] = liked_count
			post_detail['belong_to_current_user'] = belong_to_current_user
			post_detail['is_original'] = is_original
		decorated_time = utils.parse_time(model_post.date)
		post_detail['date'] = decorated_time
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到圈子{0}".format(id))
	return JsonResponse(post_detail, safe=False)


@require_GET
def get_comments(request, id):
	comments = MomentsComments.objects.filter(corresponding_post_id = id).order_by('-publish_time')
	json_list = []
	for comment in comments:
		comment_detail = comment.to_json()
		decorated_time = utils.parse_time(comment.publish_time)
		comment_detail['date'] = decorated_time
		json_list.append(comment_detail)
	return JsonResponse({
		'count': comments.count(),
		'data': json_list
	})

#not in usage
@require_GET
@login_required
def get_current_user_moments(request):
	'''
	分页获取但前用户的圈子内容
	:param request:
	:return: 200 圈子列表
	404 找不到对应页面的数据, 超出范围
	400 page参数上传有误
	'''
	page_number = request.GET.get('p')
	current_user = request.user
	belong_current_user = True
	my_post = Post.objects.filter(publisher=current_user).order_by('-date')
	for i in my_post:
		if i.publisher == current_user:
			belong_current_user &= True
		else:
			belong_current_user &= False
	# my_post = Post.objects.filter(corresponding_user=current_user).order_by('-date')
	if page_number is None:
		# json = [i.to_json() for i in my_post]
		json = []
		for post in my_post:
			post_liked = True if post in current_user.usermoments.moments_likes.all() else False
			post_detail = post.to_json()
			post_detail['liked'] = post_liked
			json.append(post_detail)
		return JsonResponse(json, safe=False)
	else:
		try:
			page_number = int(page_number)
		except:
			return HttpResponseBadRequest("参数不正确")
		pages = Paginator(my_post, 5)
		if page_number not in pages.page_range:
			return HttpResponseNotFound("页码超出范围")
		page = pages.page(page_number)
		model_list = page.object_list
		json_list = []

		for post in model_list:
			post_liked = True if post in current_user.usermoments.moments_likes.all() else False
			post_detail = post.to_json()
			post_detail['liked'] = post_liked
			json_list.append(post_detail)

		return JsonResponse({
			'list': json_list,
			'has_next': page.has_next(),
			'belong_current_user': belong_current_user
		}, safe=False)


@login_required
def like_post(request, id):
	try:
		post = Post.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到圈子{0}".format(id))

	utils.update_user(request.user)
	response_message = request.user.usermoments.toggle_like_moments(post)
	liked = post in request.user.usermoments.moments_likes.all()
	if liked:
		baidu_push(recipient=post.publisher, action='MomentsToggle', params={
			'post': post,
			'liked': liked,
			'trigger_user': request.user
		})
	return HttpResponse(response_message)

@csrf_exempt
@require_POST
@login_required
def comment_post(request, id):
	comment = request.POST.get('text')
	if comment is None:
		return HttpResponseBadRequest("请填写正确评论")
	if len(comment) > MomentsComments._meta.get_field('content').max_length:
		return HttpResponseBadRequest('圈子评论长度超过限制')
	if utils.contains_sensitive(comment):
		return HttpResponseBadRequest('圈子评论包含敏感词')

	try:
		post = Post.objects.get(pk=id)
		user = request.user
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到对应圈子")

	try:
		new_comment = MomentsComments()
		new_comment.content = comment
		new_comment.corresponding_post = post
		new_comment.corresponding_user = user
		new_comment.save()
		baidu_push(recipient=post.publisher, action='Comment',params={
			'moments_comment': new_comment,
			'trigger_user': request.user
		})
		return HttpResponse("评论成功")

	except ValueError:
		return HttpResponseBadRequest("评论参数传值有错,提交评论失败")

@require_GET
@login_required
def delete_post(request, id):
	try:
		post = Post.objects.get(pk=id)
		current_user = request.user
		if post in Post.objects.filter(publisher=current_user):
			post.delete()
		else:
			return HttpResponseForbidden("该条圈子不是当前登录用户所发布, 不能删除")
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到圈子{0}".format(id))
	return HttpResponse("删除圈子{0}成功".format(id))