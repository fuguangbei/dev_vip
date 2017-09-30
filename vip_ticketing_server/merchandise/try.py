from merchandise.models import *
o1 = DisneyOrder.objects.all()[0]
u = o1.purchaser
# print DisneyOrder._meta.get_field_by_name('purchaser')[0].related_query_name()
print o1.create_order_number()
ticket = DisneyTicket.objects.all()[1]
print ticket.pk
o2 = DisneyOrder(ticket_type=ticket)
print o2.create_order_number()