# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import vip.utils as utils
from datetime import date
from registrar.models import UserLabel

COUNTRIES = (
	('CN', '中国'),
	('US', '美国'),
	('CA', '加拿大'),
	('JP', '日本'),
	('KR', '韩国'),
)

PURCHASE_STATUSES = (
	('P', '已付款'),
	('N', '待付款'),
	('C', '取消交易'),
)

USER_LEVELS = (
	(1, '一级用户'),
	(2, '二级用户'),
	(3, '三级用户'),
)

RATIO = (
	(0, '0%'),
	(.1, '10%'),
	(.2, '20%'),
	(.3, '30%'),
	(.4, '40%'),
	(.5, '50%'),
)

SIGHT = (
	('potala','布达拉宫'),
	('palace','故宫')
)

@python_2_unicode_compatible
class City(models.Model):
	class Meta:
		verbose_name = '城市'
		verbose_name_plural = '城市'

	name = models.CharField(max_length=10, verbose_name='全称')
	code = models.CharField(
		verbose_name='英文名称',
		max_length=20,
	)

	country = models.CharField(
		max_length=3,
		verbose_name='国家',
		choices=COUNTRIES,
		default='CN'
	)

	def __str__(self):
		return self.name

	def to_json(self):
		this = {
			'name': self.name,
			'code': self.code,
			'id': self.pk
		}
		return this


@python_2_unicode_compatible
class Ticket(models.Model):
	class Meta:
		verbose_name = '卡'
		verbose_name_plural = '卡'

	name = models.CharField(max_length=50, verbose_name='名称')
	price = models.IntegerField(verbose_name='价格', null=True)
	available = models.IntegerField(verbose_name='剩余票数', default=0)
	caption_description = models.CharField(
		max_length=30,
		verbose_name='推荐内容描述'
	)
	caption_title = models.CharField(
		max_length=10,
		verbose_name='推荐标题描述',
	)
	listing_cover = models.ImageField(
		verbose_name='列表页封面图',
		upload_to=utils.get_ticket_listing_cover_upload_path,
		null=True,
	)
	detail_cover = models.ImageField(
		verbose_name='详情页封面图',
		upload_to=utils.get_ticket_detail_cover_upload_path,
		null=True,
	)
	related_cities = models.ManyToManyField(
		City,
		verbose_name='关联城市',
		related_name='tickets',
	)
	labels = models.ManyToManyField(
		UserLabel,
		verbose_name='关联标签',
		related_name='tickets',
		blank=True
	)
	bonus_amount = models.FloatField(
		verbose_name='提成总额',
		default=0
	)

	def get_ticket_object(self):
		result = DisneyTicket.objects.filter(pk=self.pk)
		if len(result):
			return result[0]
		result = ConcertTicket.objects.filter(pk=self.pk)
		if len(result):
			return result[0]
		result = AerospaceTicket.objects.filter(pk=self.pk)
		if len(result):
			return result[0]
		result = SceneryTicket.objects.filter(pk=self.pk)
		if len(result):
			return result[0]

	@staticmethod
	def find_type_by_id(id):
		result = AerospaceTicket.objects.filter(pk=id)
		if len(result):
			return 'aerospace'
		result = DisneyTicket.objects.filter(pk=id)
		if len(result):
			return 'disney'
		result = ConcertTicket.objects.filter(pk=id)
		if len(result):
			return "concert"
		result = SceneryTicket.objects.filter(pk=id)
		if len(result):
			return "scenery"
		return None

	@staticmethod
	def search(keywords):
		raw_results = {
			"disney": Ticket._search(DisneyTicket, keywords),
			"concert": Ticket._search(ConcertTicket, keywords),
			"aerospace": Ticket._search(AerospaceTicket, keywords),
			"scenery": Ticket._search(SceneryTicket, keywords)
		}
		results = []
		for type, model_list in raw_results.iteritems():
			for model_obj in model_list:
				data_rep = {
					"category": "ticket",
					"type": type,
					"id": model_obj.pk,
					"title": model_obj.name
				}
				results.append(data_rep)
		return results

	@staticmethod
	def _search(model_class, keywords):
		'''
		returns a list of model instances of the given model class which contains the given keywords
		:param model_class: the actual model class
		:param keywords: a list of keywords, in unicode
		:return: a list of model instances
		'''
		result_model_list = []
		for kw in keywords:
			result = model_class.objects.filter(name__contains=kw)
			result_model_list += result
		return result_model_list

	def __str__(self):
		return self.name


