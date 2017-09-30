$(document).on('ready', function () {
	$('.amount').money()
	$('#consumption').money()
	$('#withdraw').money()
	$('#table-purchases').DataTable()
	$('#table-promotes').DataTable()

	var promotes = $('#table-promotes').find('tr.clickable')
	promotes.on('click', function () {
		user_id = $(this).data('id')
		window.location.href = "/cms/users/{0}".format(user_id)
	})

	$('#table-purchases tbody tr.clickable').on('click', function () {
		order_number = $(this).data('target')
		console.log(order_number)
		window.location.href = '/cms/purchases/{0}'.format(order_number)
	})

	$('#agent-app-ac').on('click', function () {
		console.log('通过')
		verify_application($(this).data('target'), true)
		$(this).closest('div.alert').alert('close')
	})
	$('#agent-app-dc').on('click', function () {
		console.log('拒绝')
		verify_application($(this).data('target'), false)
		$(this).closest('div.alert').alert('close')
	})
})

var verify_application = function (app_id, decision) {
	$.ajax({
		url: '/cms/verify_application',
		type: 'get',
		data: {
			application_id: app_id,
			decision: decision
		},
		success: function (data) {
			console.log(data)
			window.location.reload()
		},
		error: function (xhr) {
			console.log(xhr)
			alert('审核操作失败, 请重试')
		}
	})
}