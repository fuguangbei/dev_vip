var format_text_display = function () {
	var $sales = $('#sales .info-box-content span.info-box-number')
	$sales.text('￥' + convert_money_amount_str($sales.text()))
}

$(document).ready(function () {
	var $sales = $('#sales .info-box-content span.info-box-number')
	$sales.money()

	$('div#users').on('click', function () {
		window.location.href = "/cms/users/"
	})
	$('div#orders, div#sales').on('click', function () {
		window.location.href = '/cms/purchases/'
	})
	// read agent data
})