class AerospaceTicket(Ticket):
	class Meta:
		verbose_name = '宇航套餐'
		verbose_name_plural = '宇航套餐'

	intro = RichTextUploadingField(
		verbose_name='套餐介绍',
		blank=True,
	)
	purchase_notes = RichTextUploadingField(
		verbose_name='购买须知',
		null=True,
		blank=True
	)

	def to_json(self, simple=True):
		this = {
			'type': 'aerospace',
			'id': self.pk,
			'title': self.name,
			'listing_cover': self.listing_cover.url if self.listing_cover else '',
			'caption_title': self.caption_title,
			'caption_description': self.caption_description
		}
		detail = {
			'detail_cover': self.detail_cover.url if self.detail_cover else '',
			'price': self.price,
			'package_introduction': self.intro,
			'purchase_notes': self.purchase_notes
		}
		if not simple:
			this.update(detail)
		return this


@python_2_unicode_compatible
class DisneyTicket(Ticket):
	class Meta:
		verbose_name = '迪士尼公园卡'
		verbose_name_plural = '迪士尼公园卡'

	# start_date = models.DateField(verbose_name='起始日期', default=date.today)
	validity = models.DateField(null=True, blank=True, verbose_name='有效期')
	vip_channel = RichTextUploadingField(
		verbose_name='VIP通道',
		null=True,
		blank=True)
	purchase_notes = RichTextUploadingField(
		verbose_name='购买须知',
		null=True,
		blank=True
	)
	intro = RichTextUploadingField(
		verbose_name='套餐介绍',
		null=True,
		blank=True
	)
	entry_notes = models.TextField(verbose_name='入场须知', blank=True)
	pickup_rate = models.FloatField(verbose_name='接送价格', default=0)

	def __str__(self):
		return self.name

	def get_total_inventory(self):
		total = 0
		for i in self.schedules.all():
			total += i.inventory
		return total

	def to_json(self, simple=True, past=False):
		this = {
			'type': 'disney',
			'id': self.pk,
			'title': self.name,
			'listing_cover': self.listing_cover.url if self.listing_cover else '',
			'caption_title': self.caption_title,
			'caption_description': self.caption_description
		}

		schedule_model_queryset = DisneySchedule.objects.filter(ticket=self, inventory__gt=0)
		from django.utils.timezone import datetime
		now = datetime.now().date()

		if past:
			schedule_data = [i.data_display() for i in schedule_model_queryset]
		else:
			schedule_data = [i.data_display() for i in schedule_model_queryset if i.date >= now]

		detail = {
			'remaining': self.get_total_inventory(),
			'detail_cover': self.detail_cover.url if self.detail_cover else '',
			'price': self.price,
			'vip_channel': self.vip_channel,
			'purchase_notes': self.purchase_notes,
			'package_introduction': self.intro,
			'entry_notes': self.entry_notes,
			'schedule': schedule_data,
			# 'start_date': self.start_date
		}
		if not simple:
			this.update(detail)
		return this

	def update_inventory(self, date, number):
		schedules = self.schedules.all()
		from datetime import datetime
		current = datetime.strptime(date, '%Y-%m-%d')
		for i in schedules:
			if current.date() == i.date:
				i.inventory = number
				i.save()
				return
		DisneySchedule.objects.create(ticket=self, date=current.date(), inventory=number)


@python_2_unicode_compatible
class DisneySchedule(models.Model):
	class Meta:
		verbose_name = '迪士尼时间表'
		verbose_name_plural = '迪士尼时间表'

	ticket = models.ForeignKey(
		DisneyTicket,
		on_delete=models.CASCADE,
		verbose_name='商品',
		related_name='schedules'
	)
	date = models.DateField(verbose_name='日期')
	inventory = models.IntegerField(
		verbose_name='余票量'
	)

	def data_display(self):
		return {
			'id': self.pk,
			'date': self.date,
			'count': self.inventory
		}

	def __str__(self):
		return str(self.date)


