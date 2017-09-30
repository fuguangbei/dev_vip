# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from merchandise.models import TicketOrder, DisneyOrder, ConcertOrder, DisneyTicket, SceneryOrder, SceneryTicket
from registrar.models import Profile
from django.views.decorators.csrf import csrf_exempt

import vip.utils as utils


@login_required(login_url='/cms/login/')
def index(request):
	owned_users = get_owned_users(request)
	num_users = len(owned_users)
	if request.user.is_superuser:
		paid_orders = [i for i in DisneyOrder.objects.filter(status='P')] + [i for i in ConcertOrder.objects.filter(status='P')] + [i for i in SceneryOrder.objects.filter(status='P')]
		num_orders = len(paid_orders)
		sales = 0
		for i in paid_orders:
			sales += i.get_price()
	else:
		paid_orders = []
		for order_class in [DisneyOrder, ConcertOrder, SceneryOrder]:
			order_list = order_class.objects.filter(status='P', purchaser__in=[i.usermerchandise for i in owned_users])
			paid_orders += order_list
		num_orders = len(paid_orders)
		sales = 0
		for i in paid_orders:
			sales += i.get_price()

	obj = {
		'users': num_users,
		'orders': num_orders,
		'sales': sales
	}
	base = _page_base_info(request)
	base['general_data'] = obj
	return render(request, 'cms/index.html', base)


def _page_base_info(request):
	return {
		'user': request.user,
		'avatar': request.user.profile.avatar.url if request.user.profile.avatar else '/static/assets/i/app-icon72x72@2x.png',
	}


@login_required(login_url='/cms/login/')
def user_page(request):
	base = _page_base_info(request)
	return render(request, 'cms/users.html', base)


@require_GET
@login_required(login_url='/cms/login/')
def user_detail_page(request, user_id):
	base = _page_base_info(request)
	user = User.objects.get(pk=user_id)
	user_profile = user.profile.to_json()

	base['user_data'] = user_profile

	orders = user.usermerchandise.get_purchases()

	def parse_order(order):
		ticket = {
			"type": order.get_type(),
			"title": order.ticket_type.name,
			"id": order.ticket_type.pk,
			"cover": order.ticket_type.detail_cover.url if order.ticket_type.detail_cover else "/static/assets/i/cover.png"
		}
		if order.get_type() == 'disney':
			ticket['validity'] = order.ticket_type.validity
		elif order.get_type() == 'concert':
			ticket['time'] = order.ticket_type.time
		elif order.get_type() == 'disney':
			ticket['validity'] = order.ticket_type.validity

		this = {
			"order_number": order.order_number,
			"ticket": ticket,
			"count": order.count,
			"amount": order.get_price(),
			'purchase_date': order.order_date,
		}
		return this

	base['user_purchases'] = [parse_order(i) for i in orders]
	base['user_purchase_amount'] = user.usermerchandise.get_purchase_amount()

	promoted_users = _get_owned_users(user)
	base['promote_count'] = len(promoted_users)

	def parse_user(user_model):
		return {
			'id': user_model.pk,
			'nickname': user_model.profile.nickname,
			'phone_number': user_model.username,
			'amount': user_model.usermerchandise.get_purchase_amount()
		}

	base['user_promotes'] = [parse_user(i) for i in promoted_users]

	base['total_income'] = user.usermerchandise.get_total_income()

	try:
		if user.agentapplication.status == 0:
			base['agent_application'] = user.agentapplication.data_display()
	except:
		pass

	return render(request, 'cms/user_details.html', base)


