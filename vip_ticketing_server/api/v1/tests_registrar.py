#_*_coding:utf-8_*_
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from registrar.models import *
from django.core.urlresolvers import reverse
from registrar.forms import *
from merchandise.models import *
from explore.models import *
from moments.models import *
import moments
import explore
# from explore.models import *
from explore.models import Post
import json
from django.contrib.auth.models import User, Group
from django.core.files import File
from django.utils import timezone
import datetime
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.test import RequestFactory
from notifications.models import *

class TestCasesWithoutLogin(TestCase):
	FIXTURE_DIRS = ('api.json')
	def setup(self):
		self.client = Client()
		# self.user = UserLabel.objects.all()
		# self.usertest = UserLabel.objects.create("")
		self.client.login(username = 'admin',password = 'qwerasdf')
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.user.save()
		self.group  = Group.objects.create(name='代理')
		self.group.save()
		self.ticketorder = TicketOrder.objects.create(order_number = "01160705001",
			count = 400,
			order_date = timezone.now(),
			status = "P",
			contact = "13912345678",
			transaction_info = u"银联交易信息",
			beneficiary = self.user
			)

	def test_API1(self):
		response = self.client.get('/api/')
		self.assertEqual(response.status_code, 200)

	def test_API2(self):
		response = self.client.get('/api/v1/')
		self.assertEqual(response.status_code, 200)
		self.assertIn('home page', response.content)


	#注册信息API
	def test_API1002(self):
		pin = utils.generate_pin()
		response = self.client.post('/api/v1/signup/',{'phone_number' :'13912312345','PIN':pin,'promotion':'CUTBCUWN'})
		self.assertEqual(response.content,"验证码错误, 注册失败")

	def test_API1003(self):
		pin = utils.generate_pin()
		data = {'phone_number' :'13912312345','PIN':pin}
		response = self.client.post('/api/v1/login/', data, follow = True)
		# self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content,"账号不存在/验证码错误, 登录失败")

	def test_API1004(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.user.save()
		self.client.login(username='newsposter',password='newspass')
		self.usernotifications= UserNotifications()
		self.usernotifications.user = self.user
		self.usernotifications.save()
		response = self.client.get('/api/v1/logout/',follow = True)
		self.assertEqual(response.content,"注销成功")
		self.assertEqual(response.status_code, 200)

	def test_API1005(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		group  = Group.objects.create(name='代理')
		label1 = UserLabelCategory(text = "t1",short = "s1")
		usertest1 = UserLabel(text = "t1",short = "s1",category = label1)
		profile = Profile(user = self.user,
			gender = 'M', 
			nickname = "test",
			# label = usertest1,
			promoter = None, 
			avatar = ""
			)
		response = self.client.get('/api/v1/profiles/')
		print "1005",response.content
		self.assertEqual(response.status_code,200)

	def test_API1006(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		label1 = UserLabelCategory(text = "t1",short = "s1")
		usertest1 = UserLabel(text = "t1",short = "s1",
			category = label1)
		profile1 = Profile(user = self.user,
			gender = 'M', 
			nickname = "test",
			# label = usertest1,
			promoter = None, 
			avatar = ""
			)
		path = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
		data  = {'label' :'1','nickname':'django','gender':'F','avatar':path}
		response = self.client.post('/api/v1/profiles/', data, follow = True)
		self.assertEqual(response.status_code,200)


	def test_API1007(self):
		self.label1 = UserLabelCategory.objects.create(text = "t1",short = "s1")
		self.label2 = UserLabelCategory.objects.create(text = "t2",short = "s2")
		self.usertest1 = UserLabel.objects.create(text = "t1",short = "s1",
			category = self.label1)
		self.usertest2 = UserLabel.objects.create(text = "t2",short = "s2",
			category = self.label1)
		self.usertest3 = UserLabel.objects.create(text = "t3",short = "s3",
			category = self.label2)
		
		response = self.client.get('/api/v1/labels/')
		jsonlist = json.loads(response.content)
		self.assertEqual(jsonlist[1]["name"],self.usertest2.short)
		self.assertEqual(response.status_code, 200)

	def test_API1008(self):
		self.label1 = UserLabelCategory.objects.create(text = "t1",short = "s1")
		self.label2 = UserLabelCategory.objects.create(text = "t2",short = "s2")
		self.usertest1 = UserLabel.objects.create(text = "t1",short = "s1",
			category = self.label1)
		self.usertest2 = UserLabel.objects.create(text = "t2",short = "s2",
			category = self.label1)
		self.usertest3 = UserLabel.objects.create(text = "t3",short = "s3",
			category = self.label2)
		response = self.client.get('/api/v1/labels/30')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/api/v1/labels/s2/')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/api/v1/labels/100/')
		self.assertEqual(response.status_code, 404)


	def test_API1009(self):
		self.label1 = UserLabelCategory.objects.create(text = "t1",short = "s1")
		self.label2 = UserLabelCategory.objects.create(text = "t2",short = "s2")
		response = self.client.get('/api/v1/label_categories/')
		jsonlist = json.loads(response.content)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(jsonlist[0]["name"],self.label1.short)
		self.assertEquals(UserLabelCategory.objects.count(), 2)

	def test_API1010(self):
		self.label1 = UserLabelCategory.objects.create(text = "t1",short = "s1")
		self.label2 = UserLabelCategory.objects.create(text = "t2",short = "s2")
		self.usertest1 = UserLabel.objects.create(text = "t1",short = "s1",
			category = self.label1)
		self.usertest2 = UserLabel.objects.create(text = "t2",short = "s2",
			category = self.label1)
		self.usertest3 = UserLabel.objects.create(text = "t3",short = "s3",
			category = self.label2)
		response = self.client.get('/api/v1/label_categories/s2/')
		self.assertEqual(response.status_code, 200)

	def test_API1011(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.citycreat1 = City.objects.create(name = u"上海", code = "shanghai", country = "CN")
		self.usermerchandise = UserMerchandise.objects.create(user = self.user,
			current_city = self.citycreat1)
		self.usermerchandise.save()
		response = self.client.get('/api/v1/apply/agent/')
		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.content,"User cannot be promoted to be an agent, error.")


	#商品API测试
	def test_API1101(self):
		self.disneyticket = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.concertticket = ConcertTicket.objects.create(time = timezone.now() + datetime.timedelta(days = 40),
			location = u'梅德赛斯奔驰中心东区',
			seat = u'11号包厢 (任意位置落座)',
			vip_seating = u'VIP专座',
			purchase_notes = u'购买须知',
			intro = u'演出介绍',
			entry_notes = u'演出介绍')
		self.aerospaceticket = AerospaceTicket.objects.create(intro = u"空中飞人",
			purchase_notes = u"听工作人员安排",
			)
		response = self.client.get('/api/v1/tickets/disney/')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/api/v1/tickets/concert/')
		self.assertEqual(response.status_code, 200)
		response = self.client.get('/api/v1/tickets/aerospace/')
		self.assertEqual(response.status_code, 200)

	def test_API1102(self):
		self.disneyticket = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.aerospaceticket1 = AerospaceTicket.objects.create(pk=1
			)
		self.aerospaceticket2 = AerospaceTicket.objects.create(pk=2
			)
		self.aerospaceticket3 = AerospaceTicket.objects.create(pk=3
			)
		response = self.client.get('/api/v1/tickets/aerospace/1/')
		self.assertEqual(response.status_code, 200)
	# 	# data = json.loads(response.content)

	def test_API1103(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		for i in range(10):
			disneyticket = DisneyTicket(validity = timezone.now() + datetime.timedelta(days = 45),
				vip_channel = u'VIP通道',
				purchase_notes =u'购买须知',
				intro = u'套餐介绍',
				entry_notes = u'入场须知',
				pickup_rate = 100.0
					)
			disneyticket.save()
		response = self.client.get('/api/v1/tickets/disney/8/like/')
		self.assertEqual(response.content,"找不到迪士尼门票8")

	def test_API1104(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.citycreat1 = City.objects.create(name = u"上海", code = "shanghai", country = "CN")
		self.usermerchandise = UserMerchandise.objects.create(user = self.user,
			current_city = self.citycreat1)
		disneyticket = DisneyTicket(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 100.0
				)
		self.client.get('/api/v1/tickets/disney/1/like/')
		response = self.client.get('/api/v1/likes/tickets/')
		self.assertEqual(response.status_code, 200)

	def test_API1105(self):
		self.ticket1 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 2,
			caption_description = u"冰雪奇缘迪斯尼VIP专属通道",
			caption_title = u"狮子王套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.ticket1.save()
		self.ticket2 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 3,
			caption_description = u"冰雪奇缘通道",
			caption_title = u"辛巴套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.ticket2.save()
		self.commercial = Commercial.objects.create(cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			display = False,
			link = self.ticket1
			)
		response = self.client.get('/api/v1/commercials/')
		# print response.to_json()
		data = json.loads(response.content)
		self.assertEqual(response.status_code, 200)

	def test_API1106(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		ticket = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 2,
			caption_description = u"冰雪奇缘迪斯尼VIP专属通道",
			caption_title = u"狮子王套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		ticket.save()
		response = self.client.get('/api/v1/tickets/disney/22/purchase/')
		self.assertEqual(response.status_code, 200)

	def test_API1107(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		response = self.client.post('/api/v1/orders/01160705001/cancel/')
		self.assertEqual(response.status_code, 200)

	def test_API1108(self):
		self.ticket1 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 2,
			caption_description = u"冰雪奇缘迪斯尼VIP专属通道",
			caption_title = u"狮子王套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.ticket1.save()
		self.ticket2 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 3,
			caption_description = u"冰雪奇缘通道",
			caption_title = u"辛巴套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.ticket2.save()
		self.disneyticket = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		response = self.client.get('/api/v1/search/?q=通道')
		pdata = json.loads(response.content)
		self.assertEqual(response.status_code, 200)

	def test_API1109(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.citycreat1 = City.objects.create(name = u"上海", code = "shanghai", country = "CN")
		self.usermerchandise = UserMerchandise.objects.create(user = self.user,
			current_city = self.citycreat1)
		self.ticket = {
			"type": "disney",
			"title": "disney",
			"id": 01160705001,
			"cover":"/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
		}
		self.ticketorder = TicketOrder(order_number = "01160705001",
			count = 2,
			order_date = timezone.now(),
			status = "P",
			contact = "13912345678",
			transaction_info = u"银联交易信息",
			beneficiary = self.user
			)
		response = self.client.get('/api/v1/orders/')
		self.assertEqual(response.status_code, 200)

	# 发现API测试
	def test_API1110(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.ticketorder = TicketOrder(order_number = "01160705001",
			count = 200,
			order_date = timezone.now(),
			status = "P",
			contact = "13912345678",
			transaction_info = u"银联交易信息",
			beneficiary = self.user
			)
		response = self.client.get('/api/v1/orders/01160705001')
		self.assertEqual(response.status_code, 200)

	def test_API1201(self):
		self.post = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
			banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			caption_title = "玩转香港迪斯尼乐园",
			caption_description = "香港迪斯尼乐园占地有120公顷",
			# date = timezone.now(),
			content = "虽然面积也不算太大"
			)
		self.post.save()
		highlight = Highlight(cover_image = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			link = self.post, display = True)
		highlight.save()
		response = self.client.get('/api/v1/explore/highlights/')
		self.assertEqual(response.status_code, 200)

	# def test_API1201(self):
 #        # from explore.models import Post,Highlight

	# 	explore_post = explore.models.Post()
	# 	explore_post.title='迪士尼乐园一日游详尽攻略'
	# 	explore_post.banner='explore/posts/7/banner_A7lzAKM.png'
	# 	explore_post.caption_title='默认标题'
	# 	explore_post.caption_description='默认描述.'
	# 	explore_post.content="虽然面积也不算太大"
	# 	explore_post.save()

	# 	explore_highlight = explore.models.Highlight()
	# 	explore_highlight.cover_image = ''
	# 	explore_highlight.link = explore_post
	# 	explore_highlight.display = True
	# 	explore_highlight.save()

		# url = reverse('api/v1/explore/highlights/', args=())
		# response = self.client.get('/api/v1/explore/highlights/')
		# print response.content
		# print response.context
		# self.assertEqual(response.status_code, 200)

	def test_API1202(self):
		for i in range(1000):
			i = i+1
			self.post = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
				banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
				caption_title = "玩转香港迪斯尼乐园",
				caption_description = "香港迪斯尼乐园占地有120公顷",
				# date = timezone.now(),
				content = "虽然面积也不算太大"
				)
		response = self.client.get('/api/v1/explore/posts/?p=1')
		self.assertEqual(response.status_code, 200)

	def test_API1203(self):
		for i in range(1000):
			i = i+1
			self.post = explore.models.Post.objects.create(pk = i)
		response = self.client.get('/api/v1/explore/posts/1/')
		data = json.loads(response.content)
		self.assertEqual(response.status_code,200)
		response = self.client.get('/api/v1/explore/posts/1001/')
		self.assertEqual(response.status_code,404)

	def test_API1204(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		for i in range(100):
			i = i+1
			self.post = explore.models.Post.objects.create(pk = i)
		response = self.client.get('/api/v1/explore/posts/2/like/')
		self.assertEqual(response.status_code,200)
		response = self.client.get('/api/v1/explore/posts/2/like/')
		self.assertEqual(response.status_code,200)
		response = self.client.get('/api/v1/explore/posts/2698/like/')
		self.assertEqual(response.status_code,404)

	def test_API1205(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		# for i in range(1000):
		# 	i = i+1
		# post = explore.models.Post.objects.create(pk = 1)
		post = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
			banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			caption_title = "玩转香港迪斯尼乐园",
			caption_description = "香港迪斯尼乐园占地有120公顷",
			date = timezone.now(),
			content = "虽然面积也不算太大"
			)
		self.userexplore = UserExplore()
		self.userexplore.user = self.user
		# self.userexplore.explore_likes = post
		self.userexplore.save()
		response = self.client.get('/api/v1/likes/explore/')
		self.assertEqual(response.status_code,200)


	def test_API1206(self):
		self.post = explore.models.Post.objects.create(pk = 1)
		response = self.client.post('/explore/posts/1/comment/',{'text':'haha'})
		self.assertEqual(response.status_code,200)

	def test_API1207(self):
		self.user = User.objects.create(pk =1)
		self.post = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
			banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			caption_title = "玩转香港迪斯尼乐园",
			caption_description = "香港迪斯尼乐园占地有120公顷",
			date = timezone.now(),
			content = "虽然面积也不算太大"
			)
		for i in range(1000):
			self.moments = ExploreComments(publish_time = timezone.now(), 
				content = "zhouwu",
				corresponding_post = self.post,
				corresponding_user = self.user
				)
		response = self.client.get('/explore/posts/1/comments/')
		self.assertEqual(response.status_code,200)

	# #圈子API测试
	def test_API1301(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		from django.contrib.staticfiles import finders
		result = finders.find('assets/i/30@3x.png')
		searched_locations = finders.searched_locations
		# with open(result, 'rb') as fp:
		for i in range(1000):
			response = self.client.post('/api/v1/moments/post/', {'text': 'test20160623112332'},follow =True)
		# json_resp = json.loads(response.content)
		self.assertEqual(response.status_code,200)
		# self.assertTrue('thumbnail_url' in json_resp)
		# self.assertEquals(len(json_resp), 2)

	def test_API1302(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		for i in range(10):
			post = moments.models.Post(
				text = "test20160630",
				banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
				date = timezone.now(),
				publisher = self.user,
				author = self.user,
				forward_notes = u'转发文字',
				display = True
				)
		response = self.client.get('/api/v1/moments/posts/?p=1')
		self.assertEqual(response.status_code,200)

	def test_API1303(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		for i in range(1000):
			i = i+1
			post = moments.models.Post(
				text = "test20160630",
				banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
				date = timezone.now(),
				publisher = self.user,
				author = self.user,
				forward_notes = u'转发文字',
				display = True
				)
		response = self.client.get('/api/v1/moments/posts/2000/')
		self.assertEqual(response.status_code,200)

	def test_API1304(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		post1 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = True
			)
		post2 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = True
			)
		post3 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = True
			)
		response = self.client.get('/api/v1/moments/posts/2/like/')
		self.assertEqual(response.status_code,200)
		response = self.client.get('/api/v1/moments/posts/2/like/')
		self.assertEqual(response.status_code,200)
		response = self.client.get('/api/v1/moments/posts/2698/like/')
		self.assertEqual(response.status_code,404)

	# def test_API1306(self):
	# 	self.user = User.objects.create_user('newsposter', 
	# 	'newsposter@news.com', 'newspass')
	# 	self.client.login(username='newsposter',password='newspass')
	# 	self.post1 = moments.models.Post(
	# 		text = "test20160630",
	# 		banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
	# 		date = timezone.now(),
	# 		publisher = self.user,
	# 		author = self.user,
	# 		forward_notes = u'转发文字',
	# 		display = False
	# 		)
	# 	self.post2 = moments.models.Post(
	# 		text = "test20160630",
	# 		banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
	# 		date = timezone.now(),
	# 		publisher = self.user,
	# 		author = self.user,
	# 		forward_notes = u'转发文字',
	# 		display = False
	# 		)
	# 	self.post3 = moments.models.Post(
	# 		text = "test20160630",
	# 		banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
	# 		date = timezone.now(),
	# 		publisher = self.user,
	# 		author = self.user,
	# 		forward_notes = u'转发文字',
	# 		display = False
	# 		)
	# 	response = self.client.post('/api/v1/moments/post/1/comment/',{'text':'test2'})
	# 	self.assertEqual(response.status_code,200)

	def test_comment_moments_api1306(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		moments_1 = None
		user = None
		moments_post_1 = moments.models.Post()
		moments_post_1.text = 'moments_post_1'
		moments_post_1.publisher = moments_post_1.author = self.user
		moments_post_1.save()

		moments_post_2 = moments.models.Post()
		moments_post_2.text = 'moments_post_2'
		moments_post_2.publisher = moments_post_2.author = self.user
		moments_post_2.save()
		try:
			moments_1 = moments.models.Post.objects.get(id=1)
			# user = User.objects.get_by_natural_key(username='newsposter')
		except ObjectDoesNotExist:
			print 'can not find moments_1'
		data = {'text': 'moments_comment_1', 'corresponding_post': moments_post_1, 'corresponding_user': self.user}
		response = self.client.post('/api/v1/moments/posts/{id}/comment/'.format(id=1), data=data)
		self.assertEquals(MomentsComments.objects.filter(corresponding_post_id=1).count(), 1)
		self.assertContains(response=response, text='评论成功', status_code=200)


	def test_API1307(self):
		self.user5 = User.objects.create(pk = 1)
		self.post1 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user5,
			author = self.user5,
			forward_notes = u'转发文字',
			display = False
			)
		self.post2 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user5,
			author = self.user5,
			forward_notes = u'转发文字',
			display = False
			)
		self.post3 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user5,
			author = self.user5,
			forward_notes = u'转发文字',
			display = False
			)
		response = self.client.get('/api/v1/moments/posts/1/comments/')
		jsonlist = json.loads(response.content)
		self.assertEqual(response.status_code,200)

	def test_API1308(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.post1 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = False
			)
		self.post2 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = False
			)
		self.post3 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = False
			)
		response = self.client.get('/api/v1/moments/posts/1/delete/')
		self.assertEqual(response.status_code,200)

	def test_API1309(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.post1 = moments.models.Post(
			text = "test20160630",
			banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
			date = timezone.now(),
			publisher = self.user,
			author = self.user,
			forward_notes = u'转发文字',
			display = True
			)
		response = self.client.post('/api/v1/moments/posts/1/forward/',{'caption':"test1309forward"})
		self.assertEqual(response.status_code,200)

    #主页API测试
	def test_API1901(self):
		self.city1 = City.objects.create(name = "shanghai",code = "SH")
		self.city2 = City.objects.create(name = "chengdu",code = "CD")
		self.city2 = City.objects.create(name = "guangzhou",code = "GZ")
		response = self.client.get('/api/v1/cities/')
		jsonlist = json.loads(response.content)
		self.assertEqual(response.status_code,200)
		self.assertEqual(jsonlist[0]['name'], self.city1.name)
		self.assertEqual(jsonlist[0]['code'], self.city1.code)
		self.assertEqual(jsonlist[0]['id'], self.city1.id)

	def test_API1902(self):
		self.disneyticket1 = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.disneyticket2 = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.disneyticket3 = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.post1 = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
			banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			caption_title = "玩转香港迪斯尼乐园",
			caption_description = "香港迪斯尼乐园占地有120公顷",
			date = timezone.now(),
			content = "虽然面积也不算太大"
			)
		self.post1.save()
		self.post2 = explore.models.Post(title = "迪士尼乐园一日游详尽攻略",
			banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			caption_title = "玩转香港迪斯尼乐园",
			caption_description = "香港迪斯尼乐园占地有120公顷",
			date = timezone.now(),
			content = "虽然面积也不算太大"
			)
		self.post2.save()
		self.city1 = City.objects.create(name = "shanghai",code = "shanghai")
		self.city2 = City.objects.create(name = "chengdu",code = "chengdu")
		self.city2 = City.objects.create(name = "guangzhou",code = "guangzhou")
		city = City.objects.get(code = 'shanghai')
		response = self.client.get('/api/v1/features/')
		print response.content
		self.assertEqual(response.status_code,200)

	def test_API1401(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		data = {
			"device_type":u'4',
			"user_id":"801235190707786080",
			"channel_id":"5194127824291972987"
			}
		response = self.client.post('/api/v1/notifications/device/', data, follow = True)
		self.assertEqual(response.status_code,200)

	def test_API1402(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.notification = Notification(
			content_type = 'Comment',
			content_id = 0,
			action = 'explore',
			triggering_user = self.user,
			target_user = self.user,
			time = timezone.now(),
			content = "test1402",
			banner = '/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png',
			is_read = True
			)
		response = self.client.get('/api/v1/notifications/')
		self.assertEqual(response.status_code,200)

	def test_API1403(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		self.user1 = User.objects.create_user('newsposter1', 
		'newsposter1@news.com', 'newspass1')
		self.client.login(username='newsposter1',password='newspass1')
		for i in range(10):
			Notification(
				content_type = 'Comment',
				content_id = i,
				action = 'explore',
				triggering_user = self.user,
				target_user = self.user1,
				time = timezone.now(),
				content = "test1403",
				banner = '/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png',
				is_read = False
				)
		response = self.client.get('/api/v1/notifications/notification/8/read/')
		self.assertEqual(response.status_code,200)

	def test_API1404(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.client.login(username='newsposter',password='newspass')
		for i in range(100):
			Notification(
				content_type = 'Comment',
				content_id = 0,
				action = 'explore',
				triggering_user = self.user,
				target_user = self.user,
				time = timezone.now(),
				content = "test1403",
				banner = '/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png',
				is_read = True
				)
		response = self.client.get('/api/v1/notifications/unread/')
		self.assertEqual(response.status_code,200)

	
	#model测试
	#registrarAPI测试
class TestCaseModel(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('newsposter', 
		'newsposter@news.com', 'newspass')
		self.user1 = User.objects.create_user('newsposter1', 
		'newsposter1@news.com', 'newspass1')
		self.user2 = User.objects.create_user('newsposter2', 
		'newsposter2@news.com', 'newspass2')
		self.user.save()
		self.user1.save()
		self.user2.save()
		self.userlabelcategory1 = UserLabelCategory.objects.create(text = "t1", 
		short = "s1", allow_multiple = False)
		self.userlabelcategory2 = UserLabelCategory.objects.create(text = "t2", 
		short = "s2", allow_multiple = False)
		self.userlabel1 = UserLabel.objects.create(text = "c1", short = "d1", category = self.userlabelcategory1)
		self.userlabel2 = UserLabel.objects.create(text = "c2", short = "d2", category = self.userlabelcategory1)
		self.userlabelcategory1.save()
		self.userlabelcategory2.save()
		self.citycreat1 = City.objects.create(name = u"上海", code = "shanghai", country = "CN")
		self.citycreat2 = City.objects.create(name = u"广州", code = "guangzhou", country = "CN")
		self.citycreat3 = City.objects.create(name = u"成都", code = "chengdu", country = "CN")
		self.citycreat1.save()
		self.citycreat2.save()
		self.citycreat3.save()
		self.client = Client()

	def test_userlabelcategory_creation(self):
		"""
		Tests that we can create a userlabel
		"""
		self.userlabelc1 = UserLabelCategory.objects.filter(pk=1)
		self.userlabelc2 = UserLabelCategory.objects.filter(pk=2)
		for i in self.userlabelc2:
			tmp = i.to_json()
			self.assertEqual(self.userlabelcategory2.text, tmp['text'])
			self.assertEqual(self.userlabelcategory2.__str__(), "{0} ({1})".format(tmp['text'], tmp['name']))

	def test_userlabel_creation(self):
		# self.userlabel1 = UserLabel.objects.create(text = "c1", short = "d1", category = self.userlabelcategory1)
		# self.userlabel2 = UserLabel.objects.create(text = "c2", short = "d2", category = self.userlabelcategory1)
		# self.assertTrue(isinstance(self.userlabel1.UserLabel)
		self.assertEqual(self.userlabel1.__str__(),"{0} ({1})".format(self.userlabel1.text, self.userlabel1.short))
		self.assertEqual(self.userlabel1.get_category().__str__(), self.userlabelcategory1.__str__())

	def test_profile_creation(self):
		self.profile = Profile.objects.create(user = self.user,
		 gender = 'M', 
		 nickname = "pf", 
		 # labels = self.userlabel1,
		 # promoter = None, 
		 # avatar = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb'))
		 )
		# print self.profile.gender

	def test_pin_creation(self):
		time = timezone.now() + datetime.timedelta(hours = 8)
		self.pin = PIN.objects.create(phone_number = 13912349876, pin = "gdfdfg", updated_on = time)
		self.assertEquals(self.pin.__str__(),str(self.pin))
		# print self.pin.updated_on

	# def test_promotion_creation(self):
	# 	self.promotion = Promotion.objects.create(code = "YOURHOHO",valid = True, ower = self.profile)
	# 	print self.promotion

	def test_post_creation(self):
		# self.post1 = moments.models.Post.objects.create(
		# 	text = "test20160630",
		# 	banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
		# 	date = timezone.now(),
		# 	publisher = self.user,
		# 	author = self.user1,
		# 	forward_notes = u'转发文字',
		# 	display = True)
		# self.post2 = moments.models.Post.objects.create(
		# 	text = "test20160631",
		# 	banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
		# 	date = timezone.now(),
		# 	publisher = self.user1,
		# 	author = self.user2,
		# 	forward_notes = u'转发文字',
		# 	display = True)
		# self.post3 = moments.models.Post.objects.create(
		# 	text = "test20160632",
		# 	banner = File(open("/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png", 'rb')),
		# 	date = timezone.now(),
		# 	publisher = self.user2,
		# 	author = self.user,
		# 	forward_notes = u'转发文字',
		# 	display = True)
		# print self.post.date
		# self.post = Post.objects.create(title = "迪士尼乐园一日游详尽攻略",
		# 	banner = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
		# 	caption_title = "玩转香港迪斯尼乐园",
		# 	caption_description = "香港迪斯尼乐园占地有120公顷",
		# 	date = timezone.now(),
		# 	content = "虽然面积也不算太大"
		# 	)
		p1 = Post.objects.create(pk = 1)
		p2 = Post.objects.create(pk = 2)
		p3 = Post.objects.create(pk = 3)
		p4 = Post.objects.create(pk = 4)
		self.assertFalse(p1.title)
		self.assertFalse(p1.banner)
		self.assertFalse(p1.caption_title)
		self.assertFalse(p1.caption_description)
		self.assertTrue(p1.date)
		self.assertFalse(p1.content)

		self.assertFalse(p2.title)
		self.assertFalse(p2.banner)
		self.assertFalse(p2.caption_title)
		self.assertFalse(p2.caption_description)
		self.assertTrue(p2.date)
		self.assertFalse(p2.content)

		self.assertFalse(p4.title)
		self.assertFalse(p4.banner)
		self.assertFalse(p4.caption_title)
		self.assertFalse(p4.caption_description)
		self.assertTrue(p4.date)
		self.assertFalse(p4.content)

	def test_city_creation(self):
		
		# print self.citycreat2.to_json()["name"]
		self.assertEquals(self.citycreat2.to_json()["name"],u"广州")

	def test_ticket_creation(self):
		self.ticket1 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 2,
			caption_description = u"冰雪奇缘迪斯尼VIP专属通道",
			caption_title = u"狮子王套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.ticket1.save()
		# print "price",self.ticket1.price

    
	def test_aerospaceticket_creation(self):
		self.aerospaceticket = AerospaceTicket.objects.create(intro = u"空中飞人",
			purchase_notes = u"听工作人员安排",
			)
		self.aerospaceticket.save()

	def test_disneyticket_creation(self):
		self.disneyticket = DisneyTicket.objects.create(validity = timezone.now() + datetime.timedelta(days = 45),
			vip_channel = u'VIP通道',
			purchase_notes =u'购买须知',
			intro = u'套餐介绍',
			entry_notes = u'入场须知',
			pickup_rate = 25
			)
		self.disneyticket.save()
		self.assertEquals(self.disneyticket.to_json()['type'],'disney')

	def test_concertticket_creation(self):
		self.concertticket = ConcertTicket.objects.create(time = timezone.now() + datetime.timedelta(days = 40),
		location = u'梅德赛斯奔驰中心东区',
		seat = u'11号包厢 (任意位置落座)',
		vip_seating = u'VIP专座',
		purchase_notes = u'购买须知',
		intro = u'演出介绍',
		entry_notes = u'演出介绍')
		self.concertticket.save()
		self.assertEquals(self.concertticket.to_json()['type'], 'concert')

	def test_usermerchandise_creation(self):
		self.usermerchandise = UserMerchandise.objects.create(user = self.user,
			current_city = self.citycreat1
			# disney_likes = self.disneyticket,
			# concert_likes = self.concertticket,
			# aero_likes = self.aerospaceticket
			)
		self.assertEquals(str(self.usermerchandise.current_city), "上海")

	def test_commercial_creation(self):
		self.ticket1 = Ticket.objects.create(name = "disney",
			price = 3888,
			available= 2,
			caption_description = u"冰雪奇缘迪斯尼VIP专属通道",
			caption_title = u"狮子王套餐",
			listing_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			detail_cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png"
			)
		self.commercial = Commercial.objects.create(cover = "/Users/test/projects/vip_ticketing/vip_ticketing_server/static/assets/i/30@3x.png",
			display = False,
			link = self.ticket1
			)

	# def test_ticketorder_creation(self):
	# 	self.ticketorder = TicketOrder.objects.create(order_number = "01160705001",
	# 		count = 400,
	# 		order_date = timezone.now(),
	# 		status = "P",
	# 		contact = "13912345678",
	# 		transaction_info = u"银联交易信息",
	# 		beneficiary = self.user1
	# 		)
	# 	print self.ticketorder.order_number
		
	def tearDown(self):
		pass




