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
              label: "Total de Vendas nos ultimos 12 Meses",
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
