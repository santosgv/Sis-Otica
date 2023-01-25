function update() {
  var select = document.getElementById('SERVICO');
  const Sub_Serviço = document.getElementById('SUB_SERVICO');


  if (select.value =='Encomenda'){
      const OptionsList = ["Ruby", "JavaScript", "Python", "GoLang"];
      OptionsList.forEach((opt) => {
      option = new Option(opt, opt.toLowerCase());
      Sub_Serviço.options[Sub_Serviço.options.length] = option;
    });
  }

  if (select.value =='Pronta entrega'){
    
    const OptionsList = ["c#", "teste", "test1", "22"];
    OptionsList.forEach((opt) => {
    option2 = new Option(opt, opt.toLowerCase());
    Sub_Serviço.options[Sub_Serviço.options.length] = option2;
    console.log(OptionsList.length=0);
  });
  }
}

update();