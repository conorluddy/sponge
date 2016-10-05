'use strict';

/* Controllers */

function IndexController($scope, Category) {
	var categoryQuery = Category.get({}, function(categories) {
		$scope.categories = categories.results;
	});
}

function AboutController($scope) {
	
}

function SearchController($scope, $routeParams, Search) {
	var searchQuery = Search.get({ search: $routeParams.search }, function(result) {
		$scope.results = result.results;
	});
}

function PostListController($scope, Post) {
	var postsQuery = Post.get({}, function(posts) {
		$scope.posts = posts.objects;
	});
}

function PostDetailController($scope, $routeParams, Post) {
	var postQuery = Post.get({ postId: $routeParams.postId }, function(post) {
		$scope.post = post;
	});
}
