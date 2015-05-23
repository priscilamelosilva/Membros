var rest = angular.module('rest', []);
rest.factory('MembroApi', function($rootScope){
    return{
        salvar: function(membro){
            var obj={};
            obj.success = function(fcnSucesso){
                obj.fcnSucesso = fcnSucesso;
            };

            obj.error = function(fcnErro){
                obj.fcnErro = fcnErro;
            };

            setTimeout(function(){
                membro.id = 1;
                obj.fcnSucesso(membro)
                $rootScope.$digest()
            },1000);

            return obj;
        }
    };
});