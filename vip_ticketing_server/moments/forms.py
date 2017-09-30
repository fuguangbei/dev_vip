from django import forms
from models import *

class MomentsBannerForm(forms.Form):
	banner = forms.ImageField()