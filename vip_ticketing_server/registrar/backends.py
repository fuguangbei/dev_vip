from registrar.models import *
from vip import utils
from django.contrib.auth.models import User

class VIPUserAuthBackend(object):
	def authenticate(self, phone_number=None, pin=None):
		if not utils.check_pin(phone_number, pin):
			return None
		try:
			user = User.objects.get(username=phone_number)
		except User.DoesNotExist:
			return None
		utils.clean_pin(phone_number, pin)
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None