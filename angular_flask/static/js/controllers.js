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
	if( $routeParams.county )
		args.county = $routeParams.county;

	Search.get(args, function(result) {
		$scope.results = result;
		if( result.page + 1 < result.page_count && result.page_count > 1 )
			$scope.next_url = setQueryStringPage($location.absUrl(), result.page + 1);
		if( result.page > 0 )
			$scope.prev_url = setQueryStringPage($location.absUrl(), result.page - 1);
	});
}

function setQueryStringPage(queryString, page){
	return queryString.split("page")[0] + "page=" + page.toString();
}

app.controller('NavController', ['$scope', '$window', '$cookieStore',
    function($scope, $window, $cookieStore) {
    $scope.search_term = $cookieStore.get('sponge_search');
    $scope.selected_county = $cookieStore.get('sponge_county') || 'Anywhere';
    $scope.selected_county_id = $cookieStore.get('sponge_county_id') || 0;

    $scope.setCountyId = function(county_id){
        $scope.selected_county_id = county_id;
        $cookieStore.put('sponge_county_id', county_id);
    };

    $scope.setCounty = function(county){
        $scope.selected_county = county;
        $cookieStore.put('sponge_county', county);
    };

    $scope.search = function(){
        $cookieStore.put('sponge_search', $scope.search_term);
        $window.location.href =
            "/search?search=" + $scope.search_term + "&county=" + $scope.selected_county_id + "&page=0";
    }
}]);

app.controller('LoginController', ['$scope', '$window',
    function($scope, $window) {
    $scope.login = function(){
		// Todo
    }
}]);

app.controller('SignupController', ['$scope', '$window',
    function($scope, $window) {
    $scope.signup = function(){
		// Todo
    }
}]);