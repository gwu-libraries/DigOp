<span xmlns="http://www.w3.org/1999/xhtml">/*!
 * jQuery UI @VERSION
 *
 * Copyright (c) 2010 AUTHORS.txt (http://jqueryui.com/about)
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://docs.jquery.com/UI
 */
;jQuery.ui || (function($)<span> {
</span>
//Helper functions and ui object
$.ui =<span> {
</span>	version: "@VERSION",

	// $.ui.plugin is deprecated.  Use the proxy pattern instead.
	plugin:<span> {
</span>		add: function(module, option, set)<span> {
</span>			var proto = $.ui[module].prototype;
			for(var i in set)<span> {
</span>				proto.plugins[i] = proto.plugins[i] || [];
				proto.plugins[i].push([option, set[i]]);
			}
		},
		call: function(instance, name, args)<span> {
</span>			var set = instance.plugins[name];
			if(!set || !instance.element[0].parentNode)<span> { </span>return; }

			for (var i = 0; i < set.length; i++)<span> {
</span>				if (instance.options[set[i][0]])<span> {
</span>					set[i][1].apply(instance.element, args);
				}
			}
		}
	},

	contains: function(a, b)<span> {
</span>		return document.compareDocumentPosition
			? a.compareDocumentPosition(b) & 16
			: a !== b && a.contains(b);
	},

	hasScroll: function(el, a)<span> {
</span>
		//If overflow is hidden, the element might have extra content, but the user wants to hide it
		if ($(el).css('overflow') == 'hidden')<span> { </span>return false; }

		var scroll = (a && a == 'left') ? 'scrollLeft' : 'scrollTop',
			has = false;

		if (el[scroll] > 0)<span> { </span>return true; }

		// TODO: determine which cases actually cause this to happen
		// if the element doesn't have the scroll set, see if it's possible to
		// set the scroll
		el[scroll] = 1;
		has = (el[scroll] > 0);
		el[scroll] = 0;
		return has;
	},

	isOverAxis: function(x, reference, size)<span> {
</span>		//Determines when x coordinate is over "b" element axis
		return (x > reference) && (x < (reference + size));
	},

	isOver: function(y, x, top, left, height, width)<span> {
</span>		//Determines when x, y coordinates is over "b" element
		return $.ui.isOverAxis(y, top, height) && $.ui.isOverAxis(x, left, width);
	},

	keyCode:<span> {
</span>		BACKSPACE: 8,
		CAPS_LOCK: 20,
		COMMA: 188,
		CONTROL: 17,
		DELETE: 46,
		DOWN: 40,
		END: 35,
		ENTER: 13,
		ESCAPE: 27,
		HOME: 36,
		INSERT: 45,
		LEFT: 37,
		NUMPAD_ADD: 107,
		NUMPAD_DECIMAL: 110,
		NUMPAD_DIVIDE: 111,
		NUMPAD_ENTER: 108,
		NUMPAD_MULTIPLY: 106,
		NUMPAD_SUBTRACT: 109,
		PAGE_DOWN: 34,
		PAGE_UP: 33,
		PERIOD: 190,
		RIGHT: 39,
		SHIFT: 16,
		SPACE: 32,
		TAB: 9,
		UP: 38
	}
};

//jQuery plugins
$.fn.extend(<span>{
</span>	_focus: $.fn.focus,
	focus: function(delay, fn)<span> {
</span>		return typeof delay === 'number'
			? this.each(function()<span> {
</span>				var elem = this;
				setTimeout(function()<span> {
</span>					$(elem).focus();
					(fn && fn.call(elem));
				}, delay);
			})
			: this._focus.apply(this, arguments);
	},
	
	enableSelection: function()<span> {
</span>		return this
			.attr('unselectable', 'off')
			.css('MozUserSelect', '')
			.unbind('selectstart.ui');
	},

	disableSelection: function()<span> {
</span>		return this
			.attr('unselectable', 'on')
			.css('MozUserSelect', 'none')
			.bind('selectstart.ui', function()<span> { </span>return false; });
	},

	scrollParent: function()<span> {
</span>		var scrollParent;
		if(($.browser.msie && (/(static|relative)/).test(this.css('position'))) || (/absolute/).test(this.css('position')))<span> {
</span>			scrollParent = this.parents().filter(function()<span> {
</span>				return (/(relative|absolute|fixed)/).test($.curCSS(this,'position',1)) && (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
			}).eq(0);
		} else<span> {
</span>			scrollParent = this.parents().filter(function()<span> {
</span>				return (/(auto|scroll)/).test($.curCSS(this,'overflow',1)+$.curCSS(this,'overflow-y',1)+$.curCSS(this,'overflow-x',1));
			}).eq(0);
		}

		return (/fixed/).test(this.css('position')) || !scrollParent.length ? $(document) : scrollParent<span xmlns="http://www.w3.org/1999/xhtml">;
	},

	zIndex: function(zIndex)<span><span> {
</span></span>		if (zIndex !== undefined)<span><span> {
</span></span>			return this.css('zIndex', zIndex);
		}
		
		if (this.length)<span><span> {
</span></span>			var elem = $(this[0]), position, value;
			while (elem.length && elem[0] !== document)<span><span> {
</span></span>				// Ignore z-index if position is set to a value where z-index is ignored by the browser
				// This makes behavior of this function consistent across browsers
				// WebKit always returns auto if the element is positioned
				position = elem.css('position');
				if (position == 'absolute' || position == 'relative' || position == 'fixed')
			<span><span>	{
</span></span>					// IE returns 0 when zIndex is not specified
					// other browsers return a string
					// we ignore the case of nested elements with an explicit value of 0
					// <div style="z-index: -10;"><div style="z-index: 0;"></div></div>
					value = parseInt(elem.css('zIndex'));
					if (!isNaN(value) && value != 0)<span><span> {
</span></span>						return value;
					}
				}
				elem = elem.parent();
			}
		}

		return 0;
	}
});


//Additional selectors
$.extend($.expr[':'],<span><span> {
</span></span>	data: function(elem, i, match)<span><span> {
</span></span>		return !!$.data(elem, match[3]);
	},

	focusable: function(element)<span><span> {
</span></span>		var nodeName = element.nodeName.toLowerCase(),
			tabIndex = $.attr(element, 'tabindex');
		return (/input|select|textarea|button|object/.test(nodeName)
			? !element.disabled
			: 'a' == nodeName || 'area' == nodeName
				? element.href || !isNaN(tabIndex)
				: !isNaN(tabIndex))
			// the element and all of its ancestors must be visible
			// the browser may report that the area is hidden
			&& !$(element)['area' == nodeName ? 'parents' : 'closest'](':hidden').length;
	},

	tabbable: function(element)<span><span> {
</span></span>		var tabIndex = $.attr(element, 'tabindex');
		return (isNaN(tabIndex) || tabIndex >= 0) && $(element).is(':focusable');
	}
});

})(jQuery);
