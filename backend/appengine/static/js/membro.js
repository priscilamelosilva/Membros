var membroModulo = angular.module('membroModulo', ['rest']);

membroModulo.directive('membroform', function(){
    return{
        restrict: 'E',
        replace: true,
        templateUrl: '/static/membro/html/membro_form.html ',
        scope:{
            membro:'=',
            nomeLabel: '@',
            cpfLabel: '@',
            rgLabel: '@',
            dataLabel: '@',
            enderecoLabel: '@',
            telefoneLabel: '@',
            cargoLabel: '@',
            saveComplete: '&'

        },
        controller: function($scope, MembroApi){
            $scope.salvandoFlag = false;
            $scope.salvar = function () {
                $scope.salvandoFlag = true;
                $scope.erros = {};
                var promessa = MembroApi.salvar($scope.membro);
                promessa.success(function(membro){
                    $scope.membro.nome = '';
                    $scope.membro.cpf = '';
                    $scope.membro.rg = '';
                    $scope.membro.data = '';
                    $scope.membro.endereco = '';
                    $scope.membro.telefone = '';
                    $scope.membro.cargo = '';
                    $scope.salvandoFlag = false;
                    if($scope.saveComplete != undefined){
                        $scope.saveComplete({'membro': membro});
                    }
                });
                promessa.error(function(erros){
                    $scope.erros = erros;
                    $scope.salvandoFlag = false;
                });
            }
        }
    };
});


membroModulo.directive('membrolinha', function(){
    return{
        replace: true,
        templateUrl: '/static/membro/html/membro_linha.html',
        scope:{
            membro:'=',
            deleteComplete:'&'
        },
        controller: function($scope, MembroApi){
            $scope.ajaxFlag = false;
            $scope.editFlag = false;
            $scope.membroEdicao = [];
            $scope.apagar = function(){
                $scope.ajaxFlag = true;
                MembroApi.apagar($scope.membro.id).success(function(){
                    $scope.deleteComplete({'membro':$scope.membro});
                }).erros(function(){
                    console.log('erro');
                });
            };

            $scope.editar = function(){
                 $scope.editFlag = true;
                 $scope.membroEdicao.id = $scope.membro.id;
                 $scope.membroEdicao.nome = $scope.membro.nome;
                 $scope.membroEdicao.cpf = $scope.membro.cpf;
                 $scope.membroEdicao.rg = $scope.membro.rg;
                 $scope.membroEdicao.data = $scope.membro.data;
                 $scope.membroEdicao.endereco = $scope.membro.endereco;
                 $scope.membroEdicao.telefone = $scope.membro.telefone;
                 $scope.membroEdicao.cargo = $scope.membro.cargo;
            };

            $scope.cancelarEdicao = function(){
                $scope.editFlag = false;
            };

            $scope.completarEdicao = function(){
                MembroApi.editar($scope.membroEdicao).success(function(membro){
                    $scope.membro = membro;
                    $scope.editFlag = false;
                });
            }
        }
    };
});

$(document).ready(function () {
    var $ajaxSaveGif = $('#ajax-save-gif');
    $ajaxSaveGif.hide();
    var $nomeInput = $('#nome-input');
    var $cpfInput = $('#cpf-input');
    var $rgInput = $('#rg-input');
    var $dataInput = $('#data-input');
    var $enderecoInput = $('#endereco-input');
    var $telefoneInput = $('#telefone-input');
    var $cargoInput = $('#cargo-input');
    var $membrosUl = $('#membros-ul');
    function adicionarMembro(membro) {
        var li = '<br><li id = "li-' + membro.id + '"';
        li = li + '><button id = "btn-deletar-' + membro.id + '"';
        li = li + ' class ="btn btn-danger"><i class = "glyphicon glyphicon-trash"></i></button>';
        li = li + membro.nome + ' - ' + membro.cargo + '</li>';
        $membrosUl.append(li);
        $('#btn-deletar-' + membro.id).click(function () {
            $.post('/novo_membro/rest/deletar', {membro_id: membro.id}, function () {
                $("#li-" + membro.id).remove();
            });
        });
    }

    $.get('/novo_membro/rest/listar', function(membros){
        $.each(membros, function(index, m){
            adicionarMembro(m);
        });
    })


    function obterInputsDeMembro() {
        return {
            'nome': $nomeInput.val(),
            'cpf': $cpfInput.val(),
            'rg': $rgInput.val(),
            'data': $dataInput.val(),
            'endereco': $enderecoInput.val(),
            'telefone': $telefoneInput.val(),
            'cargo': $cargoInput.val()
        };
    }

    var $salvarBotao = $('#salvar-btn');
    $salvarBotao.click(function () {
        $('.has-error').removeClass('has-error');
        $('.help-block').empty();
        $ajaxSaveGif.fadeIn();
        $salvarBotao.attr('disabled','disabled')
        $.post('/novo_membro/rest/salvar',
            obterInputsDeMembro(),
            function (membro) {
                $('input[type="text"]').val('');
                adicionarMembro(membro);
            }).error(function(erro){
                for (propriedade in erro.responseJSON){
                    $('#' + propriedade + '-div').addClass('has-error');
                    $('#' + propriedade + '-span').text(erro.responseJSON[propriedade]);
                }
            }).always(function(){
                $ajaxSaveGif.hide();
                $salvarBotao.removeAttr('disabled')
            });
    });

});