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
                    $('#'+propriedade+'-div').addClass('has-error');
                    $('#'+propriedade+'-span').text(erro.responseJSON[propriedade]);
                }
            }).always(function(){
                $ajaxSaveGif.hide();
                $salvarBotao.removeAttr('disabled')
            });
    });

});