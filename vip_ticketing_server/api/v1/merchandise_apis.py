#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from merchandise.models import *
from registrar.forms import *

from django.core.paginator import Paginator
from notifications.notifications import *

from threading import *
from alipay.alipay import *
from wechatpay.wxpay_sdk.Wx_Pay import *
from vip import settings

notify_url = settings.HOST+'/wechat_pay_callback/'

@require_GET
def get_disney_tickets(request):
	'''
	分页获取迪士尼门票列表
	:param p: 页码数
	:return: 200 迪士尼列表
	400 页码数上传有误
	404 页码超出范围
	'''
	page_number = request.GET.get('p')

	ticket_models = DisneyTicket.objects.all()
	ticket_json_list = [i.to_json() for i in ticket_models]

	if page_number is not None:
		try:
			page_number = int(page_number)
		except:
			return HttpResponseBadRequest("参数不正确")

		ticket_json_list, has_next = utils.paginate(ticket_json_list, page_number)
		if ticket_json_list is False:
			return HttpResponseNotFound("页码超出范围")

		return JsonResponse({
			'list': ticket_json_list,
			'has_next': has_next
		}, safe=False)
	return JsonResponse(ticket_json_list, safe=False)


@require_GET
def get_disney_ticket(request, id):
	try:
		ticket = DisneyTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到迪士尼门票{0}".format(id))
	# if request.GET.get('past'):
	# 	ticket_data = ticket.to_json(simple=False, past=True)
	# else:
	ticket_data = ticket.to_json(simple=False)

	ticket_data['liked'] = False
	if request.user.is_authenticated():
		flag = ticket in request.user.usermerchandise.disney_likes.all()
		ticket_data['liked'] = flag

	if not request.GET:
		return JsonResponse(ticket_data, safe=False)

	ret = {}
	for key, _ in request.GET.iteritems():
		if key in ticket_data:
			ret[key] = ticket_data[key]

	return JsonResponse(ret, safe=False)


@login_required
def like_disney_ticket(request, id):
	try:
		ticket = DisneyTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到迪士尼门票{0}".format(id))
	utils.update_user(request.user)
	# apiKey, secretKey, userid, channel_id, device_type, deploy_status = get_current_device_param_same_user(request.user.id)
	msg = request.user.usermerchandise.toggle_like_disney(ticket)

	liked = ticket in request.user.usermerchandise.disney_likes.all()

	if liked:
		baidu_push(recipient=request.user, action='TicketToggle', params={
			'ticket': ticket,
			'liked': liked,
			'trigger_user': request.user
		})
	return HttpResponse(msg)

#add by sunming
@require_GET
def get_scenery_tickets(request,sight):
	'''
	分页获取景区门票列表
	:param p: 页码数
	:return: 200 景区门票列表
	400 页码数上传有误
	404 页码超出范围
	'''
	page_number = request.GET.get('p')

	ticket_models = SceneryTicket.objects.filter(sight = sight)
	ticket_json_list = [i.to_json() for i in ticket_models]

	if page_number is not None:
		try:
			page_number = int(page_number)
		except:
			return HttpResponseBadRequest("参数不正确")

		ticket_json_list, has_next = utils.paginate(ticket_json_list, page_number)
		if ticket_json_list is False:
			return HttpResponseNotFound("页码超出范围")

		return JsonResponse({
			'list': ticket_json_list,
			'has_next': has_next
		}, safe=False)
	return JsonResponse(ticket_json_list, safe=False)


@require_GET
def get_scenery_ticket(request, id):
	try:
		ticket = SceneryTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到景区门票{0}".format(id))
	ticket_data = ticket.to_json(simple=False)

	ticket_data['liked'] = False
	if request.user.is_authenticated():
		flag = ticket in request.user.usermerchandise.disney_likes.all()
		ticket_data['liked'] = flag

	if not request.GET:
		return JsonResponse(ticket_data, safe=False)

	ret = {}
	for key, _ in request.GET.iteritems():
		if key in ticket_data:
			ret[key] = ticket_data[key]

	return JsonResponse(ret, safe=False)


