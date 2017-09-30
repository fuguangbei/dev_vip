# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from cms.models import Feedback
import vip.utils as utils
from django.views.decorators.csrf import csrf_exempt
from notifications.notifications import *


@csrf_exempt
@require_POST
@login_required
def submit_feedback(request):
    content = request.POST.get('content')
    if content is None:
        return HttpResponseBadRequest("请正确填写意见反馈")
    if utils.contains_sensitive(content):
        return HttpResponseBadRequest('意见反馈中包含敏感词')
    if len(content) > Feedback._meta.get_field('content').max_length:
        return HttpResponseBadRequest('意见反馈长度超过限制')

    try:
        new_feedback = Feedback()
        new_feedback.content = content
        new_feedback.save()
    except ValueError:
        return HttpResponseBadRequest("意见反馈参数传值有错,提交意见反馈失败")
    return HttpResponse("提交意见反馈成功")