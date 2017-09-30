from django.conf.urls import url, include
from . import views

app_name = 'cms'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
	url(r'^users\/?$', views.user_page, name='users'),
	url(r'^users/(?P<user_id>\d+)\/?$', views.user_detail_page, name='user_detail'),
	url(r'^users/list/', views.get_user_list, name='get_user_list'),
	url(r'^users/import\/?$', views.upload_import_file),
	url(r'^users/import/confirm\/?$', views.import_users),
	url(r'^purchases\/?$', views.purchase_page, name='purchases'),
	url(r'^purchases/(?P<order_number>\d{11})/withdraw/', views.request_withdraw, name='request_withdraw'),
	url(r'^purchases/(?P<order_number>\d{11})/confirm_withdraw/', views.confirm_withdraw, name='request_withdraw'),
	url(r'^purchases/(?P<order_number>\d{11})\/?$', views.order_detail_page, name='order_details'),
	url(r'^disney\/?$', views.disney_listing_page, name='disney'),
	url(r'^disney/(?P<id>\d+)/', views.disney_detail, name='disney_ticket_detail'),
	url(r'^disney/get_list/', views.disney_list, name='disney_list'),
	url(r'^disney/update/', views.update_disney_inventory, name='update_inventory'),
	url(r'^scenery\/?$', views.scenery_listing_page, name='scenery'),
	url(r'^scenery/(?P<id>\d+)/', views.scenery_detail, name='scenery_ticket_detail'),
	url(r'^scenery/get_list/', views.scenery_list, name='scenery_list'),
	url(r'^scenery/update/', views.update_scenery_inventory, name='update_scenery_inventory'),
	url(r'^verify_application/', views.respond_application),
	url(r'^moments\/?$', views.moments_page, name='moments_page'),
	url(r'^moments/(?P<id>\d+)/verify', views.toggle_moment_display),
]