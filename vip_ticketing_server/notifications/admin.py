from django.contrib import admin
from models import *
# Register your models here.
admin.site.register(UserNotifications)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'triggering_user', 'action', 'content', 'target_user', 'content_type', 'is_read')