@login_required
def like_scenery_ticket(request, id):
	try:
		ticket = SceneryTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到景区门票{0}".format(id))
	utils.update_user(request.user)
	# apiKey, secretKey, userid, channel_id, device_type, deploy_status = get_current_device_param_same_user(request.user.id)
	msg = request.user.usermerchandise.toggle_like_scenery(ticket)

	liked = ticket in request.user.usermerchandise.scenery_likes.all()

	if liked:
		baidu_push(recipient=request.user, action='TicketToggle', params={
			'ticket': ticket,
			'liked': liked,
			'trigger_user': request.user
		})
	return HttpResponse(msg)
#endadd by sunming

@login_required
def get_liked_tickets(request, ticket_type):
	user = request.user.usermerchandise
	likes = []
	disneys = [i.to_json() for i in user.disney_likes.all()]
	concerts = [i.to_json() for i in user.concert_likes.all()]
	aeros = [i.to_json() for i in user.aero_likes.all()]
	scenery = [i.to_json() for i in user.scenery_likes.all()]

	if ticket_type == 'disney':
		return JsonResponse(disneys, safe=False)
	if ticket_type == 'concert':
		return JsonResponse(concerts, safe=False)
	if ticket_type == 'aerospace':
		return JsonResponse(aeros, safe=False)
	if ticket_type == 'scenery':
		return JsonResponse(scenery, safe=False)

	likes = disneys + concerts + aeros + scenery
	return JsonResponse(likes, safe=False)


def get_concert_tickets(request):
	json_list = [i.to_json() for i in ConcertTicket.objects.all().order_by('-time')]

	page_number = request.GET.get('p')
	if page_number is not None:
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
	return JsonResponse(json_list, safe=False)


def get_concert_ticket(request, id):
	try:
		ticket = ConcertTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound('找不到演唱会门票{0}'.format(id))

	ticket_data = ticket.to_json(simple=False)

	ticket_data['liked'] = False
	if request.user.is_authenticated():
		flag = ticket in request.user.usermerchandise.concert_likes.all()
		ticket_data['liked'] = flag

	if not request.GET:
		return JsonResponse(ticket_data, safe=False)
	ret = {}
	for key, _ in request.GET.iteritems():
		if key in ticket_data:
			ret[key] = ticket_data[key]
	return JsonResponse(ret, safe=False)

