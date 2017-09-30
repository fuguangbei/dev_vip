# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from merchandise.models import *
import random

@require_GET
@csrf_exempt
def search(request):
	'''
	universal search API from a GET request, matches the results based on the titles of the objects
	if they contain the given keywords
	:param q: keyword query, a urlencoded string of keywords, separated by +
	:param f: filter, consists of a string of words, API will only return the objects
	whose "type" field matches one of the words given
	:return: a list of dict objects as the matching items
	'''
	query = request.GET.get('q')
	if query is None:
		return HttpResponseBadRequest("参数错误")
	keywords = query.split()
	# search_result = []
	# ticket_list = Ticket.search(keywords)
	# search_result += ticket_list
	# return JsonResponse(search_result, safe=False)
	search_result = []
	ticket_list = Ticket.search(keywords)
	for i in ticket_list:
		if i not in search_result:
			search_result.append(i)
	return JsonResponse(search_result, safe=False)


@require_GET
def get_cities(request):
	model_list = City.objects.all()
	json_list = [i.to_json() for i in model_list]
	return JsonResponse(json_list, safe=False)


@require_POST
@csrf_exempt
@login_required
def set_city(request, id):
	from merchandise.models import City

	try:
		city = City.objects.get(pk=id)
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到城市{0}".format(id))

	request.user.usermerchandise.current_city = city
	request.user.usermerchandise.save()
	return HttpResponse(u"设置当前城市成功, 目前为{0}".format(city.name))


@require_GET
def feature_items(request):
	# user = request.user
	# if user.is_authenticated():
	# 	print "[API1902] getting featured items w/ login"
	# 	city = user.usermerchandise.current_city
	# 	labels = user.profile.labels.all()
	# else:
	# 	print "[API1902] getting featured items w/out login"
	# 	city = City.objects.get(code='shanghai')
	# 	labels = []
    #
	# tickets = []
	# for t in Ticket.objects.all():
	# 	probability = 0
	# 	if city in t.related_cities.all():
	# 		probability += 50
	# 	for l in labels:
	# 		if l in t.labels.all():
	# 			probability += 50 / len(labels)
	# 	tickets.append({
	# 		"t": t.get_ticket_object(),
	# 		"p": probability
	# 	})
	# def cmp(a, b):
	# 	return b['p'] - a['p']
    #
	# tickets.sort(cmp=cmp)
    #
	# # TODO: recommend explore posts based on labels
	# from explore.models import Post as Explore
	# explores = Explore.objects.all().order_by('-date')
    #
	# def explore_json(post_model):
	# 	json_data = post_model.to_json()
	# 	data = {
	# 		'type': 'explore',
	# 		'id': json_data['id'],
	# 		'title': json_data['caption_title'],
	# 		'content': json_data['caption_description'],
	# 		'cover': json_data['cover']
	# 	}
	# 	return data
    #
	# def ticket_json(ticket_model):
	# 	json_data = ticket_model.to_json(False)
	# 	data = {
	# 		"type": json_data['type'],
	# 		"id": json_data['id'],
	# 		'price': json_data['price'],
	# 		'cover': json_data['detail_cover'],
	# 		'title': json_data['caption_title'],
	# 		'content': json_data['caption_description'],
	# 	}
	# 	return data
    #
	# rec_tickets = [ticket_json(i['t']) for i in tickets[0:3]]
	# rec_exps = [explore_json(i) for i in explores[0:2]]
    #
	# for i, val in enumerate(rec_tickets):
	# 	print u"Featured ticket {0}, correlation {1}".format(val['title'], tickets[i]['p'])
    #
	# ret = rec_tickets + rec_exps
    #
	# print "[/API1902]"
	# return JsonResponse(ret, safe=False)

    #add by sunming
	tickets = []
	aerospaceticket = random.choice(AerospaceTicket.objects.all())
	concertticket = random.choice(ConcertTicket.objects.all())
	disneyticket = random.choice(DisneyTicket.objects.all())
	sceneryticket = random.choice(SceneryTicket.objects.all())
	tickets.append(aerospaceticket)
	tickets.append(concertticket)
	tickets.append(disneyticket)
	tickets.append(sceneryticket)
	random.shuffle(tickets)

	from explore.models import Post as Explore
	explores = Explore.objects.all().order_by('-date')

	def explore_json(post_model):
		json_data = post_model.to_json()
		data = {
			'type': 'explore',
			'id': json_data['id'],
			'title': json_data['caption_title'],
			'content': json_data['caption_description'],
			'cover': json_data['cover']
		}
		return data

	def ticket_json(ticket_model):
		json_data = ticket_model.to_json(False)
		data = {
			"type": json_data['type'],
			"id": json_data['id'],
			'price': json_data['price'],
			'cover': json_data['detail_cover'],
			'title': json_data['caption_title'],
			'content': json_data['caption_description'],
		}
		return data

	print tickets
	rec_tickets = [ticket_json(i) for i in tickets]
	rec_exps = [explore_json(i) for i in explores[0:1]]

	ret = rec_tickets + rec_exps
	return JsonResponse(ret, safe=False)
	#end add by sunming