function link(){
    var select_sub = document.getElementById('SUB_SERVICO');
    
    var select = document.getElementById('PAGAMENTO');
    var div = document.getElementById('_carner');
    var div2 = document.getElementById('_entrada');
    var div3 = document.getElementById('_parcela');

    if (select.value =='E')
    {
        div.style.display = "block";
    }

    else if (select.value !='E'){
        div.style.display = "none";
    }

    if (select.value =='D')
    {
        div2.style.display = "none";
    }

    if (select.value =='A' || select.value =='B' || select.value =='C' || select.value =='F')
    {
        div3.style.display = "none";
        div2.style.display = "none";
    }

    else if (select.value !='A' || select.value !='B' || select.value !='C' || select.value !='F')
    {
        div3.style.display = "block";
        div2.style.display = "block";
    }
    
}