'use strict';

var snafApp = angular.module('Snaf', ['snafServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/feed.html',
			controller: FeedController
		})
		.when('/topics', {
			templateUrl: 'static/partials/topics.html',
			controller: TopicController
		})
		.when('/events', {
			templateUrl: 'static/partials/events.html',
			controller: EventController
		})
		.when('/account', {
			templateUrl: 'static/partials/account.html',
			controller: AccountController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
	.directive('selectActiveFeedItem', function(){
	    return function(scope, element, attr){
	        element.bind('click', function(){      
	        	$('.active-panel').not(this).removeClass('active-panel')
	    					  	  .removeClass('panel-warning')
	    					  	  .find('.feed-item-meta')
								  .slideUp();

	            $(this).addClass('active-panel')
	            		.addClass('panel-warning')
	            		.find('.feed-item-meta')
						.slideDown()
						.promise().done(function () {
							$('html, body').animate({
						        scrollTop: $('.active-panel').offset().top
						    }, 300);
						});
				

				scope.$apply(attr.selectActiveFeedItem)
	        });
	    };
	})
	.directive('selectBrokerageAccount', function () {
		return function(scope, element, attr) {
			element.bind('click', function () {

				$(this).parents('.panel')
						.find('.panel-footer')
						.addClass('active-broker-form')
						.removeClass('hidden');
			});
		}
	});