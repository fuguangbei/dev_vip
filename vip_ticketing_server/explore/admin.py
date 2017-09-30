from django import forms
from django.contrib import admin

from models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(ExploreComments)
admin.site.register(UserExplore)
admin.site.register(Highlight)
