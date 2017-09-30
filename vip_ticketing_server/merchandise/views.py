#-*- coding: utf-8 -*-
import vip.settings as settings
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST
from PIL import Image

# Create your views here.

@require_GET
def get_asset(request, file_path):
	params = request.GET
	# file_path = file_path.decode('utf-8')
	path = os.path.join(settings.MEDIA_ROOT, 'tickets', file_path)

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


@require_GET
def get_detail_page(request, ticket_type):
	return render(request, "merchandise/{0}-detail.html".format(ticket_type))
