from django.contrib.auth.models import User
from vip.utils import update_user

for i in User.objects.all():
	print "processing user: {0}".format(str(i))
	update_user(i)
	print "user is now ready to use"

