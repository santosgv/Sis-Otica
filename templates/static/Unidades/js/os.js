function update() {
  var select = document.getElementById('SERVICO');
  const Sub_Serviço = document.getElementById('SUB_SERVICO');
  var OptionsList = []


  if (select.value =='Encomenda'){
    Sub_Serviço.empty();
    
     OptionsList = ["Óculos de Grau", "Conserto", "lente de contato"];
      OptionsList.forEach((opt) => {
      option = new Option(opt, opt.toLowerCase());
      Sub_Serviço.options[Sub_Serviço.options.length] = option;
     
    });
  }

  if (select.value =='Pronta Entrega'){
    Sub_Serviço.empty();
     OptionsList = ["óculos solar", "lente de contato", "outros"];
      OptionsList.forEach((opt) => {
      option = new Option(opt, opt.toLowerCase());
      Sub_Serviço.options[Sub_Serviço.options.length] = option;  
      
    });
  }
}

update();

function link(){
  var select = document.getElementById('PAGAMENTO');

  if(select.value=='Carne'){
    var div = document.querySelector("div[class='alert alert-warning _carner']");
    div.style.display='block';
  }
}