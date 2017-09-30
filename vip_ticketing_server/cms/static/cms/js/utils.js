jQuery.fn.extend({
	/* 
	toggle AdminLTE widget "box" loading state
	@param: state: 
		- undefined: switch to current states' opposite 
		- true: set to loading state
		- false: set to finished state
	*/
	toggle_loading_state: function (state) {
		return this.each(function () {
			var $this = $(this),
				$mask = $this.find('div.overlay')

			if (!$this.hasClass('box'))
				return 

			switch (state) {
				case undefined:
				$mask.toggleClass("hidden")
				break
				case true:
				$mask.removeClass('hidden')
				break
				default:
				$mask.addClass('hidden')
			} 
		})
	},
	/*
	convert jQuery object to the form of money
	*/
	money: function (currency) {
		var class_currency = {
			rmb: 'amount-rmb',
			usd: 'amount-usd'
		}
		return this.each(function () {
			var $this = $(this),
				amount = $this.html()

			if (currency === undefined)
				currency = 'rmb'

			amount = convert_money_amount_str(amount)
			$this.html(amount)
			$this.addClass('amount {0}'.format(class_currency[currency]))
		})
	},
	activate_html: function () {
		return this.each(function () {
			var encoded = $(this).html()

			var decoded = $(this).html(encoded).text()
			$(this).html(decoded)
			$(this).find('input[type=image]').css({
				width: '100%',
				height: 'auto'
			})
		})
	}
})

String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted
}

String.prototype.path_join = function () {
    var current	= this,
        args 	= Array.prototype.slice.call(arguments);

    args.forEach(function (elem, i) {
        var ending = current[current.length - 1],
            starting = elem[0];

        if (ending !== '/')
            current = current + '/';

        if (starting === '/')
            current += elem.substring(1)
        else
            current += elem
    })

    return current
}

String.prototype.template = function (replacements) {
	var pattern = String(this)

	if (!replacements)
		replacements = {}

	if (typeof replacements == 'object') {
		for (var key in replacements) {
			var regex = new RegExp('\\{{0}\\}'.format(key), 'gi')
			pattern = pattern.replace(regex, replacements[key])
		}
		pattern = pattern.replace(/\{\w+\}/g, 'Unknown')

		return $(pattern)
	} else {
		return $(pattern)
	}
}

var convert_money_amount_str = function (amount) {
	if (typeof amount !== 'number') amount = Number(amount).toFixed(2)
	
	var count = 0,
		result = amount.substring(amount.length - 3)

	for (var i = amount.length - 4; i > -1; i--) {
		if (count === 3) {
			count = 0
			result = ',' + result
		}
		result = amount[i] + result
		count++
	}

	return result
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}