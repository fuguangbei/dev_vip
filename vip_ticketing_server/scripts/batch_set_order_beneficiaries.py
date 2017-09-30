# -*- coding: utf8 -*-

from merchandise.models import *
def get_beneficiary(order):
	promoter = order.purchaser.user.profile.promoter
	while promoter is not None:
		if promoter.is_agent():
			break
		promoter = promoter.promoter
	if promoter is not None:
		order.beneficiary = promoter.user
	else:
		order.beneficiary = order.purchaser.user
	order.save()

orders = TicketOrder.objects.all()
for i in orders:
	order = i.get_order_object()
	print u"processing order: {0}".format(order.order_number)
	get_beneficiary(order)
	print u"order's beneficiary is now {0}".format(order.beneficiary)

