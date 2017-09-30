+function ($) {
	'use strict'

	var selector = 'span.switch-container'

	var Sweetch = function (el, options) {
		this.$el		= $(el)
		this.$display 	= $('<span>', {
			"class": 'switch-container'
		})
		this.$display.append($('<small>', {
			"class": 'switch-handle'
		})).append($('<p>', {
			'class': 'text'
		}))
		this.options	= $.extend({}, Sweetch.DEFAULTS, options)
		this.toggle_start = false

		this.init()
	}

	Sweetch.DEFAULTS = {
		on: false,
		text_on: 'ON',
		text_off: 'OFF'
	}

	Sweetch.prototype.on_click = function (e) {
		var $this = $(this)
		var data = $(this).data('eb.sweetch')

		data.toggle()
		data.render()
	}

	Sweetch.prototype.set_state = function (state) {
		if (state === undefined)
			this.on = !this.on
		else
			this.on = state
	}

	Sweetch.prototype.toggle = function (state) {
		this.$el.trigger('sweetch.toggle')
		this.toggle_start = true
		if (state === undefined) {
			this.on = !this.on
		} else {
			this.on = state
		}
		if (this.on) {
			this.$el.trigger('sweetch.on')
		}
		else
			this.$el.trigger('sweetch.off')
	}

	Sweetch.prototype.render = function () {
		var $handle = this.$display.find('.switch-handle'),
			$text = this.$display.find('p.text')

		var x_off = 1,
			W = this.$display.width(),
			w = $handle.width(),
			x_on = W - 1 - w

		if (this.on) {
			this.$display.addClass('on')
			// $text.text(this.options.text_on)
			$handle.css('left', x_on)
		}
		else {
			this.$display.removeClass('on')
			// $text.text(this.options.text_off)
			$handle.css('left', x_off)
		}
	}

	Sweetch.prototype.setPosition = function () {
		var pos = this.$el.offset(),
			w = this.$el.width(), 
			W = this.$display.width()

		this.$display.offset({
			top: pos.top,
			left: pos.left + w - W
		})
	}

	Sweetch.prototype.init = function () {
		var self = this
		this.on = this.options.on
		this.$el.after(this.$display)
		this.setPosition()
		this.$display.find('.switch-handle').on('transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd', function (e) {
			if (self.toggle_start) {
				self.$el.trigger('sweetch.toggled')
				self.toggle_start = false
			}
		})
		this.$el.css('display', 'none')
		this.render()
	}

	Sweetch.prototype.destroy = function () {

	}

	function Plugin(option) {
		return this.each(function () {
			var $this 	= $(this)
			var data	= $this.data('eb.sweetch')
			var options = typeof option == 'object' && option

			if (!data) {
				data = new Sweetch(this, options)
				$this.data('eb.sweetch', data)
			}
			data.$display.data('eb.sweetch', data)

			if (options) {
				data.set_state(options.on)
				data.render()
			}
		})
	}

	$.fn.sweetch 				= Plugin
	$.fn.sweetch.Constructor	= Sweetch

	$(document).on('click', selector, Sweetch.prototype.on_click)
}(jQuery)