@python_2_unicode_compatible
class ConcertTicket(Ticket):
	class Meta:
		verbose_name = '演唱会卡'
		verbose_name_plural = '演唱会卡'

	time = models.DateTimeField(null=True, blank=True, verbose_name='时间')
	location = models.CharField(max_length=50, verbose_name='地点')
	seat = models.CharField(max_length=20, verbose_name='观演位置', default='11号包厢 (任意位置落座)')
	vip_seating = RichTextUploadingField(
		verbose_name='VIP专座',
		blank=True,
		null=True
	)
	purchase_notes = RichTextUploadingField(
		verbose_name='购买须知',
		null=True,
		blank=True
	)
	intro = RichTextUploadingField(
		verbose_name='演出介绍',
		blank=True,
		null=True
	)
	entry_notes = models.TextField(verbose_name='入场须知', blank=True)

	def __str__(self):
		return self.name

	def to_json(self, simple=True):
		brief = {
			'type': 'concert',
			'id': self.pk,
			'title': self.name,
			'time': self.time,
			'remaining': self.available,
			'listing_cover': self.listing_cover.url if self.listing_cover else '',
			'caption_title': self.caption_title,
			'caption_description': self.caption_description
		}
		detail = {
			'detail_cover': self.detail_cover.url if self.detail_cover else '',
			'location': self.location,
			'price': self.price,
			'vip_seating': self.vip_seating,
			'purchase_notes': self.purchase_notes,
			'performance_introduction': self.intro,
			'seat': self.seat,
			'entry_notes': self.entry_notes
		}
		if not simple:
			brief.update(detail)
		return brief


@python_2_unicode_compatible
class SceneryTicket(Ticket):
	class Meta:
		verbose_name = '景区卡'
		verbose_name_plural = '景区卡'

	validity = models.DateField(null=True, blank=True, verbose_name='有效期')
	purchase_notes = RichTextUploadingField(
		verbose_name='购买须知',
		null=True,
		blank=True
	)
	intro = RichTextUploadingField(
		verbose_name='景点介绍',
		blank=True,
		null=True
	)
	entry_notes = models.TextField(verbose_name='入场须知', blank=True)

	sight = models.CharField(
		max_length=8,
		verbose_name='景区名称',
		choices=SIGHT,
		null=True
	)
	def __str__(self):
		return self.name


	def get_total_inventory(self):
		total = 0
		for i in self.schedules.all():
			total += i.inventory
		return total

	def to_json(self, simple=True, past=False):
		this = {
			'type': 'scenery',
			'id': self.pk,
			'title': self.name,
			'listing_cover': self.listing_cover.url if self.listing_cover else '',
			'caption_title': self.caption_title,
			'caption_description': self.caption_description
		}

		schedule_model_queryset = ScenerySchedule.objects.filter(ticket=self, inventory__gt=0)
		from django.utils.timezone import datetime
		now = datetime.now().date()

		if past:
			schedule_data = [i.data_display() for i in schedule_model_queryset]
		else:
			schedule_data = [i.data_display() for i in schedule_model_queryset if i.date >= now]

		detail = {
			'remaining': self.get_total_inventory(),
			'detail_cover': self.detail_cover.url if self.detail_cover else '',
			'price': self.price,
			'purchase_notes': self.purchase_notes,
			'package_introduction': self.intro,
			'entry_notes': self.entry_notes,
			'schedule': schedule_data,
		}
		if not simple:
			this.update(detail)
		return this

	def update_inventory(self, date, number):
		schedules = self.schedules.all()
		from datetime import datetime
		current = datetime.strptime(date, '%Y-%m-%d')
		for i in schedules:
			if current.date() == i.date:
				i.inventory = number
				i.save()
				return
		ScenerySchedule.objects.create(ticket=self, date=current.date(), inventory=number)

@python_2_unicode_compatible
class ScenerySchedule(models.Model):
	class Meta:
		verbose_name = '景区时间表'
		verbose_name_plural = '景区时间表'

	ticket = models.ForeignKey(
		SceneryTicket,
		on_delete=models.CASCADE,
		verbose_name='商品',
		related_name='schedules'
	)
	date = models.DateField(verbose_name='日期')
	inventory = models.IntegerField(
		verbose_name='余票量'
	)

	def data_display(self):
		return {
			'id': self.pk,
			'date': self.date,
			'count': self.inventory
		}

	def __str__(self):
		return str(self.date)



