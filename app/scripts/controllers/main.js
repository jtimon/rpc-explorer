'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        if ($routeParams.chain) {
            SrvChain.set($routeParams.chain);
        }
        $scope.CTverbose = false;
        $scope.verbose = false;
        $scope.rawhex_limit = 100;

        function cleanTx() {
            $scope.txid = "";
            $scope.transaction = null;
            $scope.txjson = null;
        }

        function cleanBlock() {
            $scope.blockid = "";
            $scope.blockheight = null;
            $scope.block = null;
            $scope.blockjson = null;
        }

        cleanTx();
        cleanBlock();

        function successCallbackBlock(data) {
            $scope.block = data;
            $scope.blockheight = $scope.block["height"];
            $scope.blockjson = JSON.stringify($scope.block, null, 4);

            return $scope.block["height"];
        };

        function statsCallbackBlock(data) {
            $scope.blockstats = data;
        };

        function PromBlockstats(height) {
            return SrvBackend.get("blockstats", height)
                .then(statsCallbackBlock);
        };

        var goToBlock = function(blockhash) {
            return SrvBackend.get("block", blockhash)
                .then(successCallbackBlock)
                .then(PromBlockstats);
        };

        $scope.searchBlockByHeight = function() {
            function successCallbackBlockHeight(data) {
                $scope.blockid = SrvUtil.GetResult(data);
                return $scope.blockid;
            };
            var params = {"height": $scope.blockheight};
            SrvBackend.RpcCall("getblockhash", params)
                .then(successCallbackBlockHeight)
                .then(goToBlock)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function successCallbackTx(data) {
            $scope.showtxlist = false;
            $scope.transaction = data;
            $scope.blockid = $scope.transaction["blockhash"];
            $scope.txjson = JSON.stringify($scope.transaction, null, 4);

            return $scope.blockid;
        };

        var goToTx = function(txhash) {
            return SrvBackend.get("tx", txhash)
                .then(successCallbackTx)
                .then(goToBlock);
        };

        $scope.IsCTOut = function(output) {
            return !output["value"] && output["value"] != 0;
        };

        $scope.searchBlock = function() {
            cleanTx();
            goToBlock($scope.blockid)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchTx = function() {
            if ($scope.txid == "") {
                $scope.transaction = null;
                return;
            }
            cleanBlock();
            goToTx($scope.txid)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        if ($routeParams.block) {
            $scope.blockid = $routeParams.block;
            goToBlock($routeParams.block)
                .catch(SrvUtil.errorCallbackScoped($scope));
        } else if ($routeParams.txid) {
            $scope.txid = $routeParams.txid;
            goToTx($routeParams.txid)
                .catch(SrvUtil.errorCallbackScoped($scope));
        }
    });
