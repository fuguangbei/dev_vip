var render_detail_data = function (data) {
	console.log("[RENDER] Rendering data to detail module...")

	var $detail = $('#moment-detail')
	var hidden_elems = $detail.find('[data-target="author"], [data-target="caption"]')
	hidden_elems.closest('li.list-group-item').addClass('hidden')

	for (var key in data) {
		var el = $detail.find('[data-target=\'{0}\']'.format(key))
		if (el.length) {
			if (key === 'image') {
				el.attr('src', data[key])
			} else if (key === 'publisher') {
				el.text(data[key].name)
			} else if (key === 'author') {
				el.closest('.list-group-item').removeClass('hidden')
				el.text(data[key])
			} else if (key === 'caption') {
				el.closest('.list-group-item').removeClass('hidden')
				el.text(data[key])
			}
			else
				el.text(data[key])
		}
	}
	$detail.find('input.sweetch').sweetch({
		on: data.verified
	})
	$detail.find('input.sweetch').data('id', data.id)
}

// ------------------- MAIN -------------------
$(document).on('ready', function () {
	var $list 	= $('#moments-list'),
		$detail = $('#moment-detail')

	var txts = $list.find('td[text]')

	for (var i = 0; i < txts.length; i++) {
		var $el = $(txts[i])
		var text = $el.text()
		if (text.length > 5)
			$el.text(text.substring(0, 5) + '...') 
	}

	$list.DataTable()

	$(document).on('click', '.post-item', function () {
		var data = $(this).data('post')
		render_detail_data(data)
	})

	$($('.post-item')[0]).click()

	$('input.sweetch').on('sweetch.off', function () {
		var id = $(this).data('id')
		$.ajax({
			url: '/cms/moments/{0}/verify'.format(id),
			type: 'post',
			data: {
				display: false
			},
			beforeSend: function (xhr, settings) {
				if (! csrfSafeMethod(settings.type) && ! this.crossDomain) {
					xhr.setRequestHeader('X-CSRFTOKEN', getCookie('csrftoken'))
				}
			},
			success: function (data) {
				console.log(data)
			},
			error: function (xhr) {
				console.log(xhr.responseText)
			}
		})
	})
	$('input.sweetch').on('sweetch.on', function () {
		var id = $(this).data('id')
		$.ajax({
			url: '/cms/moments/{0}/verify'.format(id),
			type: 'post',
			data: {
				display: true
			},
			beforeSend: function (xhr, settings) {
				if (! csrfSafeMethod(settings.type) && ! this.crossDomain) {
					xhr.setRequestHeader('X-CSRFTOKEN', getCookie('csrftoken'))
				}
			},
			success: function (data) {
				console.log(data)
			},
			error: function (xhr) {
				console.log(xhr.responseText)
			}
		})
	})
	$('input.sweetch').on('sweetch.toggled', function () {
		window.location.reload()
	})
})