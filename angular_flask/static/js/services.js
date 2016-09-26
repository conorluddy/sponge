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
		return $resource('/api/item/:itemId', {}, {
			query: {
				method: 'GET',
				params: { itemId: '' },
				isArray: true
			}
		});
	})
;



