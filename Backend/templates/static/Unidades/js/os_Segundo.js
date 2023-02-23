function atualizarSegundoSelect() {
    var segundoSelect = document.getElementById("SUB_SERVICO");
    var _receita = document.getElementById("_receita");
    var _laboratorio = document.getElementById("_laboratorio");
    var _lentes = document.getElementById("_lentes");
    var _armacao = document.getElementById("_armacao");
    var _observacao = document.getElementById("_observacao");
    var valor = segundoSelect.options[segundoSelect.selectedIndex].value;

    if (valor === 'lente de contato'){
        _laboratorio.style.display ='none';
        _receita.style.display ='none';
        _armacao.style.display ='none';
       
    }else{
        _laboratorio.style.display ='block';
        _receita.style.display ='block';  
        _armacao.style.display ='block'; 
    }

    if (valor ==='Conserto'){
        _laboratorio.style.display ='none';
        _receita.style.display ='none';
        _armacao.style.display ='none';
        _lentes.style.display ='none';
    }else{
        _laboratorio.style.display ='block';
        _receita.style.display ='block';  
        _armacao.style.display ='block'; 
        _lentes.style.display ='block';
    }
}
