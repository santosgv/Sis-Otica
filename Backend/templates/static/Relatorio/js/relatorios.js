/**
 * relatorios.js
 *
 * Cada função RECEBE o objeto/lista de dados já pronto (em vez de uma URL e fazer fetch).
 * Isso elimina a necessidade de requisição AJAX e, portanto, o problema de CORS.
 *
 * Status de confirmação do formato de dados (baseado no código real das views que você enviou):
 *  - renderiza_total_vendas_12_meses  → CONFIRMADO (vendas_ultimos_12_meses)
 *  - renderiza_vendedor               → CONFIRMADO (maiores_vendedores_30_dias)
 *  - renderiza_fluxo_12_meses         → CONFIRMADO (transacoes_mensais)
 *  - obter_os_em_aberto               → CONFIRMADO (obter_os_em_aberto)
 *  - renderiza_lentes                 → CONFIRMADO (vendas_lentes_dados)
 *  - obter_clientes                   → CONFIRMADO (dados_clientes)
 *  - recebe_hoje                      → CONFIRMADO (receber)
 */

let chartVendas12m;
let chartFluxoMensal;

/**
 * Total de vendas nos últimos 12 meses (gráfico de barra).
 * Formato real da view `vendas_ultimos_12_meses`: lista direta, já ordenada por mês:
 * [{ mes_venda: "Janeiro/2025", total_vendas: 12345.67 }, ...]
 * OBS: 'total_vendas' aqui é o VALOR somado (Sum('VALOR')), não a quantidade de pedidos.
 * Se a intenção for mostrar contagem de vendas (não R$), a view precisa anotar Count('id')
 * também — me avise que ajusto.
 */
function renderiza_total_vendas_12_meses(data) {
  if (!data || data.length === 0) return;

  const labels = data.map(item => item.mes_venda);
  const valores = data.map(item => item.total_vendas);

  const canvas = document.getElementById('vendas_12m').getContext('2d');

  if (chartVendas12m) {
    chartVendas12m.destroy();
  }

  chartVendas12m = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Vendas (R$)',
          data: valores,
          backgroundColor: '#c85a72',
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Total de Vendas (12 meses)',
          font: { size: 16 },
        },
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}


function renderiza_vendedor(data) {
  const vendedorEl = document.getElementById('vendedor');
  if (!vendedorEl) return;

  vendedorEl.innerHTML = '';

  const lista = (data && data.maiores_vendedores_30_dias) || [];

  if (lista.length === 0) {
    vendedorEl.innerHTML = '<li class="text-muted small">Sem dados no período.</li>';
    return;
  }

  const maiorPedidos = Math.max(...lista.map(item => item.total_pedidos));

  lista.forEach((vendedor, index) => {
    const percentual = maiorPedidos > 0 ? (vendedor.total_pedidos / maiorPedidos) * 100 : 0;

    const li = document.createElement('li');
    li.className = 'mb-2';
    li.style.listStyle = 'none';
    li.innerHTML = `
      <div class="d-flex justify-content-between small mb-1">
        <span class="fw-semibold">${index + 1}º ${vendedor.VENDEDOR__first_name || '—'}</span>
        <span class="text-muted">${vendedor.total_pedidos} pedidos · R$ ${vendedor.total_valor_vendas}</span>
      </div>
      <div class="progress mb-1" style="height: 6px;">
        <div class="progress-bar bg-primary" role="progressbar" style="width: ${percentual}%;"></div>
      </div>
      <div class="text-muted" style="font-size: 0.75rem;">
        Ticket médio: R$ ${vendedor.ticket_medio}
      </div>
    `;
    vendedorEl.appendChild(li);
  });
}

/**
 * Fluxo de caixa mensal (entradas x saídas).
 * Formato real da view `transacoes_mensais`: lista direta (sem wrapper), 'mes' já vem
 * como nome em português (ex: "Julho"), não como número:
 * [{ ano: 2025, mes: "Julho", entrada: { total, quantidade }, saida: { total, quantidade } }, ...]
 * Observação: o dicionário original é montado a partir de um dict indexado por (ano, mes),
 * então a ordem de iteração não é necessariamente cronológica — ordenamos aqui no JS.
 */
