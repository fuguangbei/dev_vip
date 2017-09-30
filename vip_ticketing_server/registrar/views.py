#-*- coding: utf-8 -*-
import vip.settings as settings
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from registrar.models import *

# Create your views here.
def index(request):
	return render(request, 'registrar/register.html')

def login(request):
	return render(request, 'registrar/login.html', {
		'user': request.user
	})

def landing(request):
	return render(request, 'registrar/download.html')

@csrf_exempt
def signup(request):
	params = request.POST
	try:
		phone_number = request.POST['phone_number']
		pin = request.POST['PIN']
		secret = request.POST['secret']
	except:
		return HttpResponseBadRequest("参数不正确")

	import base64
	dec_str = base64.b64decode(secret)
	promo = dec_str.split('=')[1]

	import vip.utils as utils

	if not utils.check_pin(phone_number, pin):
		return HttpResponseBadRequest("注册失败")

	success_flag = utils.create_user(phone_number)
	if not success_flag:
		return HttpResponseBadRequest("该手机号已被使用, 注册失败")
	user = authenticate(phone_number=phone_number, pin=pin)

	promo_rec = Promotion.objects.filter(code=promo, valid=True)
	if not len(promo_rec):
		return HttpResponseBadRequest("邀请码错误, 注册失败")

	promoter = promo_rec[0].owner

	if user is not None:
		user.profile.promoter = promoter
		user.profile.save()
		if user.is_active:
			login(request, user)
			return HttpResponse("注册成功")
		else:
			return HttpResponseBadRequest("账户未激活")

	return HttpResponseBadRequest('注册失败')

@require_GET
def get_asset(request, file_path):
	params = request.GET
	path = os.path.join(settings.MEDIA_ROOT, 'registrar', file_path)

	size_table = settings.IMAGE_SIZE_TABLE
	size = 'raw'
	if 'size' in params and params['size'] in size_table:
		size = params['size']
	try:
		img = Image.open(path)
	except:
		return HttpResponseNotFound("图片不存在")
	if size != 'raw':
		img.thumbnail(size_table[size])

	response = HttpResponse(content_type='image/jpeg')
	img.convert('RGB').save(response, 'jpeg')

	return response


def get_pin(request, phone):
	from api.v1.registrar_apis import get_pin as get_pin_api

	return get_pin_api(request, phone, fake=True)

def get_master_pin(request):
	return HttpResponse("OK")