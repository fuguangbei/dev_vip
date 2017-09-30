#coding:utf-8
from django.shortcuts import render
import sys
import os
import time
# sys.path.append("/Users/monst/projects/vip_ticketing/vip_ticketing_server/notifications/pythonsdk3_0")
from Channel import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from models import *
from moments.models import Post as MomentsPost
from explore.models import Post as ExplorePost
from merchandise.models import *
from PIL import Image
import vip.utils as utils
from vip.switches import ENABLE_PUSH
from threading import Thread
from django.contrib.staticfiles.templatetags.staticfiles import static

API_KEY_IOS = u"ymKdxPquXLurXqjfKbOT5hGL"
SECRET_KEY_IOS = u"0gf2WG4PUwmX8H3Sn8Yd7O8IXKxcSd1H"

API_KEY_ANDROID = u"az2xsngwymeWkKXgrR6CpdGM"
SECRET_KEY_ANDROID = u"6FloCZ6FrfzXrnaVmGMrAqL3V962qZUs"

DISNEY_TYPE = 'disney'
CONCERT_TYPE = 'concert'
AEROSPACE_TYPE = 'aerospace'
SCENERY_TYPE = 'scenery'
EXPLORE_TYPE = 'explore'
AGENT_TYPE = 'agent'
MOMENTS_TYPE = 'moments'

COMMENT_TYPE = 'Comment'
REGISTER_TYPE = 'Register'
LIKE_TYPE = 'Like'
DISLIKE_TYPE = 'Dislike'
APPROVED_TYPE = 'Approved'
DISAPPROVED_TYPE = 'Disapproved'
FAVORITE_TYPE = 'Favorite'
UNFAVORITE_TYPE = 'Unfavorite'

opts_android = {'msg_type':1, 'expires':300}
opts_ios = {'msg_type':1, 'expires':300, 'deploy_status':2}


def _get_device_params(user):
	utils.update_user(user)
	if user.usernotifications is not None:
		user_id_baidu = user.usernotifications.user_id_baidu
		channel_id = user.usernotifications.channel_id
		device_type = user.usernotifications.device_type
		return {
			"user_id_baidu": user_id_baidu,
			"channel_id": channel_id,
			"device_type": device_type,
		}
	else:
		return False