@python_2_unicode_compatible
class UserMerchandise(models.Model):
	class Meta:
		verbose_name = '用户商品行为'
		verbose_name_plural = '用户商品行为'

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	level = models.IntegerField(
		verbose_name='用户等级',
		choices=USER_LEVELS,
		default=3
	)

	bonus_percentage = models.FloatField(
		verbose_name='分红比例',
		choices=RATIO,
		default=0
	)

	current_city = models.ForeignKey(
		City,
		on_delete=models.CASCADE,
		verbose_name='当前城市',
		blank=True,
		null=True
		# default=City.objects.all()[0].pk
	)

	disney_likes = models.ManyToManyField(
		DisneyTicket,
		verbose_name='已收藏迪士尼门票',
		blank=True
	)

	concert_likes = models.ManyToManyField(
		ConcertTicket,
		verbose_name='已收藏演唱会门票',
		blank=True
	)

	aero_likes = models.ManyToManyField(
		AerospaceTicket,
		verbose_name='已收藏航空套餐',
		blank=True
	)

	scenery_likes = models.ManyToManyField(
		SceneryTicket,
		verbose_name='已收藏景点门票',
		blank=True
	)

	account_balance = models.FloatField(
		verbose_name='提现金额',
		default=0.0
	)

	credits = models.IntegerField(
		verbose_name='积分',
		default=0,
		blank=True
	)

	def withdraw(self, amount):
		if self.user.is_superuser:
			return False
		if self.account_balance < amount:
			return False
		if not self.user.profile.is_agent():
			return False
		self.account_balance -= amount
		return True

	def get_withdraw_rate(self):
		return self.bonus_percentage

	def toggle_like_disney(self, ticket):
		if ticket in self.disney_likes.all():
			self.disney_likes.remove(ticket)
			return "取消收藏迪士尼门票: {0}".format(ticket.name)
		else:
			self.disney_likes.add(ticket)
			return "收藏迪士尼门票: {0}".format(ticket.name)

	def toggle_like_concert(self, ticket):
		if ticket in self.concert_likes.all():
			self.concert_likes.remove(ticket)
			return "取消收藏演唱会门票: {0}".format(ticket.name)
		else:
			self.concert_likes.add(ticket)
			return "已收藏演唱会门票: {0}".format(ticket.name)

	def toggle_like_aero(self, ticket):
		if ticket in self.aero_likes.all():
			self.aero_likes.remove(ticket)
			return "取消收藏宇航套餐: {0}".format(ticket.name)
		else:
			self.aero_likes.add(ticket)
			return "已收藏宇航套餐: {0}".format(ticket.name)

	def toggle_like_scenery(self, ticket):
		if ticket in self.scenery_likes.all():
			self.scenery_likes.remove(ticket)
			return "取消收藏景点门票: {0}".format(ticket.name)
		else:
			self.scenery_likes.add(ticket)
			return "已收藏景点门票: {0}".format(ticket.name)

	def get_purchases(self):
		disney_orders = self.disneyorders.filter(status='P')
		concert_orders = self.concertorders.filter(status='P')
		scenery_orders = self.sceneryorders.filter(status='P')
		return [i for i in disney_orders] + [i for i in concert_orders] + [i for i in scenery_orders]

	def get_purchase_amount(self):
		total = 0
		for i in self.get_purchases():
			total += i.get_price()
		return total

	def get_total_income(self):
		if not self.user.profile.is_agent() or self.level >= 3:
			return 0
		records = self.user.withdrawables.all()
		total = 0
		for i in records:
			total += i.amount
		return total

	def __str__(self):
		return self.user.profile.get_nickname()


@python_2_unicode_compatible
class Commercial(models.Model):
	class Meta:
		verbose_name = '广告'
		verbose_name_plural = '广告'

	def __str__(self):
		return self.link.name

	cover = models.ImageField(
		verbose_name='封面',
		upload_to=utils.get_commercial_upload_path,
		blank=True
	)
	display = models.BooleanField(
		verbose_name='是否显示',
		default=False
	)
	link = models.OneToOneField(
		Ticket,
		verbose_name='关联商品'
	)

	# get the commercial corresponding ticket type
	def get_link_type(self):
		query_set = DisneyTicket.objects.filter(pk=self.link.pk)
		if len(query_set):
			self.ticket = query_set[0]
			return 'disney'
		query_set = ConcertTicket.objects.filter(pk=self.link.pk)
		if len(query_set):
			self.ticket = query_set[0]
			return 'concert'
		query_set = AerospaceTicket.objects.filter(pk=self.link.pk)
		if len(query_set):
			self.ticket = query_set[0]
			return "aerospace"
		query_set = SceneryTicket.objects.filter(pk=self.link.pk)
		if len(query_set):
			self.ticket = query_set[0]
			return "scenery"
		return 'generic'

	def to_json(self):
		ticket_type = self.get_link_type()
		this = {
			'type': ticket_type,
			'id': self.ticket.pk
		}
		if self.cover:
			this['cover'] = self.cover.url
		else:
			this['cover'] = self.ticket.to_json()['listing_cover']
		return this