function renderiza_fluxo_12_meses(data) {
  if (!data || data.length === 0) return;

  const ordemMeses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

  const dadosOrdenados = [...data].sort((a, b) => {
    if (a.ano !== b.ano) return a.ano - b.ano;
    return ordemMeses.indexOf(a.mes) - ordemMeses.indexOf(b.mes);
  });

  const labels = dadosOrdenados.map(item => `${item.mes}/${item.ano}`);
  const saidas = dadosOrdenados.map(item => item.saida.total);
  const entradas = dadosOrdenados.map(item => item.entrada.total);

  const canvas = document.getElementById('fluxo_mensal').getContext('2d');

  if (chartFluxoMensal) {
    chartFluxoMensal.destroy();
  }

  chartFluxoMensal = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Saída',
          data: saidas,
          backgroundColor: 'red',
        },
        {
          label: 'Entrada',
          data: entradas,
          backgroundColor: 'green',
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Fluxo de Caixa Mensal',
          font: { size: 16 },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

/**
 * Ordens de serviço em aberto no mês — preenche #total_vendas e #total_valor.
 * Formato real da view `obter_os_em_aberto`: LISTA com 0 ou 1 item (o filtro já restringe
 * ao mês atual, então não há múltiplos meses aqui, diferente de vendas_ultimos_12_meses):
 * [{ total_vendas: N, total_valor: "1.234,56" }]
 */
function obter_os_em_aberto(data) {
  const totalVendasEl = document.getElementById('total_vendas');
  const totalValorEl = document.getElementById('total_valor');

  if (!data || data.length === 0) {
    totalVendasEl.textContent = '0';
    totalValorEl.textContent = 'R$ 0,00';
    return;
  }

  const item = data[0];
  totalVendasEl.textContent = item.total_vendas ?? '—';
  totalValorEl.textContent = item.total_valor ? `R$ ${item.total_valor}` : 'R$ 0,00';
}

/**
 * Total de clientes cadastrados (status ativo) — preenche #clientes.
 * Formato real da view `dados_clientes`: um NÚMERO cru (int), não um objeto:
 * ex: 342
 */
function obter_clientes(data) {
  const clientesEl = document.getElementById('clientes');
  if (!clientesEl) return;

  clientesEl.textContent = (data ?? 0).toLocaleString('pt-BR');
}

/**
 * Valor a receber hoje — preenche #receber.
 * Formato real da view `receber`: um NÚMERO cru (Decimal), sem formatar_decimal() aplicado.
 * Como Decimal não é serializável nativamente em JSON, o DjangoJSONEncoder (usado por
 * json_script) converte para STRING sem formatação (ex: "1234.5" — ponto, sem milhar).
 * Por isso formatamos a moeda aqui no JS.
 */
function recebe_hoje(data) {
  const receberEl = document.getElementById('receber');
  if (!receberEl) return;

  const valor = parseFloat(data ?? 0);

  receberEl.textContent = valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });
}

/**
 * Vendas de lentes — preenche a lista #lentes.
 * Formato real da view: [{ LENTES: "MULTI FOTO", total: 492 }, ...] (top 5, já ordenado desc).
 */
function renderiza_lentes(data) {
  const lentesEl = document.getElementById('lentes');
  if (!lentesEl) return;

  lentesEl.innerHTML = '';

  if (!data || data.length === 0) {
    lentesEl.innerHTML = '<li class="text-muted small">Sem dados no período.</li>';
    return;
  }

  const maiorTotal = Math.max(...data.map(item => item.total));

  data.forEach(item => {
    const percentual = maiorTotal > 0 ? (item.total / maiorTotal) * 100 : 0;

    const li = document.createElement('li');
    li.className = 'mb-2';
    li.style.listStyle = 'none';
    li.innerHTML = `
      <div class="d-flex justify-content-between small mb-1">
        <span class="fw-semibold">${item.LENTES}</span>
        <span class="text-muted">${item.total}</span>
      </div>
      <div class="progress" style="height: 6px;">
        <div class="progress-bar bg-info" role="progressbar" style="width: ${percentual}%;"></div>
      </div>
    `;
    lentesEl.appendChild(li);
  });
}