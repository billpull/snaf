'use strict';

/* Filters */

snafApp.filter('nicedate', function () {
	return function (input) {
		return moment(input).fromNow("HH");
	}
});