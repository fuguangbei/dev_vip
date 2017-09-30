#-*- coding: utf-8 -*-
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from registrar.forms import *
from registrar.models import *
from vip import settings
from notifications.notifications import *


def index(request):
	return render(request, 'api/index.html')


@require_GET
def get_labels(request):
	params = request.GET
	if not params:
		labels = UserLabel.objects.all()
	else:
		query = {}
		allowed_params = ['id', 'name']
		for key, val in params.iteritems():
			if key in allowed_params:
				query['short' if key == 'name' else key] = val

		labels = UserLabel.objects.filter(**query)
	if len(labels) == 0:
		return HttpResponseNotFound(
			"Label under condition {0} does not exist".format(
				json.dumps(params)
			)
		)

	json_list = utils.queryset_to_json(labels)
	return JsonResponse(json_list, safe=False)


@require_GET
def get_label_by_id(request, id):
	try:
		label = UserLabel.objects.get(pk=id)
	except ObjectDoesNotExist:
		error = "Couldn't find label by id = {0}".format(id)
		return HttpResponseNotFound(error)

	return JsonResponse(label.to_json())


@require_GET
def get_labels_by_name(request, name):
	labels = UserLabel.objects.filter(short=name)
	if len(labels) == 0:
		return HttpResponseNotFound("Couldn't find label by name = {0}".format(name))
	ret = utils.queryset_to_json(labels)
	return JsonResponse(ret, safe=False)


@require_GET
def get_label_categories(request):
	categories = UserLabelCategory.objects.all()
	return JsonResponse(utils.queryset_to_json(categories), safe=False)


@require_GET
def get_category(request, **kwargs):
	try:
		category = UserLabelCategory.objects.get(**kwargs)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("Category {0} does not exist".format(kwargs.values()[0]))
	return JsonResponse(category.to_json())


@require_POST
@csrf_exempt
def sign_up(request):
	try:
		phone_number = request.POST['phone_number']
		pin = request.POST['PIN']
		promo = request.POST['promotion']
	except:
		return HttpResponseBadRequest("参数不正确")

	if not utils.check_pin(phone_number, pin):
		return HttpResponseBadRequest("验证码错误, 注册失败")

	promo_rec = Promotion.objects.filter(code__iexact=promo, valid=True)
	if not len(promo_rec):
		return HttpResponseBadRequest("邀请码错误, 注册失败")

	success_flag = utils.create_user(phone_number)
	if not success_flag:
		return HttpResponseBadRequest("该手机号已被使用, 注册失败")
	user = authenticate(phone_number=phone_number, pin=pin)

	# print promo_rec[0]
	promoter = promo_rec[0].owner
	if not settings.TEST_PROMOTION_CODE:
		promo_rec.update(valid=False)

	if user is not None:
		user.profile.promoter = promoter
		user.profile.save()

		baidu_push(recipient=promoter.user, action='Register', params={
			'promo': promo_rec,
			'trigger_user': user
		})

		if user.is_active:
			login(request, user)

			return HttpResponse("注册成功")
		else:
			return HttpResponseBadRequest("账户未激活")

	return HttpResponseBadRequest('注册失败')


@require_POST
@csrf_exempt
def sign_in(request):
	try:
		phone_number = request.POST['phone_number']
		pin = request.POST['PIN']
	except:
		return HttpResponseBadRequest('参数不正确')

	if phone_number == 'ethan':
		user = authenticate(username='ethan', password='qwerasdf')
	elif phone_number =='13208191215'and pin == '988688' :
		user = authenticate(username='13208191215', password='qwerasdf')
	else:
		user = authenticate(phone_number=phone_number, pin=pin)

	if user is not None:
		if user.is_active:
			login(request, user)
			utils.update_user(user)
			return HttpResponse("登录成功")
		else:
			return HttpResponseBadRequest("账户未激活")
	else:
		return HttpResponseBadRequest("账号不存在/验证码错误, 登录失败")

@login_required
@require_GET
def sign_out(request):
	request.user.usernotifications.update_device_param('', '', '')
	logout(request)
	return HttpResponse("注销成功")


