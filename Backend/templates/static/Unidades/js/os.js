document.getElementById("SERVICO").addEventListener("change", atualizarSegundoSelect);

function atualizarSegundoSelect() {
  var primeiroSelect = document.getElementById("SERVICO");
  var segundoSelect = document.getElementById("SUB_SERVICO");
  // limpa todas as opções do segundo select
  segundoSelect.innerHTML = "";
  // obtém a seleção do primeiro select
  var selecao = primeiroSelect.options[primeiroSelect.selectedIndex].value;
  // cria novas opções para o segundo select de acordo com a seleção do primeiro select
  if (selecao === "Encomenda") {
      var opcao1 = document.createElement("option");
      opcao1.value = "Óculos de Grau";
      opcao1.text = "Óculos de Grau";
      segundoSelect.appendChild(opcao1);

      var opcao2 = document.createElement("option");
      opcao2.value = "Conserto";
      opcao2.text = "Conserto";
      segundoSelect.appendChild(opcao2);

      var opcao3 = document.createElement("option");
      opcao3.value = "lente de contato";
      opcao3.text = "lente de contato";
      segundoSelect.appendChild(opcao3);
  } 
  
  else if (selecao === "Pronta Entrega") {
      var opcao4 = document.createElement("option");
      opcao4.value = "Oculos solar";
      opcao4.text = "Oculos solar";
      segundoSelect.appendChild(opcao4);

      var opcao5 = document.createElement("option");
      opcao5.value = "lente de contato";
      opcao5.text = "lente de contato";
      segundoSelect.appendChild(opcao5);

      var opcao5 = document.createElement("option");
      opcao5.value = "Outros";
      opcao5.text = "Outros";
      segundoSelect.appendChild(opcao5);
  }
}
