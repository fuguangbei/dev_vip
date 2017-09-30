# coding=utf-8
from django.views.decorators.http import require_GET,require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from notifications.models import *
from django.contrib.auth.decorators import login_required
from notifications.notifications import *

@csrf_exempt
@require_POST
@login_required
def get_device_param(request):
    userid = request.POST.get('user_id')
    channel_id = request.POST.get('channel_id')
    device_type = request.POST.get('device_type')
    # channel_id = request.channel_id
    # userid = request.user_id
    # device_type = request.device_type
    if len(userid) < 1:
        return HttpResponseBadRequest('user_id is not valid.')
    if len(channel_id) <1:
        return HttpResponseBadRequest('channel_id is not valid.')
    if device_type not in (u'3', u'4'):
        return HttpResponseBadRequest('device_type is not valid.')
    else:
        utils.update_user(request.user)
        request.user.usernotifications.update_device_param(channel_id, userid, device_type)
        return HttpResponse('get device param ( channel_id / user_id / device_type )successfully.')

@require_GET
@login_required
def get_notifications(request):
    '''
    分页获取消息中心列表
    :param request:
    :return: 200 消息中心列表
    404 找不到对应页面的数据, 超出范围
    400 page参数上传有误
    '''
    page_number = request.GET.get('p')
    target_user = request.user
    notifications = Notification.objects.filter(target_user=target_user).order_by('-id')
    json_list = []
    for notification in notifications:
        notification_detail = notification.to_json()
        decorated_time = utils.parse_time(notification.time)
        push_to_self = True if notification.target_user == notification.triggering_user else False
        notification_detail['date'] = decorated_time
        notification_detail['push_to_self'] = push_to_self
        json_list.append(notification_detail)

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
        'data': json_list,
        'has_next': has_next
    }, safe=False)

@login_required
def read_notification(request, id):
    current_user = request.user
    try:
        notification = Notification.objects.get(pk=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("找不到消息通知{0}".format(id))
    my_notifications = Notification.objects.filter(target_user=current_user)
    if notification not in my_notifications:
        return HttpResponseBadRequest("此条消息不属于当前用户")
    else:
        utils.update_user(request.user)
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return HttpResponse("已读通知消息{0}".format(id))

@login_required
def read_notifications(request):
    notification = None
    list = []
    current_user = request.user
    point_notification = Notification.objects.filter(target_user=current_user, action__in=['Like', 'Dislike', 'Favorite', 'Unfavorite'])
    print point_notification.count()
    my_notifications = Notification.objects.filter(target_user=current_user)
    utils.update_user(request.user)
    for notification in point_notification:
        if notification not in my_notifications:
            return HttpResponseBadRequest('消息{0}不属于当前用户'.format(str(notification.pk)))
        elif not notification.is_read:
            list.append(notification.pk)
            notification.is_read = True
            notification.save()
    return HttpResponse('消息"{0}"置为已读'.format(list))


@login_required
def get_unread_count(request):
    current_user = request.user
    count = Notification.objects.filter(target_user=current_user, is_read=False).count()
    return JsonResponse({
        'unread_count': count
    }, safe=False)


@login_required
def delete_device_param(request):
    request.user.usernotifications.update_device_param('','','')
    return HttpResponse('成功删除用户推送设备信息')


# @csrf_exempt
# @require_POST
# @login_required
# def send_share_notification(request, shared_type, shared_id):
#     # shared_type = request.POST.get('shared_type')
#     # shared_id = request.POST.get('shared_id')
#     user = request.user
#     if shared_type is None:
#         return HttpResponseBadRequest('shared_type is not valid.')
#     elif shared_id is None:
#         return HttpResponseBadRequest('shared_id is not valid.')
#     else:
#         apiKey, secretKey, userid, channel_id, device_type, deploy_status = get_current_device_param_1(user_id=user.id)
#         ret = push_share(apiKey, secretKey, userid, channel_id, device_type, deploy_status, user.id, shared_type, shared_id)
#         if ret:
#             return HttpResponse('get shared param ( shared_type / shared_id ) and send notification successfully.')
#         else:
#             return HttpResponseBadRequest('参数不正确,推送分享类消息失败')