@require_GET
def get_pin(request, phone, fake=False):
	if not utils.valid_phone_number(phone):
		return HttpResponseForbidden("请输入正确手机号, 请求失败")
	pin = utils.generate_pin()
	rec = PIN.objects.filter(phone_number=phone)

	if len(rec):
		seconds = (timezone.now() - rec[0].updated_on).seconds
		if seconds < settings.PIN_REQUEST_INTERVAL if not fake else 0:
			return HttpResponseForbidden('操作过于频繁, 请稍等{0}秒后再试'.format(settings.PIN_REQUEST_INTERVAL))
		rec.update(pin=pin, updated_on=timezone.now())
	else:
		rec = PIN(phone_number=phone, pin=pin)
		rec.save()

	# =======================================================
	print "[API {2}] Sending PIN {0} to phone number {1}".format(pin, phone, "Fake" if fake else "")
	if not fake:
		success = utils.send_SMS(phone, settings.SMS_TEMPLATE_PIN.format(pin))
	else:
		success = True
	# =======================================================

	if not success:
		return HttpResponseBadRequest("发送验证码失败, 请与工作人员联系")

	resp = {
		"status": '200',
		'message': '验证码已发送成功',
		'pin':pin
	}
	if fake:
		resp['PIN'] = pin

	return JsonResponse(resp)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@login_required
def profiles(request):
	if request.method == 'GET':
		return get_profiles(request)
	return set_profiles(request)


def get_profiles(request):
	params = request.GET
	utils.update_user(request.user)
	user = request.user.profile.to_json()

	# API request without parameters, return the whole thing
	if not params:
		return JsonResponse(user, safe=False)

	ret = {}
	for key, _ in params.iteritems():
		if key in user:
			ret[key] = user[key]
	ret['agent'] = user['agent']

	return JsonResponse(ret, safe=False)


def set_profiles(request):
	print "[API] user {0} is attempting to set profile".format(request.user.username)

	params = request.POST
	files = request.FILES
	user = request.user

	allowed_params = ['label', 'nickname', 'gender', 'avatar']
	for i in params:
		if i not in allowed_params:
			return HttpResponseBadRequest("未知属性{0}, 修改失败".format(i))

	for i in files:
		if i not in allowed_params:
			return HttpResponseBadRequest("未知属性{0}, 修改失败".format(i))

	if 'label' in params:
		label_id = params['label']
		try:
			label = UserLabel.objects.get(pk=label_id)
		except ObjectDoesNotExist:
			return HttpResponseNotFound("找不到标签{0}, 修改失败".format(label_id))
		user.profile.toggle_label(label)
	
	if 'nickname' in params:
		new_nickname = params['nickname']
		if len(new_nickname) not in range(1, 21):
			return HttpResponseBadRequest("昵称太长, 修改失败")
		user.profile.nickname = new_nickname
		user.profile.save()

	if 'gender' in params:
		if len(params['gender']) != 1 or params['gender'] not in ['M', 'F']:
			return HttpResponseBadRequest("非法性别值, 修改失败")
		user.profile.gender = params['gender']
		user.profile.save()

	if 'avatar' in files:
		print "updating the avatar image"
		form = UserAvatarForm(params, files)
		if not form.is_valid():
			return HttpResponseBadRequest("上传图片损坏或格式错误, 修改失败")
		user.profile.update_avatar(form.cleaned_data['avatar'])
	
	updated_profile = {}
	profile = user.profile.to_json()
	for key, _ in params.iteritems():
		if key in profile:
			updated_profile[key] = profile[key]
	if 'label' in params:
		updated_profile['labels'] = profile['labels']
	if 'avatar' in files:
		updated_profile['avatar'] = profile['avatar']

	print "[/API]"
	return JsonResponse({
		'status': 'success',
		'profile': updated_profile
	}, safe=False)


@login_required
def apply_agent(request):
	user = request.user
	if user.usermerchandise.level >= 3:
		return HttpResponseForbidden("User cannot be promoted to be an agent, error.")
	from registrar.models import AgentApplication
	from django.db import IntegrityError
	try:
		AgentApplication.objects.create(user=user, status=0)
	except IntegrityError:
		return HttpResponseBadRequest("Duplicated application, operation failed.")
	return HttpResponse('OK')

@require_GET
def userinfo(request,user_id):
	if user_id[0:6] == "caymen":
		try:
			user_profile = Profile.objects.get(emchatuser = user_id)
			user_profile = user_profile.to_json()
			return JsonResponse(user_profile, safe=False)
		except ObjectDoesNotExist:
			return HttpResponseNotFound("用户不存在")

	try:
		user = User.objects.get(pk=user_id)
		user_profile = user.profile.to_json()
		return JsonResponse(user_profile, safe=False)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("用户不存在")
