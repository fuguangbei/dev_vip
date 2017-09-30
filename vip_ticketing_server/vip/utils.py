# -*- coding: utf-8 -*-
import StringIO
import os
import random
import string
import urllib
import vip.switches as switches

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
import pytz
from threading import Thread
import time
from cms.models import *

import registrar.models

import vip.settings as settings
import datetime
from registrar.easemob_server_python import register_new_user,AppClientAuth
org_name, app_name = "shanghaicayman", "kmltvip"
client_id = "YXA6nYgHIG9gEealp3GehiWjKw"
client_secret = "YXA6-GId8cIlbV5ZKFw0FUSQR5HZle0"


def queryset_to_json(queryset):
	if len(queryset) == 0:
		return None
	if len(queryset) == 1:
		return queryset[0].to_json()
	json_list = []
	for i in queryset:
		json_list.append(i.to_json())
	return json_list


def print_pretty_dict(dict_obj):
	import json, datetime
	def default(o):
		if type(o) is datetime.date or type(o) is datetime.datetime:
			return o.isoformat()
	formatted = json.dumps(dict_obj, indent=4, default=default)
	print formatted
	return formatted


def valid_phone_number(number):
	if len(number) != 11:
		return False
	
	return True


def send_SMS(recipient, message):
	if not switches.ENABLE_SMS:
		return True
	# send_SMS_twilio(recipient, message)
	return send_SMS_yunpian(recipient, message)


def send_SMS_yunpian(recipient, message):
	from yunpian.SmsOperator import SmsOperator

	sms_operator = SmsOperator(settings.YUNPIAN_API_KEY)

	print message

	print "Sending message to {0} via Yunpian...".format(recipient)
	result = sms_operator.single_send({
		'mobile': recipient,
		'text': message
	})

	# display delivery information to console
	success = True if result.content['code'] == 0 else False
	if success:
		print "Message successfully delivered."
		return True
	else:
		print "Failed to send message"
		print result.content['msg']
		print result.content['detail']
		return False


def send_SMS_twilio(recipient, message):
	from twilio.rest import TwilioRestClient
	from twilio import TwilioRestException

	recipient = "+86" + recipient

	client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

	try:
		message = client.messages.create(
			body=message,
			to=recipient,
			from_=settings.TWILIO_SENDER
		)
	except TwilioRestException as e:
		print "something went wrong with the SMS messaging: {0}".format(e)
		return
	sid = message.sid
	print "Message {0} has been successfully sent.".format(sid)


def generate_pin(length=settings.PIN_LEN):
	return ''.join(random.choice(string.digits) for _ in range(length))


def check_pin(phone, pin):
	try:
		rec = registrar.models.PIN.objects.get(phone_number=phone, pin=pin)
	except ObjectDoesNotExist:
		return False

	delta = timezone.now() - rec.updated_on
	if delta.seconds > settings.PIN_VALID_SECONDS:
		return False
	return True


def clean_pin(phone, pin):
	registrar.models.PIN.objects.filter(phone_number=phone, pin=pin).delete()


def create_user(phone):
	# check if user already exists
	if len(registrar.models.User.objects.filter(username=phone)):
		return False
	import merchandise.models
	import explore.models
	import moments.models
	import notifications.models

	user = registrar.models.User(username=phone)
	user.save()

	emchat = create_code(user)
	profile = registrar.models.Profile(user=user, emchatuser = emchat[0],emchatpd = emchat[1])
	profile.save()
	user_merchandise = merchandise.models.UserMerchandise(user=user)
	user_merchandise.save()
	user_explore = explore.models.UserExplore(user=user)
	user_explore.save()
	user_moments = moments.models.UserMoments(user=user)
	user_moments.save()
	user_notifications = notifications.models.UserNotifications(user=user)
	user_notifications.save()
	user_visitor = registrar.models.Visitor(user=user)
	user_visitor.save()

	return user


def update_user(user):
	import merchandise.models
	import explore.models
	import moments.models
	import notifications.models

	try:
		user.profile
	except ObjectDoesNotExist:
		profile = registrar.models.Profile(user=user)
		profile.save()
	try:
		user.usermerchandise
	except:
		user_merchandise = merchandise.models.UserMerchandise(user=user)
		user_merchandise.save()
	try:
		user.userexplore
	except:
		user_explore = explore.models.UserExplore(user=user)
		user_explore.save()
	try:
		user.usermoments
	except:
		user_moments = moments.models.UserMoments(user=user)
		user_moments.save()
	try:
		user.usernotifications
	except:
		user_notifications = notifications.models.UserNotifications(user=user)
		user_notifications.save()
	try:
		user.visitor
	except:
		visitor = registrar.models.Visitor(user=user)
		visitor.save()


def get_file_extension(filename):
	return os.path.splitext(filename)[-1][1:]


def get_avatar_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "registrar/user_profile/{phone_number}/avatar.{ext}"
	return file_path.format(phone_number=instance.user.username, ext=extension)


def get_commercial_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "commercial/{commercial_id}/cover.{ext}"
	return file_path.format(commercial_id=instance.pk, ext=extension)


def get_ticket_cover_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "tickets/{ticket_id}/cover.{ext}"
	return file_path.format(ticket_id=instance.pk, ext=extension)


