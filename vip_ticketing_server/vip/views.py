# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

import vip.settings as settings
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, FileResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from alipay.alipay import check_notify_sign
from wechatpay.wxpay_sdk.Wx_Pay import WxPayBasic
import xmltodict
# Create your views here.
def index(request):
	return HttpResponse("IF YOU SEE THIS SENTENCE, THE SERVER IS UP")

@require_GET
def get_asset(request, file_path):
	params = request.GET
	# file_path = file_path.decode('utf-8')
	path = os.path.join(settings.MEDIA_ROOT, file_path)

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

	# from vip.utils import get_file_extension
	# ext = get_file_extension(path)
	# response = HttpResponse(content_type='image/{0}'.format(ext))
	# img.save(response, ext)

	response = HttpResponse(content_type='image/jpeg')
	img.convert('RGB').save(response, 'jpeg')

	return response

def require_login(request):
	return HttpResponseForbidden("对不起, 您还未登录")


@login_required
def test_logged_in(request):
	return HttpResponse("已登录状态")

@require_POST
@csrf_exempt
def test_post(request):
	return HttpResponse('success')


@csrf_exempt
def unionpay_callback(request):
	from vip.utils import get_order
	print "[UnionPay] callback being executed -----"

	order_number = request.POST.get('orderId')
	order = get_order(order_number)
	if order is None:
		return HttpResponseBadRequest()

	resp_code = request.POST.get('respCode')

	# save all the transaction info in the form of raw url-encoded string into the order model object
	encoded_data = request.POST.urlencode()
	print encoded_data
	order.save_transaction_info(encoded_data)

	if resp_code == '00' or resp_code == 'A6':
		result = order.confirm_transaction()
		if result:
			print "Transaction successful!"
		else:
			print "Transaction already complete, operation duplicated"
	else:
		msg = request.POST.get('respMsg')
		print "Transaction unsuccessful: "
		print msg
		result = order.cancel_transaction()
		if result:
			print "Transaction canceled"
		else:
			print "Transaction already canceled, operation duplicated"

	return HttpResponse("OK")


@require_GET
def get_homepage(request):
	return render(request, 'home/index_container.html')


@require_GET
def get_homepage_temp(request):
	return render(request, 'home/index_.html')


def get_iframe(request):
	return render(request, 'home/pullrefresh_sub.html')


def get_homepage_content(request):
	path = os.path.join(settings.BASE_DIR, 'templates', 'home', 'index.html')
	f = open(path, 'rb')
	return FileResponse(f, content_type='text/html; charset=utf-8')


def get_manifest(request):
	path = os.path.join(settings.BASE_DIR, 'templates', 'home', 'index.appcache')
	f = open(path, 'rb')
	return FileResponse(f, content_type='text/cache-manifest; charset=utf-8')

@csrf_exempt
@require_GET
def alipay_return_url(request):   # 支付宝同步通知跳转url，get 方式
	from vip.utils import get_order
	out_trade_no = request.GET.get('out_trade_no')
	trade_status = request.GET.get('trade_status')
	order = get_order(out_trade_no)
	if order is None:
		return HttpResponseBadRequest()
	if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
		return HttpResponse('success')
	else:
		HttpResponse("fail")

@require_POST
@csrf_exempt
def alipay_notify_url(request):
	verify_status = check_notify_sign(request)
	if verify_status:
		from vip.utils import get_order
		out_trade_no = request.POST.get('out_trade_no')
		order = get_order(out_trade_no)
		if order is None:
			return HttpResponseBadRequest()
		encoded_data = request.POST.urlencode()
		print encoded_data
		order.save_transaction_info(encoded_data)
		trade_status = request.POST.get("trade_status")
		if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
			result = order.confirm_transaction()
			if result:
				print "Transaction successful!"
			else:
				print "Transaction already complete, operation duplicated"
			return HttpResponse('success')
		else:
			result = order.cancel_transaction()
			if result:
				print "Transaction canceled"
			else:
				print "Transaction already canceled, operation duplicated"
			return HttpResponse('fail')
	return HttpResponse("fail")


@csrf_exempt
def wechat_pay_callback(request):
	req_xml_str = request.body

	# 回调处理：签名验证，订单查询验证
	# 返回验证结果（可作为直接返回给微信的xml）
	wechatpay_qrcode_config = {
		'wechatpay_appid': 'wx6c05f90910b55d08',  # 必填,微信分配的公众账号ID
		'wechatpay_key': 'FDSJOAIHssfjeoljh32jknib2332nnik',
		'wechatpay_mchid': '1384731102',  # 必填,微信支付分配的商户号
		'wechatpay_appsecret': 'FDSJOAIHssfjeoljh32jknib2332nnik',  # 必填,appid 密钥
	}
	wxpay = WxPayBasic(conf=wechatpay_qrcode_config)
	res_xml_str = wxpay.wxpay_callback(req_xml_str)

	res_xml_dict = xmltodict.parse(res_xml_str)
	from vip.utils import get_order
	if res_xml_dict['xml']['return_code'] == 'SUCCESS':
		# 处理商户订单逻辑
		req_xml_dict = xmltodict.parse(req_xml_str)
		total_fee = req_xml_dict['xml']['total_fee']
		out_trade_no = req_xml_dict['xml']['out_trade_no']
		order = get_order(out_trade_no)
		order.save_transaction_info(res_xml_dict)
		if order is None:
			return HttpResponseBadRequest()
		result = order.confirm_transaction()
		if result:
			print "Transaction successful!"
		else:
			print "Transaction already complete, operation duplicated"

	else:
		msg = res_xml_dict['xml']['return_msg']
		print "Transaction unsuccessful: "
		print msg
		req_xml_dict = xmltodict.parse(req_xml_str)
		out_trade_no = req_xml_dict['xml']['out_trade_no']
		order = get_order(out_trade_no)
		result = order.cancel_transaction()
		if result:
			print "Transaction canceled"
		else:
			print "Transaction already canceled, operation duplicated"

	return HttpResponse(res_xml_str, content_type='text/xml')