@python_2_unicode_compatible
class TicketOrder(models.Model):
	class Meta:
		verbose_name = '商品订单'
		verbose_name_plural = '商品订单'

	'''
	订单号由11位数字组成: TKYYMMDDXYZ
	TK: 表示票种, 两位数字00到99, 用票种的id组成
	YY, MM, DD: 订票日期
	XYZ: 当天该票种的第几张票
	'''
	order_number = models.CharField(max_length=11, verbose_name='订单号')
	count = models.IntegerField(verbose_name='数量')
	order_date = models.DateField(auto_now_add=True, null=True)

	"""P: paid, N: not paid, C: cancelled"""
	status = models.CharField(choices=PURCHASE_STATUSES, max_length=1, verbose_name='付款状态', default='N')
	contact = models.CharField(max_length=11, verbose_name='联系电话', null=True)
	transaction_info = models.TextField(verbose_name='银联交易信息', blank=True)
	beneficiary = models.ForeignKey(
		User,
		verbose_name='受益人',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)

	def get_payees(self):
		chain = self.purchaser.user.profile.get_user_chain()
		payees = []
		for i in chain:
			if not i.profile.is_agent() or i.usermerchandise.level >= 3:
				continue
			payees.append(i)
		return payees

	def save(self, *args, **kwargs):
		ptr = self.purchaser.user
		while True:
			if ptr.usermerchandise.level == 1:
				break
			ptr = ptr.profile.promoter.user
		self.beneficiary = ptr
		super(TicketOrder, self).save(*args, **kwargs)

	def __str__(self):
		return self.order_number

	def save_transaction_info(self, data):
		self.transaction_info = data
		self.save()

	def get_price(self):
		return self.ticket_type.price * self.count

	def create_order_number(self):
		TK = self.ticket_type.pk
		YY, MM, DD = date.today().year % 100, date.today().month, date.today().day
		COUNT = len(self.__class__.objects.filter(ticket_type=self.ticket_type, order_date=date.today()))
		self.order_number = str(TK).zfill(2) + str(YY).zfill(2) + str(MM).zfill(2) + str(DD).zfill(2) + str(
			COUNT).zfill(3)
		return self.order_number

	def confirm_transaction(self):
		if self.status != 'N':
			return False
		self.status = 'P'
		self.pay_beneficiaries()
		self.purchaser.credits += int(self.get_price() // 100)
		self.save()
		return True

	def pay_beneficiaries(self):
		beneficiaries = self.get_payees()
		total_bonus_amount = self.ticket_type.bonus_amount * self.count
		for i in beneficiaries:
			rate = i.usermerchandise.get_withdraw_rate()
			if i.usermerchandise.level != 1:
				bonus = total_bonus_amount * rate
			else:
				bonus = total_bonus_amount
			duplicate = WithdrawRecord.objects.filter(order=self, beneficiary=i)
			if len(duplicate) > 0:
				print "Entry already exists"
				continue
			print "Creating withdraw record for {0} in the amount of {1} yuan".format(
				i.profile.nickname,
				bonus
			)
			WithdrawRecord.objects.create(
				order=self,
				beneficiary=i,
				amount=bonus,
				status=-1
			)

	def request_withdraw(self):
		withdraw_records = self.withdrawables.all()
		for i in withdraw_records:
			if i.status != -1:
				continue
			i.request_withdraw()

	def confirm_withdraw(self):
		withdraw_records = self.withdrawables.all()
		for i in withdraw_records:
			if i.status != 0:
				continue
			i.withdraw()

	def cancel_transaction(self):
		if self.status != 'N':
			return False
		self.status = 'C'

		if self.get_type() == 'disney' or  self.get_type() == 'scenery':
			self.schedule.inventory += self.count
			self.schedule.save()
		else:
			self.ticket_type.available += self.count
			self.ticket_type.save()
		self.save()
		return True

	def to_json(self):
		this = {
			'order_number': self.order_number,
			'amount': self.get_price(),
		}
		return this

	def data_display(self):
		ticket = self.ticket_type.to_json(False)
		this = {
			"ticket": ticket,
			"purchase_date": self.order_date,
			"count": self.count,
			"purchaser": {
				"id": self.purchaser.user.pk,
				"nickname": self.purchaser.user.profile.nickname
			},
			"contact_phone_number": self.contact
		}
		if self.get_type() == 'disney':
			specific = {
				"identification": self.identification,
				"pickup": self.pickup
			}
		elif self.get_type() == 'concert':
			specific = {
				"shipping_address": self.shipping_address,
				"shipping_status": "已寄出" if self.shipped else "等待寄送",
			}
			if self.shipped:
				specific['shipping_code'] = self.shipping_code
		elif self.get_type() == 'scenery':
			specific = {
				"identification": self.identification,
			}
		else:
			specific = {}

		this.update(self.to_json())
		this.update(specific)
		return this

	def get_type(self):
		type_code = self.order_number[0:2]
		return Ticket.find_type_by_id(type_code)

	def get_order_object(self):
		if self.get_type() == 'disney':
			return DisneyOrder.objects.get(pk=self.pk)
		elif self.get_type() == 'concert':
			return ConcertOrder.objects.get(pk=self.pk)
		elif self.get_type() == 'scenery':
			return SceneryOrder.objects.get(pk=self.pk)
		return None


class WithdrawRecord(models.Model):
	beneficiary = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name="受益人",
		related_name='withdrawables'
	)
	order = models.ForeignKey(
		TicketOrder,
		verbose_name='订单',
		on_delete=models.CASCADE,
		related_name='withdrawables'
	)
	withdraw_datetime = models.DateTimeField(
		verbose_name='提现时间',
		blank=True,
		null=True
	)
	apply_datetime = models.DateTimeField(
		verbose_name='申请提现时间',
		blank=True,
		null=True
	)
	status = models.IntegerField(
		default=-1,
		verbose_name='提现状态',
		choices=(
			(-1, '未提现'),
			(0, '提现申请中'),
			(1, '已提现')
		)
	)
	amount = models.FloatField(
		verbose_name='提现金额'
	)

	def data_display(self):
		this = {
			'income': self.amount,
			'status_display': self.get_status_display(),
			'status_code': self.status,
			'beneficiary': self.beneficiary.profile.to_json(),
		}
		if self.status != -1:
			this['apply_time'] = self.apply_datetime
		if self.status == 1:
			this['withdraw_time'] = self.withdraw_datetime
		return this

	def withdraw(self):
		self.status = 1
		from django.utils import timezone
		self.withdraw_datetime = timezone.now()
		self.save()

	def request_withdraw(self):
		self.status = 0
		from django.utils import timezone
		self.apply_datetime = timezone.now()
		self.save()


