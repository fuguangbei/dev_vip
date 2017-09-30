from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='register'),
    url(r'^signup/', views.signup),
    url(r'^success/', views.landing),
    url(r'^login/$', views.login),
    url(r'^login/pin/(?P<phone>\d+)', views.get_pin),
    url(r'^login/pin/ethan/', views.get_master_pin),
]