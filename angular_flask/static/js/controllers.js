'use strict';

/* Controllers */

function IndexController($scope, Category) {
	Category.get({}, function(categories) {
		$scope.categories = categories.results;
	});
}

function AboutController($scope) {}

function SearchController($scope, $routeParams, $location, Search) {
	var args = {};
	if( $routeParams.search )
		args.search = $routeParams.search;
	if( $routeParams.category )
		args.category = $routeParams.category;
	if( $routeParams.page )
		args.page = $routeParams.page;

	Search.get(args, function(result) {
		$scope.results = result;
		if( result.page < result.page_count )
			$scope.next_url = setQueryStringPage($location.absUrl(), result.page + 1);
		if( result.page > 0 )
			$scope.prev_url = setQueryStringPage($location.absUrl(), result.page - 1);
	});
}

function setQueryStringPage(queryString, page){
	return queryString.split("page")[0] + "page=" + page.toString();
}