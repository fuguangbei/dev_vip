# coding=utf-8
from django.contrib import admin
from models import *
from django.contrib.admin import ListFilter, FieldListFilter

# Register your models here.
# admin.site.register(Post)
admin.site.register(UserMoments)
admin.site.register(MomentsComments)


def batch_enable_moments_display(modeladmin, request, queryset):
	for post in queryset:
		post.display = True
		post.save()
batch_enable_moments_display.short_description = "批量审核通过/推荐圈子"


def batch_disable_moments_display(modeladmin, request, queryset):
	for post in queryset:
		post.display = False
		post.save()
batch_disable_moments_display.short_description = "批量取消审核/推荐圈子"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	actions = [batch_enable_moments_display, batch_disable_moments_display, ]

	list_display = ('id', 'text', 'display', 'publisher', 'author', 'forwarding')

	def forwarding(self, instance):
		return not instance.author == instance.publisher

	forwarding.boolean = True
	forwarding.short_description = "是否为转发"
