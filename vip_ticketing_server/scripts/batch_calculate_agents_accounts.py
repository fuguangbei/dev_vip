from merchandise.models import *

orders = TicketOrder.objects.all()

users = UserMerchandise.objects.all()
for i in users:
	i.account_balance = 0
	i.save()

for i in orders:
	order = i.get_order_object()
	print "processing order: {0}".format(order.order_number)
	order.pay_beneficiary()

