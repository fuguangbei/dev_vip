from django.conf.urls import url, include

from . import registrar_apis
from . import merchandise_apis
from . import explore_apis
from . import universal_apis
from . import moments_apis
from . import notifications_apis
from . import feedback_apis

app_name = 'api_v1'
urlpatterns = [
	url(r'^$', registrar_apis.index),

	# universal
	url(r'^search\/?$', universal_apis.search),
	url(r'^cities/', universal_apis.get_cities),
	url(r'^city/(?P<id>\d+)\/?', universal_apis.set_city),
	url(r'^features/', universal_apis.feature_items, name='customized_recommendations'),

	# registrar
	url(r'^labels\/*$', registrar_apis.get_labels, name='get_all_labels'),
	url(r'^labels/(?P<id>\d+\Z)', registrar_apis.get_label_by_id, name='get_label_by_id'),
	url(r'^labels/(?P<name>\d*\D+\d*)', registrar_apis.get_labels_by_name, name='get_label_by_name'),
	url(r'^label_categories\/*$', registrar_apis.get_label_categories, name='get_label_categories'),
	url(r'^label_categories/(?P<pk>\d+\Z)', registrar_apis.get_category, name='get_category'),
	url(r'^label_categories/(?P<short>\d*\D+\d*)', registrar_apis.get_category, name='get_category'),
	url(r'^pin/(?P<phone>\d{11}\Z)', registrar_apis.get_pin, name='get_pin'),
	url(r'^signup\/*$', registrar_apis.sign_up, name='sign_up'),
	url(r'^login\/*$', registrar_apis.sign_in, name='login'),
	url(r'^logout\/*$', registrar_apis.sign_out, name='logout'),
	url(r'^profiles\/*$', registrar_apis.profiles, name='get_or_set_profiles'),
	url(r'^apply/agent\/?', registrar_apis.apply_agent,name='apply_to_an_agent'),
	url(r'^userinfo/(?P<user_id>\w*)\/*', registrar_apis.userinfo,name='user_info'),

	# merchandise
	url(r'^tickets/disney\/*$', merchandise_apis.get_disney_tickets, name='get_disney_tickets'),
	url(r'^tickets/disney/(?P<id>\d+)\/?$', merchandise_apis.get_disney_ticket, name='get_disney_ticket_by_id'),
	url(r'^tickets/disney/(?P<id>\d+)/like/$', merchandise_apis.like_disney_ticket, name='like_disney_ticket'),

	url(r'^tickets/scenery/(?P<id>\d+)\/?$', merchandise_apis.get_scenery_ticket, name='get_scenery_ticket_by_id'),
	url(r'^tickets/scenery/(?P<sight>\w*)\/*$', merchandise_apis.get_scenery_tickets, name='get_scenery_tickets'),

	url(r'^tickets/scenery/(?P<id>\d+)/like/$', merchandise_apis.like_scenery_ticket, name='like_scenery_ticket'),
	url(r'^likes/tickets/(?P<ticket_type>\w*)\/*', merchandise_apis.get_liked_tickets, name='get_liked_tickets'),
	url(r'^tickets/concert/$', merchandise_apis.get_concert_tickets, name='get_concert_tickets'),
	url(r'^tickets/concert/(?P<id>\d+)/$', merchandise_apis.get_concert_ticket, name='get_concert_ticket_by_id'),
	url(r'^tickets/concert/(?P<id>\d+)/like/', merchandise_apis.like_concert_ticket, name='like_concert_ticket'),
	url(r'^tickets/aerospace/$', merchandise_apis.get_aero_tickets, name='get_aerospace_tickets'),
	url(r'^tickets/aerospace/(?P<id>\d+)/$', merchandise_apis.get_aero_ticket, name='get_aerospace_ticket_by_id'),
	url(r'^tickets/aerospace/(?P<id>\d+)/like/', merchandise_apis.like_aero_ticket, name='like_aerospace_ticket'),
	url(r'^commercials/', merchandise_apis.get_commercials, name='get_commercial_list'),
	url(r'^tickets/(?P<ticket_type>\w*)/(?P<id>\d+)/purchase\/*$', merchandise_apis.purchase_ticket, name='purchase_ticket'),
	# transaction operations
	url(r'^orders/(?P<order_number>\d{11})/cancel\/?', merchandise_apis.cancel_order, name='cancel_order'),
	url(r'^orders\/?$', merchandise_apis.get_purchased_orders, name='get_purchased_orders'),
	url(r'^orders/(?P<order_number>\d{11})\/?$', merchandise_apis.get_order_detail, name='get_order_detail'),

	#explore
	url(r'^likes/explore\/?$', explore_apis.get_liked_post, name = 'get_liked_post'),
	url(r'^explore/posts/(?P<id>\d+)/like\/?$', explore_apis.like_post, name = 'like_a_post'),
	url(r'^explore/posts/(?P<id>\d+)/comment\/?$', explore_apis.comment_post, name = 'comment_post'),
	url(r'^explore/posts/(?P<id>\d+)/comments\/?$', explore_apis.get_comments, name = 'get_comments'),
	url(r'^explore/highlights\/?$', explore_apis.get_highlights, name='get_highlights'),
	url(r'^explore/posts\/?$', explore_apis.get_posts, name='get_posts'),
	url(r'^explore/posts/(?P<id>\d+)\/?$', explore_apis.get_post, name='get_post_by_id'),

	#moments
	url(r'^moments/post\/?$', moments_apis.publish_post, name='publish_post'),
	url(r'^moments/posts\/?$', moments_apis.get_posts, name='get_posts'),
	url(r'^moments/posts/(?P<id>\d+)\/?$', moments_apis.get_post, name='get_post_by_id'),
	url(r'^moments/myposts\/?$', moments_apis.get_current_user_moments, name='get_current_user_moments'),
	url(r'^moments/posts/(?P<id>\d+)/like\/?$', moments_apis.like_post, name='like_a_post'),
	# url(r'^likes/moments', moments_apis.get_liked_posts, name='get_liked_posts'),
	url(r'^moments/posts/(?P<id>\d+)/comment\/?$', moments_apis.comment_post, name='comment_post'),
	url(r'^moments/posts/(?P<id>\d+)/comments\/?$', moments_apis.get_comments, name='get_comments'),
	url(r'^moments/posts/(?P<id>\d+)/delete\/?$', moments_apis.delete_post, name='delete_post_by_id'),
	url(r'^moments/posts/(?P<id>\d+)/forward\/?$', moments_apis.forward_post, name='forward_post_by_id'),

	#notifications
	url(r'^notifications/device\/?$', notifications_apis.get_device_param, name='get_device_param'),
	url(r'^notifications\/?$', notifications_apis.get_notifications, name='get_notifications'),
	url(r'^notifications/notification/(?P<id>\d+)/read\/?$', notifications_apis.read_notification, name='read_notification'),
	url(r'^notifications/notification/read\/?$', notifications_apis.read_notifications, name='read_part_of_notifications'),
	url(r'^notifications/unread\/?$', notifications_apis.get_unread_count, name='get_unread_count'),
	url(r'^notifications/device/delete\/?$', notifications_apis.delete_device_param, name='delete_device_param'),
	# url(r'^notifications/share/(?P<shared_type>\w*)/(?P<shared_id>\d+)\/?$', notifications_apis.send_share_notification, name='send_share_notification'),

	#feedback
	url(r'^feedback/submit\/?$', feedback_apis.submit_feedback, name='submit_feedback')
]