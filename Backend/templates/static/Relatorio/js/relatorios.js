function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }
    
    return [bg_color, border_color];
    
}

function renderiza_total_vendas_12_meses(url){


    fetch(url)
    .then(response => response.json())  // Converte a resposta em JSON
    .then(data => {
      // Extrai as informações relevantes do objeto JSON para gerar o gráfico
      const labels = data.data.map(item => item.mes_venda);
      const values = data.data.map(item => item.total_vendas);
      const canvas = document.getElementById('vendas_12m').getContext('2d');
      var cores_vendas_12m = gera_cor(qtd=12)

      // Configura o gráfico
      const chart = new Chart(canvas, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Total",
              data: values,
              backgroundColor: cores_vendas_12m[0],
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });
    })
    .catch(error => console.error(error));


}


function renderiza_vendedor(url) {
  fetch(url, {
    method: 'get',
  }).then(function(result) {
    return result.json()
  }).then(function(data) {
    const vendedores = data.maiores_vendedores_30_dias;
    const vendedorContainer = document.getElementById('vendedor');

    vendedores.forEach(function(vendedor) {
      const vendedorNome = vendedor['VENDEDOR__first_name'];
      const totalPedidos = vendedor['total_pedidos'];
      const totalvendas = vendedor['total_valor_vendas'];
      // Crie elementos HTML para exibir o nome do vendedor e o total de pedidos
      const vendedorElement = document.createElement('div');
      vendedorElement.innerHTML = `${vendedorNome}: ${totalPedidos} Pedidos ${totalvendas} em Vendas`;

      // Adicione o elemento à div de vendedores
      vendedorContainer.appendChild(vendedorElement);
    });
  });
}


function renderiza_fluxo_12_meses(url) {
  fetch(url)
    .then(response => response.json())  // Converte a resposta em JSON
    .then(data => {
      // Extrai as informações relevantes do objeto JSON para gerar o gráfico

      const labels = data.data.map(item => `${item.mes}/${item.ano}`);
      const saidas = data.data.map(item => item.saida.total);
      const entradas = data.data.map(item => item.entrada.total);
      const canvas = document.getElementById('fluxo_mensal').getContext('2d');

      // Configura o gráfico
      const chart = new Chart(canvas, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Saída",
              data: saidas,
              backgroundColor: "red",
            },
            {
              label: "Entrada",
              data: entradas,
              backgroundColor: "green",
            },
          ],
        },
        options: {
          title:{
            display:true,
            fontSize:20,
            text:"Fluxo de Caixa Mensal nos ultimos 12 Meses:"
          },
          responsive: true,
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });
    })
    .catch(error => console.error(error));
}