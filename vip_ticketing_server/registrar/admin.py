# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *
from merchandise.models import UserMerchandise

admin.site.unregister(User)

class UserCreationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'is_staff')


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['promoter', 'gender', 'nickname', 'labels', 'avatar', 'emchatuser','emchatpd',]


class ProfileInline(admin.StackedInline):
	model = Profile
	form = ProfileForm


class UserMerchandiseInline(admin.StackedInline):
	model = UserMerchandise


def generate_promotion_code(modeladmin, request, queryset):
	for user in queryset:
		user.profile.create_promotion_code(5)


generate_promotion_code.short_description = "为选中用户添加邀请码"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	actions = [generate_promotion_code, ]
	inlines = (ProfileInline, UserMerchandiseInline,)
	add_form = UserCreationForm
	add_fieldsets = [
		(None, {'fields': (
			'username',
		),}),
		("Permissions", {
			'fields': (
				'is_staff',

			)
		})
	]
	fieldsets = [
		(None, {'fields': (
			'username',
			'password',
		),}),
		("Permissions", {
			'fields': (
				'is_staff',
				'user_permissions',
				'groups'
			)
		})
	]
	list_display = ('phone_number', 'nickname', 'gender', 'is_agent', 'level')

	def level(self, instance):
		return instance.usermerchandise.get_level_display()

	def phone_number(self, instance):
		return instance.username

	phone_number.short_description = '手机号'

	def nickname(self, instance):
		return instance.profile.nickname

	nickname.short_description = '昵称'

	def gender(self, instance):
		return instance.profile.get_gender_display()

	gender.short_description = '性别'

	def is_agent(self, instance):
		gp = instance.groups.filter(name='代理')
		return len(gp) > 0

	is_agent.short_description = '代理'
	is_agent.boolean = True


@admin.register(Promotion)
class PromotionCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'valid', 'owner')
	list_filter = ('valid', 'owner')


@admin.register(UserLabel)
class UserLabelAdmin(admin.ModelAdmin):
	list_display = ['text', 'short', 'category']


# Register your models here.
admin.site.register(UserLabelCategory)

@admin.register(AgentApplication)
class AgentApplicationAdmin(admin.ModelAdmin):
	list_display = ['user', 'status', 'applied_time']

# admin.site.register(UserLabel)
# admin.site.register(PIN)
