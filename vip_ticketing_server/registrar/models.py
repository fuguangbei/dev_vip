#-*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models
import vip.settings as settings
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.utils.crypto import get_random_string
from forms import *
from PIL import Image
import vip.utils as utils

APPLICATION_STATES = (
	(-1, '申请拒绝'),
	(0, '等待审核'),
	(1, '申请成功'),
)


@python_2_unicode_compatible
class UserLabelCategory(models.Model):
	class Meta:
		verbose_name = u'用户标签种类'
		verbose_name_plural = u'用户标签种类'

	text = models.CharField(max_length=30, verbose_name='全称')
	short = models.CharField(max_length=20, verbose_name='简称')
	allow_multiple = models.BooleanField(verbose_name='允许多选', default=False)

	def __str__(self):
		return "{0} ({1})".format(self.text, self.short)

	def get_labels(self):
		labels = UserLabel.objects.filter(category__pk=self.pk)
		return labels

	def to_json(self):
		labels = []
		for i in self.get_labels():
			tmp = i.to_json()
			del tmp['category']
			labels.append(tmp)

		this = {
			'id': self.pk,
			'text': self.text,
			'name': self.short,
			'labels': labels
		}
		return this

@python_2_unicode_compatible
class UserLabel(models.Model):
	class Meta:
		verbose_name = u'用户标签'
		verbose_name_plural = u'用户标签'

	text = models.CharField(max_length=30, verbose_name='全称')
	short = models.CharField(max_length=20, verbose_name='简称')
	category = models.ForeignKey(
		UserLabelCategory,
		on_delete=models.CASCADE,
		related_name='labels'
	)

	def __str__(self):
		return "{0} ({1})".format(self.text, self.short)

	def to_json(self):
		this = {
			'id': self.pk,
			'category': {
				'id': self.category.pk,
				'text': self.category.text,
				'name': self.category.short
			},
			'text': self.text,
			'name': self.short
		}
		return this

	def get_category(self):
		return self.category


