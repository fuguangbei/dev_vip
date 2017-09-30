from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^detail/(?P<ticket_type>\w+)\/?', views.get_detail_page),
]