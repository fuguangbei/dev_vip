$(document).on('ready', function () {
	$('.amount').money()
	$('table').DataTable()

	$(document).on('click', 'td.user-info', function () {
		var user_id = $(this).data('target')
		window.location.href = '/cms/users/{0}'.format(user_id)
	})

	$(document).on('click', 'td.order-info', function () {
		var order_number = $(this).data('target')
		window.location.href = '/cms/purchases/{0}'.format(order_number)
	})
})