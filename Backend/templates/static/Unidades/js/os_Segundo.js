function atualizarSegundoSelect() {
    var segundoSelect = document.getElementById("SUB_SERVICO");
    var _receita = document.getElementById("_receita");
    var _laboratorio = document.getElementById("_laboratorio");
    var _lentes = document.getElementById("_lentes");
    var _armacao = document.getElementById("_armacao");
    var _observacao = document.getElementById("_observacao");
    var valor = segundoSelect.options[segundoSelect.selectedIndex].value;


    if (valor =="Óculos de Grau"){
        _receita.style.display = 'block';
        _laboratorio.style.display ='block';
        _lentes.style.display = 'block';
        _armacao.style.display = 'block';
        _observacao.style.display='block';
    }

    else if (valor == "lente de contato"){
        _receita.style.display ='block';
        _lentes.style.display = 'block';
        _laboratorio.style.display ='none';
        _armacao.style.display = 'none';
        _observacao.style.display='none';
    }
    else if (valor=="lente de contato pronta" || valor =="Oculos de Sol"){
        _lentes.style.display = 'block';
        _armacao.style.display = 'block';

        _receita.style.display = 'none';
        _laboratorio.style.display ='none';
        _observacao.style.display='none';
    }

    else if (valor == "Outros"){
        _observacao.style.display ='block';

        _receita.style.display = 'none';
        _laboratorio.style.display ='none';
        _lentes.style.display = 'none';
        _armacao.style.display = 'none';
    }

    else if (valor =="Conserto"){
        _observacao.style.display ='block';
        
        _receita.style.display = 'none';
        _laboratorio.style.display ='none';
        _lentes.style.display = 'none';
        _armacao.style.display = 'none';
    }
   
    else
    {
        _receita.style.display = 'none';
        _laboratorio.style.display ='none';
        _lentes.style.display = 'none';
        _armacao.style.display = 'none';
        _observacao.style.display='none';
    }
    
    
}