@python_2_unicode_compatible
class Profile(models.Model):

	class Meta:
		verbose_name = u'用户信息'
		verbose_name_plural = u'用户信息'

	GENDER_CHOICES = (
		('M', '男'),
		('F', '女'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别', blank=True)
	nickname = models.CharField(max_length=20, verbose_name='昵称', default='')
	labels = models.ManyToManyField(UserLabel, verbose_name='用户标签', blank=True)
	promoter = models.ForeignKey("self", verbose_name='推荐人', null=True, blank=True)
	emchatuser = models.CharField(max_length=16, verbose_name='环信账号', blank=True)
	emchatpd = models.CharField(max_length=8, verbose_name='环信密码', blank=True)
	# user avatar image file will be stored in .../asssets/registrar/user_profile/{phone number}/XXX
	avatar = models.ImageField(
		verbose_name='头像', 
		null=True, blank=True, 
		upload_to=utils.get_avatar_upload_path,
		storage=utils.OverwriteStorage())

	def __str__(self):
		name = self.nickname if self.nickname else "Unknown VIP"
		return "username: {0}, nickname: {1}".format(self.user.username, name)

	def toggle_label(self, label):
		allow_multiple = label.category.allow_multiple
		if label in self.labels.all():
			self.labels.remove(label)
		else:
			if not allow_multiple:
				exclusives = self.labels.filter(category__pk=label.category.pk)
				for l in exclusives:
					self.labels.remove(l)
			self.labels.add(label)

	def get_nickname(self):
		return self.nickname if len(self.nickname) != 0 else _masked_phone_number(self.user.username)

	def get_avatar(self):
		if self.avatar:
			return self.avatar.url
		from django.contrib.staticfiles.templatetags.staticfiles import static
		return static('assets/i/defult@3x.png')

	def update_avatar(self, image):
		try:
			compressed_image = utils.compress_image(image)
		except:
			print "something went wrong when compressing the image"
			return
		self.avatar = compressed_image
		self.save()

	def is_agent(self):
		group_agents = Group.objects.get(name='代理')
		return group_agents in self.user.groups.all()

	def promote_agent(self):
		group_agents = Group.objects.get(name='代理')
		self.user.groups.add(group_agents)

	def unset_agent(self):
		group_agents = Group.objects.get(name='代理')
		group_agents.user_set.remove(self.user)

	def promotable(self):
		from django.core.exceptions import ObjectDoesNotExist
		try:
			application = self.user.agentapplication
		except ObjectDoesNotExist:
			return self.user.usermerchandise.level < 3
		return False

	def get_agent_status(self):
		if self.is_agent():
			return '是'
		from django.core.exceptions import ObjectDoesNotExist
		try:
			application = self.user.agentapplication
		except ObjectDoesNotExist:
			return "否"
		if application.status == 0:
			return "正在审核"
		return "否"

	def set_password(self, pwd=None):
		if pwd is None:
			pwd = 'qwerasdf'
		self.user.set_password(pwd)
		self.sms_password(pwd)
		self.save()

	def sms_password(self, pwd):
		phone_number = self.user.username
		if not utils.is_phone_number(phone_number):
			print "This user {0} does not have a valid phone number, \
retrieving password failed.".format(self.user)
			return

		utils.send_SMS(phone_number, settings.SMS_TEMPLATE_PWD.format(pwd))

	def to_json(self):
		this = {
			'id': self.user.pk,
			'phone_number': self.user.username,
			'nickname': self.nickname if len(self.nickname) != 0 else _masked_phone_number(self.user.username),
			'gender': self.get_gender_display(),
			'avatar': self.get_avatar(),
			'labels': [i.to_json() for i in self.get_labels()],
			'agent': self.get_agent_status(),
			'promotion': self.get_promotion(),
			'promotable': self.promotable(),
			'credits': self.user.usermerchandise.credits,
			'emchatuser': self.emchatuser,
			'emchatpd': self.emchatpd
		}

		if self.promoter:
			this['promoter'] = {
				'phone_number': self.promoter.user.username,
				'nickname': self.promoter.nickname,
				'gender': self.promoter.get_gender_display(),
				'id': self.promoter.user.pk,
			}
		else:
			this['promoter'] = {}
		return this

	def get_user_chain(self):
		chain = [self.user]
		current = self
		while current.promoter != current and current.promoter is not None:
			current = current.promoter
			chain.append(current.user)
		return chain

	def get_labels(self):
		return self.labels.all()

	def get_promotion(self):
		if self.is_agent():
			codes = Promotion.objects.filter(owner=self)
			if len(codes) == 0:
				self.create_promotion_code()
			code = Promotion.objects.filter(owner=self)[0]
			return utils.create_promotion_url(code.code)
		else:
			return [i.code for i in self.get_promotion_codes()]

	def get_promotion_codes(self, valid_only=True):
		if valid_only:
			return Promotion.objects.filter(owner=self, valid=True)
		return Promotion.objects.filter(owner=self)

	def create_promotion_code(self, number=1):
		for i in range(number):
			promocode = Promotion.create()
			promocode.owner = self
			promocode.save()


@python_2_unicode_compatible
class PIN(models.Model):
	class Meta:
		verbose_name = '手机验证码'
		verbose_name_plural = '手机验证码'

	phone_number = models.CharField(max_length=11, unique=True, verbose_name='验证手机号')
	pin = models.CharField(max_length=settings.PIN_LEN, verbose_name='验证码')
	updated_on = models.DateTimeField(auto_now=True, verbose_name='更新时间')

	def __str__(self):
		return "PIN for {0} is {1}, updated on {2}".format(self.phone_number, self.pin, self.updated_on)


@python_2_unicode_compatible
class Promotion(models.Model):
	code = models.CharField(max_length=settings.PROMOTION_CODE_LEN)
	valid = models.BooleanField(default=True)
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE,
		related_name='promotions')

	class Meta:
		verbose_name = u'邀请码'
		verbose_name_plural = u'邀请码'

	@classmethod
	def create(cls):
		while True:
			code = get_random_string(
				length=settings.PROMOTION_CODE_LEN,
				allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			if len(cls.objects.filter(code=code)) == 0:
				break
		print code
		promo = cls(code=code)
		return promo

	def __str__(self):
		return "{0}".format(self.code, "valid" if self.valid else "invalid", self.owner)


@python_2_unicode_compatible
class AgentApplication(models.Model):
	user = models.OneToOneField(
		User,
		verbose_name='用户',
		on_delete=models.CASCADE
	)
	status = models.IntegerField(
		verbose_name='申请状态',
		default=0,
		choices=APPLICATION_STATES
	)
	applied_time = models.DateTimeField(
		auto_now_add=True,
		verbose_name='申请时间'
	)

	def decline(self):
		self.status = -1
		self.save()
		self.user.profile.unset_agent()

	def accept(self):
		self.status = 1
		self.save()
		self.user.profile.set_password()
		self.user.profile.promote_agent()

	def data_display(self):
		return {
			'applied_time': self.applied_time,
			'status': self.get_status_display(),
			'id': self.pk
		}

	def __str__(self):
		return str(self.pk)


def _masked_phone_number(number):
	if utils.is_phone_number(number):
		return number[0:3] + '*' * 4 + number[7:]
	return number


class Visitor(models.Model):
	user = models.OneToOneField(User)
	session_key = models.CharField(null=True, blank=True, max_length=40)
