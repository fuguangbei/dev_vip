jQuery.fn.extend({
	render: function (list, table_row_template_selector, reload) {
		var selector = 'table'

		return this.each(function () {
			var $this = $(this),
				template = $(table_row_template_selector).html(),
				$container = $this.find('tbody')

			if (!$this.hasClass(selector))
				return 

			if (reload)
				$container.find('tr[role=row]').remove()

			list.forEach(function (elem, index) {
				var $elem = template.template(elem)
				$container.append($elem)

				var $user_cols = $elem.find('.user-info')
				$($user_cols[0]).data('id', elem.id)
				if (elem.promoter !== null)
					$($user_cols[1]).data('id', elem.promoter.id)
			})
		})
	}
})

var load_user_list = function (reload) {
	var $box = $('#user-list > .box')

	reload = reload === undefined ? true : reload

	$box.toggle_loading_state(true)
	// request user list from server
	$.ajax({
		url: '/cms/users/list',
		type: 'get',
		success: function (user_list) {
			for (var i = 0; i < user_list.length; i++) {
				console.log(user_list[i].gender)
				if (user_list[i].promoter.nickname)
					user_list[i].promoter_name = user_list[i].promoter.nickname
				else
					user_list[i].promoter_name = "无"
				// user_list[i].is_agent_text = user_list[i].agent ? '是' : '否'
				user_list[i].is_agent_text = user_list[i].agent
			}
			$('#user-table').render(user_list, 'script#user-table-item-template', reload)
			$('#user-table').DataTable()
			$box.toggle_loading_state()
			$('.amount').money()
		},
		error: function (xhr) {
			$box.toggle_loading_state()
		}
	})

	// $box.find('table.table').DataTable()
}

var render_confirm_import_users = function (confirm_data) {
	var $modal = $('#confirm-import-users')
	var $table_container = $modal.find('table > tbody')

	$table_container.find('tr:not(.table-header)').remove()
	$modal.find('span[target=number]').html(confirm_data.length)
	
	confirm_data.forEach(function(elem, index) {
		var template = $('script#import-user-template').html(),
			$elem = template.template(elem)
		$table_container.append($elem)
	})
}





// -------------------- MAIN --------------------
$(document).on('ready', function () {
	load_user_list()

	// ---------------- GO TO USER DETAIL ---------------
	$(document).on('click', 'td.user-info', function (e) {
		var user_id = $(this).data('id')
		if (user_id === undefined)
			return 
		// go to user detail page with the user_id
		console.log(user_id)
		window.location.href = "/cms/users/{0}/".format(user_id)
	})

	// ---------------- TOOL BOXES -------------------
	var $btn_import = $('.btn.btn-app#import-users'),
		$input_import = $('#import-user-uploader'),
		$confirm_import = $('#confirm-import-users')

	$btn_import.on('click', function (e) {
		e.preventDefault()
		var $file_input = $($(this).attr('uploader'))
		$file_input.click()
	})
	$input_import.on('change', function (e) {
		var file = this.files[0]
		var form = new FormData()
		form.append('users', file)
		$.ajax({
			url: '/cms/users/import',
			type: 'post',
			processData: false,
			contentType: false,
			data: form,
			beforeSend: function (xhr, settings) {
				if (! csrfSafeMethod(settings.type) && ! this.crossDomain) {
					xhr.setRequestHeader('X-CSRFTOKEN', getCookie('csrftoken'))
				}
			},
			success: function (data) {
				render_confirm_import_users(data)
				$('#confirm-import-users').modal('show')
			},
			error: function (xhr) {
				console.log(xhr.responseText)
			}
		})
		$(this).val("")
	})
	$confirm_import.find('button#confirm').on('click', function () {
		$confirm_import.modal('hide')
		$.ajax({
			url: '/cms/users/import/confirm',
			type: 'post',
			beforeSend: function (xhr, settings) {
				if (! csrfSafeMethod(settings.type) && ! this.crossDomain) {
					xhr.setRequestHeader('X-CSRFTOKEN', getCookie('csrftoken'))
				}
			},
			success: function (data) {
				load_user_list()
			},
			error: function (xhr) {
				load_user_list()
				console.log(xhr)
			}
		})
	})
})