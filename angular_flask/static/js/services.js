'use strict';

angular.module('angularFlaskServices', ['ngResource', 'ngRoute'])
	.factory('Item', function($resource) {
		return $resource('/api/item/', {}, {
			query: {
				method: 'GET',
				params: { id: '' },
				isArray: true
			}
		});
	})
	.factory('Category', function($resource) {
		return $resource('/api/category', {}, {
			query: {
				method: 'GET',
				params: { },
				isArray: true
			}
		});
	})
	.factory('Search', function($resource) {
		return $resource('/api/item/', {}, {
			query: {
				method: 'GET',
				params: { search: '' },
				isArray: true
			}
		});
	})
	.factory('User', function($resource) {
		return $resource('/api/user/', {}, {
			get: {
				method: 'GET',
				params: { }
			},
			patch: {
				method: 'PATCH',
				params: { }
			}
		});
	})
	.factory('Register', function($resource) {
		return $resource('/api/user/register', {}, {
			query: {
				method: 'POST',
				params: { }
			}
		});
	})
	.factory('Login', function($resource) {
		return $resource('/api/user/login', {}, {
			query: {
				method: 'POST',
				params: { }
			}
		});
	})
	.factory('Logout', function($resource) {
		return $resource('/api/user/logout', {}, {
			query: {
				method: 'GET',
				params: { }
			}
		});
	})
	.factory('Password', function($resource) {
		return $resource('/api/user/password', {}, {
			query: {
				method: 'POST',
				params: { }
			}
		});
	})
;



