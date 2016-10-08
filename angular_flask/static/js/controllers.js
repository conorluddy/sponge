'use strict';

/* Controllers */

function IndexController($scope, Category) {
	Category.get({}, function(categories) {
		$scope.categories = categories.results;
	});
}

function AboutController($scope) {}

function SearchController($scope, $routeParams, Search) {
	var args = {};
	if( $routeParams.search )
		args.search = $routeParams.search;
	if( $routeParams.category )
		args.category = $routeParams.category;
	if( $routeParams.page )
		args.page = $routeParams.page;

	Search.get(args, function(result) {
		$scope.results = result.results;
	});
}
