'use strict';

angular.module('angularFlaskServices', ['ngResource'])
	.factory('Post', function($resource) {
		return $resource('/api/post/:postId', {}, {
			query: {
				method: 'GET',
				params: { postId: '' },
				isArray: true
			}
		});
	})
	.factory('Item', function($resource) {
		return $resource('/api/item/', {}, {
			query: {
				method: 'GET',
				params: { itemId: '' },
				isArray: true
			}
		});
	})
	.factory('Home', function($resource) {
		return $resource('api/home', {}, {
			query: {
				method: 'GET',
				params: { },
				isArray: true
			}
		});
	})
;



