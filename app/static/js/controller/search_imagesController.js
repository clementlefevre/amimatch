/**
 * Created by lefevre on 07.09.2015.
 */

exampleApp.controller('search_imagesController', function ($rootScope, $scope, $http) {
    console.log("search_imagesController reporting for duty.");


    function initData() {
        $scope.loading = true;
        $http.get('/images/amin').success(function (data) {
            $scope.images = data;

            console.log("number of Images found : " + $scope.images.length);


        }).error(function (data, status, headers, config) {
            console.log("Error fetching images");


            return;
        });
    }

    $scope.sort = {
        column: 'name',
        descending: false
    };
    $scope.changeSorting = function (column) {

        var sort = $scope.sort;

        if (sort.column == column) {
            sort.descending = !sort.descending;
        } else {
            sort.column = column;
            sort.descending = false;
        }
    };


    initData();

});