def _push_comment(recipient, trigger_user, moments_comment, *args, **kwargs):
	# print args
	# print kwargs
	msg = u"{somebody}评论了{content}".format(
		somebody=trigger_user.profile.to_json()['nickname'],
		content=moments_comment.content
	)

	# TODO: save something into db
	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=COMMENT_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = moments_comment.corresponding_post.banner
	new_notification.content = moments_comment.content
	new_notification.target_user = recipient
	new_notification.content_id = moments_comment.corresponding_post.pk
	new_notification.content_type = MOMENTS_TYPE
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def _push_register(recipient, trigger_user, promo, *args, **kwargs):
	utils.update_user(trigger_user)
	msg = u'{somebody}注册成功'.format(
		somebody=trigger_user.profile.to_json()['nickname']
	)

	# TODO: save something into db
	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=REGISTER_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = static('assets/i/invite.jpg')
	new_notification.content = u'通过您的邀请码"{promo}"注册'.format(promo=promo[0].code)
	new_notification.target_user = recipient
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def _push_ticket_toggle(recipient, trigger_user, ticket, liked, *args, **kwargs):
	# ticket_type = Ticket.find_type_by_id(ticket.pk)
	msg = u"{somebody}{action}收藏了{title}".format(
		somebody=trigger_user.profile.to_json()['nickname'],
		action=u"" if liked else u"取消",
		title=ticket.name
	)

	# TODO: save something into db

	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=LIKE_TYPE if liked else DISLIKE_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = ticket.detail_cover
	new_notification.content = ticket.name
	new_notification.target_user = recipient
	new_notification.content_id = ticket.pk
	new_notification.content_type = Ticket.find_type_by_id(ticket.pk)
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def _push_explore_toggle(recipient, trigger_user, post, liked, *args, **kwargs):
	msg = u"{somebody}{action}收藏了{title}".format(
		somebody=trigger_user.profile.to_json()['nickname'],
		action=u"" if liked else u"取消",
		title=post.title
	)

	# TODO: save something into db

	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=LIKE_TYPE if liked else DISLIKE_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = post.banner
	new_notification.content = post.title
	new_notification.target_user = recipient
	new_notification.content_id = post.pk
	new_notification.content_type = EXPLORE_TYPE
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def _push_agent_application(recipient, trigger_user, approved, *args, **kwargs):
	msg = u"尊敬的{somebody}: 管理员{action}了您的代理申请.".format(
		somebody=recipient.profile.get_nickname(),
		action=u"通过" if approved else u"拒绝",
	)

	# TODO: save something into db

	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=APPROVED_TYPE if approved else DISAPPROVED_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = static('assets/i/approved.png') if approved else static('assets/i/disapproved.png')
	new_notification.content = u'申请成为代理{action}'.format(action=u'成功' if approved else u'失败')
	new_notification.target_user = recipient
	new_notification.content_type = AGENT_TYPE
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def _push_moments_toggle(recipient, trigger_user, post, liked, *args, **kwargs):
	msg = u"{somebody}{action}点赞了{text}".format(
		somebody=trigger_user.profile.to_json()['nickname'],
		action=u"" if liked else u"取消",
		text=post.forward_notes if post.forward_notes else post.text
	)

	# TODO: save something into db

	# save_notification(triggering_user, banner, title, target_user, liked_type, action)
	new_notification = Notification(action=FAVORITE_TYPE if liked else UNFAVORITE_TYPE)
	new_notification.triggering_user = trigger_user
	new_notification.banner = post.banner
	new_notification.content = post.forward_notes if post.forward_notes else post.text
	new_notification.target_user = recipient
	new_notification.content_id = post.pk
	new_notification.content_type = MOMENTS_TYPE
	new_notification.save()

	device_info = _get_device_params(recipient)
	if not device_info:
		return False

	notifications = Notification.objects.filter(target_user=recipient)
	badge = notifications.filter(is_read=False).count()
	return push_message(message=msg, badge=badge, **device_info)


def push_message(user_id_baidu, channel_id, device_type, message, badge):
	# TODO: get the number of unread messages
	api_key = None
	secret_key = None
	message_params = {}

	if device_type == u'3': #Android
		api_key = API_KEY_ANDROID
		secret_key = SECRET_KEY_ANDROID
		message_params = {
			"title": "来自 尊享VIP 的消息",
			"description": message
		}
	if device_type == u'4': #iOS
		api_key = API_KEY_IOS
		secret_key = SECRET_KEY_IOS
		message_params = {
			"aps": {
				"content-available": 1,
				"badge": badge,
				"sound": "",
				"alert": message
			}
		}
	optional = {
		Channel.USER_ID: user_id_baidu,
		Channel.CHANNEL_ID: channel_id,
		Channel.PUSH_TYPE: 1,  #
		Channel.MESSAGE_TYPE: 1,  # 0: penNAMEetration 1: notification
		Channel.DEPLOY_STATUS: 2,  # production or development
	}
	channel = Channel(api_key, secret_key)
	try:
		ret = channel.pushMessage(1, json.dumps(message_params), 'key1', optional)
		print "ret",ret
		return True
	except KeyError, k:
		print '\nbaidu_push error No. is', str(k)
		return False
	# print json.dumps(ret)


dispatcher = {
	"Comment": _push_comment,
	"Register": _push_register,
	"TicketToggle": _push_ticket_toggle,
	"ExploreToggle": _push_explore_toggle,
	"AgentApplication": _push_agent_application,
	"MomentsToggle": _push_moments_toggle
}

def separate(function):
	def decorator(*args, **kwargs):
		t = Thread(target=function, args=args, kwargs=kwargs)
		t.daemon = True
		t.start()
		return True

@utils.async
def baidu_push(recipient, action, params, *args, **kwargs):
	if not ENABLE_PUSH:
		return False

	dispatcher[action](recipient, **params)