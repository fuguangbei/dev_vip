from django.shortcuts import render
import vip.settings as settings
import os
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST
from PIL import Image


def get_detail_page(request):
	return render(request, 'explore/find-detail.html')