class DisneyOrder(TicketOrder):
	class Meta:
		verbose_name = "迪士尼门票订单"
		verbose_name_plural = "迪士尼门票订单"

	ticket_type = models.ForeignKey(
		DisneyTicket,
		related_name='orders',
		on_delete=models.CASCADE
	)
	purchaser = models.ForeignKey(
		UserMerchandise,
		related_name="%(class)ss",
		on_delete=models.CASCADE,
		verbose_name='购买人'
	)
	identification = models.CharField(verbose_name='身份证号', max_length=18)
	pickup = models.BooleanField(verbose_name='是否接送', default=False)
	schedule = models.ForeignKey(
		DisneySchedule,
		on_delete=models.CASCADE,
		verbose_name='日期',
		null=True
	)

	def get_price(self):
		pickup_fee = self.ticket_type.pickup_rate * int(self.pickup)
		return super(DisneyOrder, self).get_price() + pickup_fee


class ConcertOrder(TicketOrder):
	class Meta:
		verbose_name = "演唱会票订单"
		verbose_name_plural = "演唱会票订单"

	ticket_type = models.ForeignKey(
		ConcertTicket,
		related_name='orders',
		on_delete=models.CASCADE
	)
	shipping_address = models.CharField(
		max_length=40,
		verbose_name='收票地址',
		blank=True,
	)
	purchaser = models.ForeignKey(
		UserMerchandise,
		related_name="%(class)ss",
		on_delete=models.CASCADE
	)

	shipped = models.BooleanField(default=False, verbose_name='订单已寄出')
	shipping_code = models.CharField(max_length=30, verbose_name='快递单号', blank=True)

class SceneryOrder(TicketOrder):
	class Meta:
		verbose_name = "景区门票订单"
		verbose_name_plural = "景区门票订单"

	ticket_type = models.ForeignKey(
		SceneryTicket,
		related_name='orders',
		on_delete=models.CASCADE
	)
	purchaser = models.ForeignKey(
		UserMerchandise,
		related_name="%(class)ss",
		on_delete=models.CASCADE
	)

	identification = models.CharField(verbose_name='身份证号', max_length=18)
	schedule = models.ForeignKey(
		ScenerySchedule,
		on_delete=models.CASCADE,
		verbose_name='日期',
		null=True
	)