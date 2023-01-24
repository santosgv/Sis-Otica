function update() {
  var select = document.getElementById('servico');
  var Sub_Serviço = document.getElementById('Sub_Serviço');

  if (select.value =='Encomenda'){
    alert('Encomenda');
  }

  if (select.value =='Pronta_entrega'){
    alert('Pronta_entrega')
  }
}

update();