from django import forms
from models import *

class UserAvatarForm(forms.Form):
	avatar = forms.ImageField()