@login_required
def like_concert_ticket(request, id):
	try:
		ticket = ConcertTicket.objects.get(pk =id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到演唱会门票{0}".format(id))
	utils.update_user(request.user)
	# apiKey, secretKey, userid, channel_id, device_type, deploy_status = get_current_device_param_same_user(request.user.id)
	msg = request.user.usermerchandise.toggle_like_concert(ticket)
	liked = ticket in request.user.usermerchandise.concert_likes.all()
	if liked:
		baidu_push(recipient=request.user, action='TicketToggle', params={
			'ticket': ticket,
			'liked': liked,
			'trigger_user': request.user
		})
	return HttpResponse(msg)


def get_aero_tickets(request):
	json_list = [i.to_json() for i in AerospaceTicket.objects.all()]

	page_number = request.GET.get('p')
	if page_number is not None:
		try:
			page_number = int(page_number)
		except:
			return HttpResponseBadRequest("参数不正确")

		json_list, has_next = utils.paginate(json_list, page_number)
		if not json_list:
			return HttpResponseNotFound("页码超出范围")

		return JsonResponse({
			'list': json_list,
			'has_next': has_next
		}, safe=False)
	return JsonResponse(json_list, safe=False)


def get_aero_ticket(request, id):
	try:
		ticket = AerospaceTicket.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到宇航套餐{0}".format(id))

	ticket_data = ticket.to_json(simple=False)

	ticket_data['liked'] = False
	if request.user.is_authenticated():
		flag = ticket in request.user.usermerchandise.aero_likes.all()
		ticket_data['liked'] = flag

	if not request.GET:
		return JsonResponse(ticket_data, safe=False)
	ret = {}
	for key, _ in request.GET.iteritems():
		if key in ticket_data:
			ret[key] = ticket_data[key]
	return JsonResponse(ret, safe=False)


@login_required
def like_aero_ticket(request, id):
	try:
		ticket = AerospaceTicket.objects.get(pk =id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到宇航套餐{0}".format(id))
	utils.update_user(request.user)
	# apiKey, secretKey, userid, channel_id, device_type, deploy_status = get_current_device_param_same_user(request.user.id)
	msg = request.user.usermerchandise.toggle_like_aero(ticket)
	liked = ticket in request.user.usermerchandise.aero_likes.all()
	if liked:
		baidu_push(recipient=request.user, action='TicketToggle', params={
			'ticket': ticket,
			'liked': liked,
			'trigger_user': request.user
		})
	return HttpResponse(msg)

@require_GET
def get_commercials(request):
	commercial_model_list = Commercial.objects.filter(display=True)
	json_list = [i.to_json() for i in commercial_model_list]
	return JsonResponse(json_list, safe=False)

@login_required
@require_POST
@csrf_exempt
def purchase_ticket(request, ticket_type, id):
	'''
        提交商品订单
        :param request: HTTP请求对象
        :param ticket_type: 商品类型, 接受disney, concert, aerospace, scenery
        :param id: 商品id
        :return: 200 创建订单成功
        400 post参数错误
        403 余票不足
        404 找不到相应商品
        '''

	# disney ticket mandatory fields
	mandatory = {
		'disney': ['identification', 'count', 'contact', 'schedule'],
		'concert': ['count', 'contact'],
		'scenery': ['identification', 'count', 'contact', 'schedule'],
	}
	optional = {
		'disney': ['pickup'],
		'concert': ['shipping_address'],
	}

	params = {
		'purchaser': request.user.usermerchandise,
	}
	try:
		for key in mandatory[ticket_type]:
			params[key] = request.POST[key]
	except KeyError:
		return HttpResponseBadRequest("订票参数格式错误, 提交订单失败")

	if ticket_type != 'scenery':
		for key in optional[ticket_type]:
			if request.POST.get(key) is not None:
				params[key] = request.POST.get(key)

	if ticket_type == 'disney':
		try:
			params['ticket_type'] = DisneyTicket.objects.get(pk=id)
		except ObjectDoesNotExist:
			return HttpResponseNotFound('迪士尼门票{0}不存在, 提交订单失败'.format(id))
		response = create_disney_order(**params)
	elif ticket_type == 'concert':
		try:
			params['ticket_type'] = ConcertTicket.objects.get(pk=id)
		except ObjectDoesNotExist:
			return HttpResponseNotFound("演唱会票{0}不存在, 提交订单失败".format(id))
		response = create_concert_order(**params)
	elif ticket_type == 'scenery':
		try:
			params['ticket_type'] = SceneryTicket.objects.get(pk=id)
		except ObjectDoesNotExist:
			return HttpResponseNotFound('景区门票{0}不存在, 提交订单失败'.format(id))
		response = create_scenery_order(**params)
	else:
		response = HttpResponseBadRequest("未知错误")
	if 'payment' in request.POST:
		pay_type = request.POST['payment']
		if pay_type == "unionpay":
			return unionpay_purchase_ticket(response)
		elif pay_type == "alipay":
			return  alipay_purchase_ticket(response)
		elif pay_type == "wechatpay":
			return wechatpay_purchase_ticket(response, id)
		else:
			return response
	else:
		return unionpay_purchase_ticket(response)

def wechatpay_purchase_ticket(response, id):
	if type(response) == dict:
		amount = response['amount'] * 100
		orderid = response['order_number']
		amount = int(amount)
		params = {
			'body': u"订单商品",  # 商品或支付单简要描述,例如：Ipad mini  16G  白色
			'out_trade_no': orderid,  # 商户系统内部的订单号,32个字符内、可包含字母
			'total_fee': amount,  # 订单总金额，单位为分
			'product_id': id,  # 商品ID
			'notify_url': notify_url,
			'trade_type': 'APP',
		}

		wechatpay_qrcode_config = {
			'wechatpay_appid': 'wx6c05f90910b55d08',  # 必填,微信分配的公众账号ID
			'wechatpay_key': 'FDSJOAIHssfjeoljh32jknib2332nnik',
			'wechatpay_mchid': '1384731102',  # 必填,微信支付分配的商户号
			'wechatpay_appsecret': 'FDSJOAIHssfjeoljh32jknib2332nnik',  # 必填,appid 密钥
		}
		wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
		app_result = wxpay.unifiedorder_get_app_url(**params)
		# return JsonResponse(app_result, safe=False)
		return JsonResponse({"result":app_result,"order_number":orderid,"payment":"wxpay"}, safe=False)
	return response

def alipay_purchase_ticket(response):
	if type(response) == dict:
		amount = response['amount']
		order_number = response['order_number']
		amount = int(amount)
		alipay = Alipay(out_trade_no = order_number, subject = u"卡曼天连科技有限公司", body = u"卡曼天连", total_fee = amount)
		result = alipay.create_pay_url()
		# url = alipay._build_sign_url()
		# sign = alipay._create_sign(url)
		# s = result.split('&')
		# list  = []
		# for i in s:
		# 	list.append(eval(str(i.split('=')).replace('"','')))
		# result = {}
		# for obj in list:
		# 	result.setdefault(obj[0], obj[1])
		# print result
		return JsonResponse({"result":result,"order_number":order_number,"payment":"alipay"}, safe=False)
	return response


def unionpay_purchase_ticket(response):
	if type(response) == dict:
		from unionpay.client import UnionpayClient
		from unionpay.util.helper import load_config

		config = load_config(settings.UNIONPAY_CONFIG_PATH)

		client = UnionpayClient(config)
		amount = response['amount'] * 100
		orderid = response['order_number']
		amount = int(amount)

		from unionpay.error import UnionpayError
		try:
			payment_resp = client.pay(amount, orderid)
		except UnionpayError, msg:
			return HttpResponseBadRequest(msg)
		if payment_resp['respCode'] == '00':
			return JsonResponse({
				'tn': payment_resp['tn'],
				'order_number': orderid,
				'payment':'unionpay'
			}, safe=False)
		return HttpResponseBadRequest(payment_resp['respMsg'])
	return response


def create_disney_order(ticket_type, contact, purchaser, count, schedule, identification, pickup=False):
	try:
		count = int(count)
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")
	# if count > 5:
	# 	return HttpResponseForbidden("一次性购票不能超过5张, 提交订单失败")
	try:
		schedule = DisneySchedule.objects.get(pk=schedule)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("订票日期有误, 提交订单失败")

	if schedule.inventory < count:
		return HttpResponseForbidden("该商品剩余数量为{0}, 余票不足, 提交订单失败".format(schedule.inventory))
	if type(pickup) != bool:
		if pickup.lower() in ['false', 'f', '0']:
			pickup = False
		else:
			pickup = True
	try:
		new_order = DisneyOrder(**locals())
		new_order.create_order_number()
		new_order.schedule = schedule
		new_order.save()
		schedule.inventory -= count
		schedule.save()
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")

	return {
		'amount': new_order.get_price(),
		'order_number': new_order.order_number
	}


def create_concert_order(count, ticket_type, contact, purchaser, shipping_address=""):
	try:
		count = int(count)
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")
	if count > ticket_type.available:
		return HttpResponseForbidden("该商品剩余数量为{0}, 余票不足, 提交订单失败".format(ticket_type.available))
	try:
		new_order = ConcertOrder(**locals())
		new_order.create_order_number()
		new_order.save()
		ticket_type.available -= count
		ticket_type.save()
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")

	return {
		'amount': new_order.get_price(),
		'order_number': new_order.order_number
	}

def create_scenery_order(ticket_type, contact, purchaser, count, schedule, identification):
	try:
		count = int(count)
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")
	try:
		schedule = ScenerySchedule.objects.get(pk=schedule)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("订票日期有误, 提交订单失败")

	if schedule.inventory < count:
		return HttpResponseForbidden("该商品剩余数量为{0}, 余票不足, 提交订单失败".format(schedule.inventory))
	try:
		new_order = SceneryOrder(**locals())
		new_order.create_order_number()
		new_order.schedule = schedule
		new_order.save()
		schedule.inventory -= count
		schedule.save()
	except ValueError:
		return HttpResponseBadRequest("订票参数传值有错, 提交订单失败")

	return {
		'amount': new_order.get_price(),
		'order_number': new_order.order_number
	}


@login_required
@require_POST
@csrf_exempt
def cancel_order(request, order_number):

	from vip.utils import get_order
	order = get_order(order_number)
	if order is None:
		return HttpResponseNotFound("订单不存在, 取消失败") #404

	# check if this order belongs to the current user
	user = request.user.usermerchandise
	if order.purchaser != user:
		return HttpResponseForbidden("订单{0}不属于用户{1}, 取消失败".format(order_number, str(user))) #403

	result = order.cancel_transaction()
	if result:
		return HttpResponse("订单{0}已取消".format(order_number)) #200
	return HttpResponseBadRequest("重复取消订单 {0}, 操作失败".format(order_number)) #400


@login_required
@require_GET
def get_purchased_orders(request):
	filter = request.GET.get('filter')
	page_number = request.GET.get('p')
	user = request.user.usermerchandise

	import datetime
	now = datetime.datetime.now()

	disney_filter_params = {
		"status": 'P'
	}
	concert_filter_params = {
		"status": 'P'
	}
	scenery_filter_params = {
		"status": 'P'
	}

	# split past/prospective orders
	if filter:
		if filter == 'past':
			disney_filter_params["ticket_type__validity__lt"] = now
			concert_filter_params['ticket_type__time__lt'] = now
			scenery_filter_params["ticket_type__validity__lt"] = now
		elif filter == 'prospective':
			disney_filter_params["ticket_type__validity__gt"] = now
			concert_filter_params['ticket_type__time__gt'] = now
			scenery_filter_params["ticket_type__validity__gt"] = now

	disney_orders = user.disneyorders.filter(**disney_filter_params)
	concert_orders = user.concertorders.filter(**concert_filter_params)
	scenery_orders = user.sceneryorders.filter(**scenery_filter_params)

	def parse_order(order):
		ticket = {
			"type": order.get_type(),
			"title": order.ticket_type.name,
			"id": order.ticket_type.pk,
			"cover": order.ticket_type.detail_cover.url if order.ticket_type.detail_cover else ""
		}
		if order.get_type() == 'disney':
			ticket['validity'] = order.ticket_type.validity
		elif order.get_type() == 'concert':
			ticket['time'] = order.ticket_type.time
		elif order.get_type() == 'scenery':
			ticket['validity'] = order.ticket_type.validity

		this = {
			"order_number": order.order_number,
			"ticket": ticket,
			"count": order.count
		}
		return this

	disney_json_list = [parse_order(i) for i in disney_orders]
	concert_json_list = [parse_order(i) for i in concert_orders]
	scenery_json_list = [parse_order(i) for i in scenery_orders]
	json_list = disney_json_list + concert_json_list + scenery_json_list

	# pagination
	if page_number is not None:
		try:
			page_number = int(page_number)
		except:
			return HttpResponseBadRequest("参数不正确")
		json_list, has_next = utils.paginate(json_list, page_number)
		if json_list is False:
			return HttpResponseNotFound("页码超出范围")
		return JsonResponse({
			"list": json_list,
			"has_next": has_next,
		}, safe=False)

	return JsonResponse(json_list, safe=False)


@require_GET
@login_required
def get_order_detail(request, order_number):
	try:
		order = TicketOrder.objects.get(order_number=order_number)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("订单{0}不存在, 请求失败".format(order_number))
	order = order.get_order_object()

	ticket_field = {
		"type": order.get_type(),
		"id": order.ticket_type.pk
	}
	this = {
		"order_number": order_number,
		"ticket": ticket_field
	}
	if order.get_type() == 'disney':
		this["identification"] = order.identification
		this['schedule'] = order.schedule.date
	elif order.get_type() == 'concert':
		this["shipping_status"] = "已寄出" if order.shipped else "等待寄送"
		if order.shipped:
			this['shipping_code'] = order.shipping_code
	elif order.get_type() == 'scenery':
		this["identification"] = order.identification
		this['schedule'] = order.schedule.date
		print "order.schedule.date",order.schedule.date

	return JsonResponse(this, safe=False)
