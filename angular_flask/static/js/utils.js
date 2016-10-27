'use strict';

/* Utils */

function setQueryStringPage(queryString, page){
	return queryString.split("page")[0] + "page=" + page.toString();
}

function notifyResponse(data, headersGetter, status){
    if( status == 200) {
        notifySuccess(data);
        return true;
    } else if( status == 401 || status == 405) {
        window.location.href = '/';
    } else {
        notifyError(JSON.parse(data).message);
        return false;
    }
}

function authResponse(data, headersGetter, status){
    if( status == 401 || status == 405) {
        window.location.href = '/';
    }
    return angular.fromJson(data);
}

function notifySuccess(message){
	$.bootstrapGrowl(message, {type: 'success', delay: 2000});
}

function notifyError(message){
	$.bootstrapGrowl(message, {type: 'danger', delay: 2000});
}