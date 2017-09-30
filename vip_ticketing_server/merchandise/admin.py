# coding=utf-8
from django.contrib import admin

from models import *

# Register your models here.
admin.site.register(ConcertTicket)
# admin.site.register(DisneyTicket)
admin.site.register(AerospaceTicket)
admin.site.register(UserMerchandise)
admin.site.register(City)
admin.site.register(Commercial)


@admin.register(DisneyTicket)
class DisneyTicketAdmin(admin.ModelAdmin):
	exclude = ('available', )


@admin.register(DisneyOrder)
class DisneyOrderAdmin(admin.ModelAdmin):
	list_display = ('order_number', 'status', 'purchaser', 'identification', 'count')


@admin.register(DisneySchedule)
class DisneyScheduleAdmin(admin.ModelAdmin):
	list_display = ('ticket', 'date', 'inventory')

@admin.register(SceneryTicket)
class SceneryTicketAdmin(admin.ModelAdmin):
	exclude = ('available', )


@admin.register(SceneryOrder)
class SceneryOrderAdmin(admin.ModelAdmin):
	list_display = ('order_number', 'status', 'purchaser', 'identification', 'count')


@admin.register(ScenerySchedule)
class SceneryScheduleAdmin(admin.ModelAdmin):
	list_display = ('ticket', 'date', 'inventory')




@admin.register(TicketOrder)
# @admin.register(DisneyOrder)
@admin.register(ConcertOrder)
class TicketOrderAdmin(admin.ModelAdmin):
	list_display = ('order_number', 'type', 'status', 'purchaser', 'count')

	def type(self, instance):
		return instance.get_type()
	type.short_description = '票种'

	def purchaser(self, instance):
		return instance.get_order_object().purchaser
	purchaser.short_description = "购买人"

@admin.register(WithdrawRecord)
class WithdrawRecordAdmin(admin.ModelAdmin):
	list_display = ('order', 'beneficiary', 'withdraw_datetime', 'status', 'amount')