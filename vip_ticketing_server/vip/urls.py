"""vip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
import registrar.views
import merchandise.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^api/', include('api.urls')),
    url(r'^registrar/', include('registrar.urls')),
    url(r'^merchandise/', include('merchandise.urls')),
    url(r'^explore/', include('explore.urls')),
    url(r'^home\/?$', views.get_homepage),
    # HOME PAGE EXPERIMENT, CAN DELETE LATER
    url(r'^h/', views.get_homepage_temp),
    url(r'^home/index\.html', views.get_homepage_content),
    url(r'^get_iframe', views.get_iframe),
    url(r'^index\.appcache', views.get_manifest),
    url(r'^assets/registrar/(?P<file_path>.*)', registrar.views.get_asset),
    url(r'^assets/tickets/(?P<file_path>.*)', merchandise.views.get_asset),
    url(r'^assets/(?P<file_path>.*)', views.get_asset),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^require-login/', views.require_login),
    url(r'^test_logged_in/', views.test_logged_in),
    url(r'^test_post', views.test_post),
    url(r'^unionpay_callback', views.unionpay_callback),
    url(r'^cms/', include('cms.urls')),
    url(r'^alipay_return_url/', views.alipay_return_url),
    url(r'^alipay_notify_url/', views.alipay_notify_url),
    url(r'^wechat_pay_callback', views.wechat_pay_callback),
]
