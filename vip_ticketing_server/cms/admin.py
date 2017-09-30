from django.contrib import admin

# Register your models here.
from cms.models import Sensitive,Feedback


@admin.register(Sensitive)
class SensitiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'words', 'added', 'time')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'submit_time', 'solved_time','is_solved')