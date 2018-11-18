app.controller("controller", function($http, $scope, $uibModal) {


    $scope.get_uploads = function() {
        $http.get('/uploads/').success(function(data) {
            $scope.uploads = data.uploads
        })
    }

    $scope.change_mode = function(mode) {
        delete $scope.file
        $scope.mode = mode
        if (mode == 1) {
            $scope.get_uploads()
        }
    }

    $scope.initial = function() {
        $scope.mode = 1
        $scope.get_uploads()
        $scope.geocoding_label_map = { 1: "InProgress", 2: "Complete" }
    }

    $scope.download_csv = function(uploadid) {
        window.location.href = '/download-csv/' + String(uploadid) + "/"
    }

    $scope.uploadfile = function() {
        var file = $scope.file[0]
        var extnsn = '.' + file.name.slice((file.name.lastIndexOf(".") - 1 >>> 0) + 2)
        if (['.xlsx'].indexOf(extnsn) == -1) {
            $scope.invalid_file_error = true
            alert('Invalid file')
            return
        }
        $scope.invalid_file_error = false

        var fd = new FormData();
        //Take the first selected file
        fd.append("file", file);
        $http.post('/upload-file/', fd, {
            withCredentials: true,
            headers: { 'Content-Type': undefined },
            transformRequest: angular.identity
        }).success(function(data) {
            //$scope.ok(data.geojson)
            $scope.change_mode(1)
        }).error(function(data, status) {
            if (data.response) {
                alert(data.response)
            } else {
                alert("Invalid file")
            }
        });
    }

    $scope.initial()

})