def get_ticket_listing_cover_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "tickets/{ticket_id}/listingcover.{ext}"
	return file_path.format(ticket_id=instance.pk, ext=extension)


def get_explore_highlight_upload_path(instance, filename):
	extension = get_file_extension(filename)
	pk = instance.pk
	if instance.pk is None:
		pass
	file_path = "explore/highlight/{id}/cover.{ext}".format(id=pk, ext=extension)
	return file_path


def get_ticket_detail_cover_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "tickets/{ticket_id}/detailcover.{ext}"
	return file_path.format(ticket_id=instance.pk, ext=extension)

def get_explore_post_cover_upload_path(instance, filename):
	extension = get_file_extension(filename)
	file_path = "explore/post/{post_id}/cover.{ext}"
	return file_path.format(post_id=instance.pk, ext = extension)


def compress_image(image_file):
	image = Image.open(image_file)
	image.thumbnail(settings.AVATAR_SIZE)
	tempfile_io = StringIO.StringIO()
	image.save(tempfile_io, format='JPEG')
	basename = os.path.splitext(image_file.name)[0:-1][0]
	newname = basename + '.jpg'
	image_file = InMemoryUploadedFile(tempfile_io, None, newname, 'image/jpg', tempfile_io.len, None)
	return image_file


def create_promotion_url(code):
	import base64
	import vip.settings
	data = {
		'promotion': code
	}
	s = urllib.urlencode(data)
	s = base64.b64encode(s)
	return "{0}/registrar?{1}".format(vip.settings.HOST, s)


def get_order(order_number):
	from merchandise.models import TicketOrder, DisneyOrder, ConcertOrder, SceneryOrder
	try:
		order = TicketOrder.objects.get(order_number=order_number)
	except ObjectDoesNotExist:
		return None
	if type(order_number) is unicode:
		order_number = order_number.encode('utf8')
	if order.get_type() == 'disney':
		order = DisneyOrder.objects.get(order_number=order_number)
	elif order.get_type() == 'concert':
		order = ConcertOrder.objects.get(order_number=order_number)
	elif order.get_type() == 'scenery':
		order = SceneryOrder.objects.get(order_number=order_number)
	else:
		order = None
	return order


def paginate(data_list, page_number, page_size=10):
	from django.core.paginator import Paginator
	pages = Paginator(data_list, page_size)
	if page_number not in pages.page_range:
		return False, False
	page = pages.page(page_number)
	return page.object_list, page.has_next()


def set_city(user, city):
	from merchandise.models import City
	if type(city) is not City:
		return False
	user.usermerchandise.current_city = city


def html2text(html_str):
	from bs4 import BeautifulSoup as bs
	return bs(html_str, 'html.parser').get_text()


class OverwriteStorage(FileSystemStorage):
	def get_available_name(self, name):
		if self.exists(name):
			os.remove(os.path.join(settings.MEDIA_ROOT, name))
		return name


def parse_time(publish_time):
	# time = timezone.now() - publish_time
	time_now = timezone.now()+datetime.timedelta(hours=8)
	time_publish = publish_time + datetime.timedelta(hours=8)
	time = time_now - time_publish 
	if time.seconds <= 1 * 60:
		return '刚刚'
	if time.days< 1:
		if time_publish.day != time_now.day:
			return "昨天 {0}:{1}".format(str((publish_time.hour + 8) % 24).zfill(2), str(publish_time.minute).zfill(2))
		return "{0}:{1}".format(str((publish_time.hour+8) % 24).zfill(2), str(publish_time.minute).zfill(2))
	if time.days < 2:
		return "1天前"
	if time.days < 3:
		return "2天前"
	if time.days < 4:
		return "3天前"
	if time.days >= 4:
		return "{0}-{1}-{2}".format(publish_time.year, publish_time.month, publish_time.day)


def is_phone_number(number):
	pattern = r'^(13[0-9]|14[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$'
	import re
	prog = re.compile(pattern)
	return prog.match(number)
	# return len(number) == 11 and number.isdigit()


def masked_phone_number(number):
	if is_phone_number(number):
		return number[0:3] + '*' * 4 + number[7:]
	return number


def str_to_bool(string):
	if type(string) != bool:
		if string.lower() in ['false', 'f', '0']:
			return False
		elif string.lower() in ['true', 't', '1']:
			return True
		else:
			raise ValueError("Unrecognizable string, cannot convert to boolean")
	return string


def async(function):
	def decorator(*args, **kwargs):
		t = Thread(target=function, args=args, kwargs=kwargs)
		t.daemon = True
		# time.sleep(delay)
		t.start()

	# return True
	return decorator

def contains_sensitive(published):
	count = 0
	words = Sensitive.objects.all()
	for i in words:
		count += published.count(i.words)
	if count > 0:
		return True
	else:
		return False

def create_code(number):
	user ="caymen"+ str(number)[1:11]
	passwd = ''.join(random.sample("abcdefghijklmnopqrstuvwxyz", 8))
	app_client_auth = AppClientAuth(org_name, app_name, client_id, client_secret)
	success, result = register_new_user(org_name, app_name, app_client_auth, user, passwd)
	if success:
		return user, passwd
	return None, None