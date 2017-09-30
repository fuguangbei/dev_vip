/*register*/
var illegal = function(phone) {
	return !(phone.length === 11)
}

var render_illegal_phone_number = function() {
	console.log('手机号输入不正确')
}

var app_start = function() {
	//    获取验证码
	var $button = $('button.js-getcode'),
		$phone_input = $('input[name=phone].ipt-phone'),
		$pin_input = $('input[name=code]'),
		$button_submit = $('button[type=submit]')

	$button.on('click', function(e) {
		var phone_number = $phone_input.val()

		//    初步检验手机号是否合法
		if (illegal(phone_number)) {
			render_illegal_phone_number()
			return
		}

		$.ajax({
			url: API_host + 'pin/' + phone_number,
			type: 'get',
			success: function(response) {
				alert(response.message)
			},
			error: function(xhr) {
				alert(xhr.responseText)
			}
		})
	})

	//提交注册申请
	$button_submit.on('click', function(e) {
		e.preventDefault()

		var $error_container = $('div.error')
		$error_container.removeClass('hide')

		var data = {}
		data.phone_number = $phone_input.val()
		data.pin = $pin_input.val()
		data.secret = window.location.search
		data.secret = data.secret.substring(1)
	})
};
$(document).ready(function() {

	/*heart good*/
	$("#heart").click(function() {
		$(this).toggleClass("heart-right-active");
	});
	app_start()
});