'use strict';

/* Controllers */

function IndexController($scope, Category) {
	$scope.$parent.show_subnav = false;
	Category.get({}, function(categories) {
		$scope.categories = categories.results;
	});
}

function ProfileController($scope) {
	$scope.$parent.show_subnav = true;
}
function BorrowingController($scope) {
	$scope.$parent.show_subnav = true;
}
function LendingController($scope) {
	$scope.$parent.show_subnav = true;
}

function SearchController($scope, $routeParams, $location, Search) {
	$scope.$parent.show_subnav = false;

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

function ItemController($scope, $routeParams, Item) {
	$scope.$parent.show_subnav = false;
	var args = {id: $routeParams.id};
	Item.get(args, function(result) {
		$scope.result = result;
	});
}

function setQueryStringPage(queryString, page){
	return queryString.split("page")[0] + "page=" + page.toString();
}

app.controller('NavController', ['$scope', '$window', '$cookieStore', '$http', '$rootScope',
    function($scope, $window, $cookieStore, $http, $rootScope) {
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
    };

	$scope.logout = function(){
		$http({
			method: 'GET',
  			url: 'api/user/logout'
		}).then(function success() {
			// TODO - logout without refresh
			location.reload();
	  	});
	};

    $rootScope.isActive = function(tab){
		return location.pathname.indexOf(tab) != -1;
	};

	/*
	function getLocation(){
		var geoUrl = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDwik5FlbOZ7EW6CHaGMiyNsfIEtZ5b_eI";
		$http.post(geoUrl, {headers: {'Content-Type': 'application/json'}})
		.then(function (response) {
			$cookieStore.put('sponge_lat', response.data.location.lat);
			$cookieStore.put('sponge_lng', response.data.location.lng);
		});
	}
	getLocation();
	*/
}]);

app.controller('LoginController', ['$scope', '$http',
    function($scope, $http) {
    $scope.login = function(){
		$http({
  			method: 'POST',
  			url: 'api/user/login',
			data: {
				email: $scope.email,
				password: $scope.password
			}
		}).then(function success() {
			// TODO - log in without reloading the page
			$scope.error = null;
			location.reload();
	  	}, function error(response) {
			$scope.error = response.data.message;
  		});
    }
}]);

app.controller('SignupController', ['$scope', '$http', '$window',
    function($scope, $http) {
    $scope.signup = function(){
		$http({
  			method: 'POST',
  			url: 'api/user/register',
			data: {
				first: $scope.first,
				last: $scope.last,
				email: $scope.email,
				password: $scope.password
			}
		}).then(function success() {
			// TODO - log in without reloading the page
			$scope.error = null;
			location.reload();
	  	}, function error(response) {
			$scope.error = response.data.message;
  		});
    }
}]);