from merchandise.models import *
for i in [DisneyOrder, ConcertOrder]:
	orders = i.objects.filter(status='P')
	for order in orders:
		print "\norder number: {0}".format(order.order_number)
		order.pay_beneficiaries()

