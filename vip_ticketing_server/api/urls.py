from django.conf.urls import url, include

from . import views

app_name = 'api'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^v1/', include('api.v1.urls')),
]