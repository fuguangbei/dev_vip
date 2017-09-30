$(document).on('ready', function () {

	$('.amount').money()

	$.ajax({
		url: '/cms/scenery/get_list',
		type: 'get',
		success: function (list) {
			list.forEach(function (elem, index) {
				render_item(elem)
				// activate_calendar(elem)
				render_schedule(elem)
			})
		},
		error: function (xhr, error) {
			console.log(xhr)
			alert(xhr.responseText)
		}
	})

	var $modal = $('#update-inventory')
	$modal.find('button#submit').on('click', function () {
		submit_updates()
		$modal.modal('hide')
	})

	$(document).on('change', 'input[id^=import-]', function () {
		var $this = $(this)
		var file = this.files[0]
		var reader = new FileReader()
		reader.readAsBinaryString(file)
		reader.onload = (function () {
			return function (e) {
				process_file(e)
				$modal.data('tid', $this.data('target'))
				$modal.modal('show')
			}
		})()
		$(this).val('')
	})

	$(document).on('click', 'a.btn-app.import', function () {
		var target_id = $(this).data('target-id'),
			$input_import = $('#import-{0}'.format(target_id))
		$input_import.click()
	})
})

var process_file = function (e) {
	var data 		= e.target.result,
		workbook	= XLSX.read(data, {type: 'binary'}),
		sheet		= workbook.Sheets[workbook.SheetNames[0]]
	
	var rows = XLSX.utils.sheet_to_json(sheet, {
		header: ['date', 'number'], 
		range: 1
	})

	var schedule_list = []
	rows.forEach(function (elem, index) {
		console.log(elem.date)
		var date = new Date(elem.date)
		if (date == 'Invalid Date')
			return 
		var value = elem.number
		if (parseInt(value) != value || value <= 0)
			return 
		var date_str = moment(date).format('YYYY-MM-DD')
		schedule_list.push({
			date: date_str,
			inventory: value
		})
	})
	render_inventory_modal("", schedule_list)
}

var reload_scenery_data = function (id) {
	$.ajax({
		url: '/cms/scenery/{0}/'.format(id),
		type: 'get',
		success: function (data) {
			console.log(data)
			render_schedule(data, true)
		}
	})
}

var render_schedule = function (ticket_data, reload) {
	var $calendar = $('div#calendar-{0}'.format(ticket_data.id))
	var event_list = ticket_data.schedule
	if (reload)
		$calendar.fullCalendar('removeEvents')
	event_list.forEach(function (elem, index) {
		if (elem.count === 0)
			return 
		var temp = {
			title: elem.count,
			start: elem.date
		}
		$calendar.fullCalendar('renderEvent', temp, true)
	})
}

var activate_calendar = function (ticket_data) {
	var $calendar = $('div#calendar-{0}'.format(ticket_data.id))

	$calendar.fullCalendar({
		// events: events_data,
		dayClick: function (date, jsEvent, view) {
			var date_str = date.format()
			var events = $calendar.fullCalendar('clientEvents', function (event) {
				if (event.start.format() == date_str)
					return true
				return false
			})
			if (events.length) {
				invoke_inventory_update(ticket_data, date_str, events[0].title)
			} else {
				invoke_inventory_update(ticket_data, date_str)
			}
		},
		eventClick: function (cal_event, js_event, view) {
			var date_str = cal_event.start.format()
			invoke_inventory_update(ticket_data, date_str, cal_event.title)
		},
		eventRender: function (event, element) {
			element.css('font-size', '24px')
		}
	})
}

var render_item = function (obj) {
	var template = $('#scenery-ticket-template').html(),
		container = $('#tickets')

	var $elem = template.template(obj)
	container.append($elem)

	activate_calendar(obj)
}

var invoke_inventory_update = function (scenery_data, date, current_inventory) {
	render_inventory_modal(scenery_data.title, [{
		date: date,
		inventory: current_inventory
	}])
	$('#update-inventory').data('tid', scenery_data.id)
	$('#update-inventory').modal()
}

var update_inventory = function (scenery_id, date_list, number_list) {
	// console.log('updating ticket {0} inventory on date {1}'.format(scenery_id, date))
	$.ajax({
		url: '/cms/scenery/update/',
		type: 'post',
		beforeSend: function (xhr, settings) {
			if (! csrfSafeMethod(settings.type) && ! this.crossDomain) {
				xhr.setRequestHeader('X-CSRFTOKEN', getCookie('csrftoken'))
			}
		},
		data: {
			id: scenery_id,
			'date[]': date_list,
			'inventory[]': number_list
		},
		success: function (response) {
			reload_scenery_data(scenery_id)
		}
	})
}

var render_inventory_modal = function (title, schedule_list) {
	var $modal = $('#update-inventory'),
		$table = $modal.find('table.table tbody')

	$modal.find('h4.modal-title span.title').text(title)

	$table.find('tr:not(.head)').remove()

	for (var i = 0; i < schedule_list.length; i++) {
		var $row = $('#modal-table-row-template').html().template({
			date: schedule_list[i].date
		})
		$row.find('input').val(schedule_list[i].inventory === undefined ? 0 : schedule_list[i].inventory)
		$table.append($row)
	}
}

var submit_updates = function () {
	var $modal = $('#update-inventory'),
		$rows = $modal.find('tr.data-row')

	var dates = [],
		numbers = []
	for (var i = 0; i < $rows.length; i++) {
		var $row = $($rows[i])
		var date = $row.find('td:first-child').text()
		var number = $row.find('input').val()
		if (!number.length)
			number = 0
		dates.push(date)
		numbers.push(number)
	}

	update_inventory($modal.data('tid'), dates, numbers)
}