'use strict';

var app = angular.module('AngularFlask', ['ngCookies', 'angularFlaskServices', 'ngRoute'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})
		.when('/borrowing', {
			templateUrl: 'static/partials/borrowing.html',
			controller: BorrowingController
		})
		.when('/lending', {
			templateUrl: 'static/partials/lending.html',
			controller: LendingController
		})
		.when('/profile', {
			templateUrl: 'static/partials/profile.html',
			controller: ProfileController
		})
		.when('/search', {
			templateUrl: 'static/partials/search.html',
			controller: SearchController
		})
		.when('/item', {
			templateUrl: 'static/partials/item.html',
			controller: ItemController
		})
		.otherwise({
			redirectTo: '/'
		});
		$locationProvider.html5Mode(true);
	}])
;