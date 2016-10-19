'use strict';

angular.module('angularFlaskServices', ['ngResource'])
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
		return $resource('api/category', {}, {
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
			query: {
				method: 'GET',
				params: { search: '' },
				isArray: true
			}
		});
	})
;