@require_GET
@login_required(login_url='/cms/login/')
def respond_application(request):
	decision = request.GET.get('decision')
	application_id = request.GET.get('application_id')

	from registrar.models import AgentApplication
	from django.core.exceptions import ObjectDoesNotExist
	try:
		app = AgentApplication.objects.get(pk=application_id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("申请未找到")

	decision = utils.str_to_bool(decision)
	if decision:
		app.accept()
	else:
		app.decline()

	# -------- push application decision message to applicant ------
	from notifications.notifications import baidu_push
	recipient = app.user
	baidu_push(recipient=recipient, action='AgentApplication', params={
		'approved': decision,
		'trigger_user': request.user
	})

	return HttpResponse(decision)


@login_required(login_url='/cms/login/')
def purchase_page(request):
	base = _page_base_info(request)
	login_user = request.user

	orders_raw = get_owned_orders(login_user)
	orders = []
	total_income = 0
	for i in orders_raw:
		data = i.data_display()
		if login_user.is_superuser:
			withdraw_record = i.withdrawables.filter(beneficiary=i.beneficiary).first()
		else:
			withdraw_record = i.withdrawables.filter(beneficiary=login_user).first()
		if withdraw_record is None:
			data['withdraw_info'] = None
		else:
			data['withdraw_info'] = withdraw_record.data_display()
			total_income += withdraw_record.amount
		orders.append(data)

	base['order_list'] = orders
	base['total_amount'] = 0
	for i in orders_raw:
		base['total_amount'] += i.get_price()

	base['total_income'] = login_user.usermerchandise.get_total_income()

	return render(request, 'cms/orders.html', base)


@login_required(login_url='/cms/login/')
def order_detail_page(request, order_number):
	base = _page_base_info(request)

	order = TicketOrder.objects.get(order_number=order_number).get_order_object()
	base['order_info'] = order.data_display()
	if request.user.is_superuser:
		record = order.withdrawables.filter(beneficiary=order.beneficiary).first()
	else:
		record = order.withdrawables.filter(beneficiary=request.user).first()
	if record is None:
		base['withdraw_info'] = None
	else:
		base['withdraw_info'] = record.data_display()

	return render(request, 'cms/order.html', base)


@require_GET
@login_required(login_url='/cms/login/')
def moments_page(request):
	base = _page_base_info(request)

	from moments.models import Post
	import json
	moment_model_list = Post.objects.all().order_by('-date')
	moment_data_list = [i.to_json() for i in moment_model_list]
	for i in moment_data_list:
		time = i['publish_time']
		i['publish_time'] = time.strftime("%Y年%m月%d日, %H时%M分%S秒")
		i['json_str'] = json.dumps(i)

	base['list'] = moment_data_list

	return render(request, 'cms/moments.html', base)


@login_required(login_url='/cms/login/')
def toggle_moment_display(request, id):
	display = request.POST.get('display')
	from moments.models import Post
	post = Post.objects.get(pk=id)
	display = utils.str_to_bool(display)
	post.display = display
	post.save()
	return HttpResponse('ok')


@login_required(login_url='/cms/login/')
def request_withdraw(request, order_number):
	order = TicketOrder.objects.get(order_number=order_number).get_order_object()
	if request.user.usermerchandise.level != 1:
		return HttpResponseForbidden("Operation not permitted")
	record = order.withdrawables.filter(beneficiary=request.user).first()
	if record is None:
		return HttpResponseNotFound("This user cannot perform the withdraw function")
	order.request_withdraw()
	return HttpResponse("OK")


@login_required(login_url='/cms/login/')
def confirm_withdraw(request, order_number):
	order = TicketOrder.objects.get(order_number=order_number).get_order_object()
	if not request.user.is_superuser:
		return HttpResponseForbidden("Operation not permitted")
	order.confirm_withdraw()
	return HttpResponse("OK")


@login_required(login_url='/cms/login/')
def disney_list(request):
	from merchandise.models import DisneyTicket
	return JsonResponse([i.to_json(False, True) for i in DisneyTicket.objects.all()], safe=False)


def disney_detail(request, id):
	from merchandise.models import DisneyTicket
	print id
	try:
		ticket = DisneyTicket.objects.get(pk=id)
	except DisneyTicket.DoesNotExist:
		return HttpResponseNotFound('disney ticket {0} cannot be found'.format(id))
	return JsonResponse(ticket.to_json(simple=False, past=True))


@login_required(login_url='/cms/login/')
def disney_listing_page(request):
	base = _page_base_info(request)
	return render(request, 'cms/disney_listing.html', base)


@require_POST
@login_required
def update_disney_inventory(request):
	disney_id = request.POST.get('id')
	date = request.POST.getlist('date[]')
	updated_inventory = request.POST.getlist('inventory[]')

	disney_ticket = DisneyTicket.objects.get(pk=disney_id)
	for i in range(len(date)):
		disney_ticket.update_inventory(date[i], updated_inventory[i])

	return HttpResponse('OK')

#add by sunming
@login_required(login_url='/cms/login/')
def scenery_list(request):
	from merchandise.models import SceneryTicket
	return JsonResponse([i.to_json(False, True) for i in SceneryTicket.objects.all()], safe=False)


def scenery_detail(request, id):
	from merchandise.models import SceneryTicket
	print id
	try:
		ticket = SceneryTicket.objects.get(pk=id)
	except SceneryTicket.DoesNotExist:
		return HttpResponseNotFound('Scenery ticket {0} cannot be found'.format(id))
	return JsonResponse(ticket.to_json(simple=False, past=True))


@login_required(login_url='/cms/login/')
def scenery_listing_page(request):
	base = _page_base_info(request)
	return render(request, 'cms/scenery_listing.html', base)


@require_POST
@login_required
def update_scenery_inventory(request):
	scenery_id = request.POST.get('id')
	date = request.POST.getlist('date[]')
	updated_inventory = request.POST.getlist('inventory[]')

	scenery_ticket = SceneryTicket.objects.get(pk=scenery_id)
	for i in range(len(date)):
		scenery_ticket.update_inventory(date[i], updated_inventory[i])

	return HttpResponse('OK')
#add end by sunming




def _get_owned_users(user):
	if user.is_superuser:
		return User.objects.all()
	children = Profile.objects.filter(promoter=user.profile).exclude(user=user)
	profiles = [i for i in children]
	for i in children:
		grandchildren = Profile.objects.filter(promoter=i).exclude(user=user)
		profiles = profiles + [i for i in grandchildren]

	return [i.user for i in profiles]


@login_required(login_url='/cms/login/')
def get_owned_users(request):
	'''
	get all users the current login account can see, in the form of User objects
	'''
	return _get_owned_users(request.user)


def get_owned_orders(user):
	if user.is_superuser:
		pass
	owned_users = _get_owned_users(user)

	orders = []
	for i in owned_users:
		orders += i.usermerchandise.get_purchases()
	return orders


def get_withdrawable_orders(user):
	orders = get_owned_orders(user)
	withdrawable = []
	for i in orders:
		if i.beneficiary == user:
			withdrawable.append(i)
	return withdrawable


@require_GET
@login_required(login_url='/cms/login/')
def get_user_list(request):
	user_model_list = get_owned_users(request)

	data_list = []
	for i in user_model_list:
		data = i.profile.to_json()
		data['amount'] = i.usermerchandise.get_purchase_amount()
		data_list.append(data)

	return JsonResponse(data_list, safe=False)


def batch_create_users(user_list, promoter):
	from vip.utils import create_user
	for i in user_list:
		user_model = create_user(i['phone_number'])
		if user_model is False:
			continue
		user_model.profile.nickname = i['nickname']
		if 'gender' in i:
			user_model.profile.gender = i['gender']
		user_model.profile.create_promotion_code(number=5)
		user_model.profile.promoter = promoter
		user_model.profile.save()
		user_model.usermerchandise.level = promoter.user.usermerchandise.level + 1
		user_model.usermerchandise.save()


def get_raw_data(workbook):
	sheet = workbook.active
	row_number = len(sheet.rows)
	raw = []
	for i in range(1, row_number):
		current_row = sheet.rows[i]
		tp = (current_row[0].value, current_row[1].value, current_row[2].value)
		raw.append(tp)
	return raw


@require_POST
@login_required(login_url='/cms/login/')
def upload_import_file(request):
	try:
		user_file = request.FILES['users']
	except KeyError:
		return HttpResponseNotFound('File \'user\' not found')
	from openpyxl import load_workbook
	try:
		workbook = load_workbook(user_file)
	except:
		return HttpResponseBadRequest("请上传正确格式Excel文件")
	raw_data = get_raw_data(workbook)

	user_list = []
	for row in raw_data:
		(phone, name, gender) = row
		if phone is None:
			continue
		obj = {
			'phone_number': phone,
			'nickname': name if name is not None else ''
		}
		if gender is not None and gender in ['M', 'F']:
			obj['gender'] = gender
		user_list.append(obj)
	request.session['imports'] = user_list

	return JsonResponse(user_list, safe=False)


@require_POST
@login_required(login_url='/cms/login/')
def import_users(request):
	batch_create_users(request.session['imports'], request.user.profile)
	return HttpResponse("OK")


def user_login(request):
	if request.method == 'GET':
		return render(request, 'cms/login_.html')
	else:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('cms:index')
			else:
				return HttpResponseBadRequest("Login unsuccessful")

		return HttpResponseNotFound("User does not exist")


@login_required(login_url='/cms/login/')
def user_logout(request):
	logout(request)
	return redirect('cms:login')
