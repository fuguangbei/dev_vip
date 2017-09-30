$(document).on('ready', function () {
	$('.amount').money()

	$('.html-render').activate_html()

	$('#withdraw').on('click', function (e) {
		e.preventDefault()
		r = confirm("确认提现?")
		if (r) {
			$.ajax({
				url: window.location.href.path_join('withdraw'),
				type: 'get',
				success: function (data) {
					console.log(data)
					window.location.reload()
				},
				error: function (xhr) {}
			})
		}
	})

	$('#confirm-withdraw').on('click', function (e) {
		e.preventDefault()
		r = confirm("确认提现?")
		if (r) {
			$.ajax({
				url: window.location.href.path_join('confirm_withdraw'),
				type: 'get',
				success: function (data) {
					console.log(data)
					window.location.reload()
				},
				error: function (xhr) {}
			})
		}
	})
})