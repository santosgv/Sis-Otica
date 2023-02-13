function link(){
    var select = document.getElementById('PAGAMENTO');
    var div = document.getElementById('_carner');
    var div2 = document.getElementById('_entrada');
    var div3 = document.getElementById('_parcela');
    if (select.value =='E')
    {
        div.style.display = "block";
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
}