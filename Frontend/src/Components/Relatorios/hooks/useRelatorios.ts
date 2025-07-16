import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import api from "../../../utils/axiosConfig"

Chart.register(ChartDataLabels);

export function useRelatorios() {
  // States for cards
  const [clientes, setClientes] = useState<number>(0);
  const [receberHoje, setReceberHoje] = useState<number>(0);

    const [osEmAberto, setOsEmAberto] = useState<{ total_vendas: number; total_valor: number }>({
    total_vendas: 0,
    total_valor: 0,
  });

  // States for charts
  const [vendas12Meses, setVendas12Meses] = useState<{
    labels: string[];
    data: number[];
  }>({ labels: [], data: [] });
  const [fluxoMensal, setFluxoMensal] = useState<{
    labels: string[];
    data: number[];
    entrada: number[];
    saida: number[];
  }>({ labels: [], data: [],entrada: [], saida: [] });
  // Refs for charts
  const vendasChartRef = useRef<HTMLCanvasElement | null>(null);
  const fluxoChartRef = useRef<HTMLCanvasElement | null>(null);
  const vendasChartInstance = useRef<Chart | null>(null);
  const fluxoChartInstance = useRef<Chart | null>(null);
   const osChartRef = useRef<HTMLCanvasElement | null>(null);
  const osChartInstance = useRef<Chart | null>(null);
  // State for theme
  const [isDark, setIsDark] = useState(
    document.documentElement.classList.contains("dark")
  );

        // State for Funcionários do Mês card
      const [funcionariosMes, setFuncionariosMes] = useState<
        { nome: string; pedidos: number; vendas: number; ticket: number }[]
      >([]);
      // State for Funcionários do Mês chart
      const [vendedoresChartData, setVendedoresChartData] = useState<{
        labels: string[];
        data: number[];
      }>({ labels: [], data: [] });
      // Ref for Funcionários do Mês chart
      const vendedoresChartRef = useRef<HTMLCanvasElement | null>(null);


  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDark(document.documentElement.classList.contains("dark"));
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    // Fetch data for cards
    const fetchCardData = async () => {
      try {
        // Total clientes ativos
        const clientesRes = await api.get("/total_clientes_ativos");
        setClientes(clientesRes.data.total_clientes || 0);

        const osRes = await api.get("/obter_os_em_aberto");
        const osData = osRes.data.data?.[0] || { total_vendas: 0, total_valor: 0 };
        setOsEmAberto({
          total_vendas: osData.total_vendas || 0,
          total_valor: parseFloat(osData.total_valor) || 0,
        });

        // Total vendido hoje (mapped to receberHoje)
        const receberRes = await api.get("/total_vendido_hoje");
        setReceberHoje(parseFloat(receberRes.data.total_vendido_hoje) || 0);
        console.log(receberRes.data.total_vendido_hoje)

        // Maiores vendedores 30 dias (for card and chart)
        const vendedoresRes = await api.get("/maiores_vendedores_30_dias");

        const vendedoresData = vendedoresRes.data.maiores_vendedores_30_dias || [];
        // For card
        setFuncionariosMes(
          vendedoresData.slice(0, 5).map((v: any) => ({
            nome: v.VENDEDOR__first_name,
            pedidos: v.total_pedidos,
            vendas: parseFloat(v.total_valor_vendas) || 0,
            ticket: parseFloat(v.ticket_medio) || 0,
          }))
        );
        // For chart
        setVendedoresChartData({
          labels: vendedoresData.slice(0, 5).map((v: any) => v.VENDEDOR__first_name),
          data: vendedoresData.slice(0, 5).map((v: any) => parseFloat(v.total_valor_vendas) || 0),
        });
        
      } catch (error) {
        console.error("Erro ao carregar dados dos cards:", error);
        setFuncionariosMes([]);
        setVendedoresChartData({ labels: [], data: [] });
      
      }
  
    };

    // Fetch data for charts
    const fetchChartData = async () => {
      try {
        // Vendas últimos 12 meses
        const vendasRes = await api.get("/vendas_ultimos_12_meses");
        const vendasData = vendasRes.data.data || [];
        if (vendasData.length) {
          setVendas12Meses({
            labels: vendasData.map((item: { mes_venda: string }) => item.mes_venda),
            data: vendasData.map((item: { total_vendas: string }) => parseFloat(item.total_vendas) || 0),
          });
        } else {
          setVendas12Meses({ labels: [], data: [] });
        }

        // Fluxo mensal (caixa transações mensais)
        const fluxoRes = await api.get("/caixa_transacoes_mensais");
  
        const fluxoData = fluxoRes.data.data || [];
                if (fluxoData.length) {
          setFluxoMensal({
            labels: fluxoData.map((item: { ano: number; mes: string }) => `${item.mes}/${item.ano}`),
            entrada: fluxoData.map((item: { entrada: { total: number } }) => item.entrada.total || 0),
            saida: fluxoData.map((item: { saida: { total: number } }) => item.saida.total || 0),
          });
        } else {
          setFluxoMensal({ labels: [], entrada: [], saida: [] });
        }
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
      }
    };

    fetchCardData();
    fetchChartData();
  }, []);

  useEffect(() => {
    if (vendasChartRef.current && vendas12Meses.labels.length) {
      if (vendasChartInstance.current) vendasChartInstance.current.destroy();
      vendasChartInstance.current = new Chart(vendasChartRef.current, {
        type: "bar",
        data: {
          labels: vendas12Meses.labels,
          datasets: [
            {
              label: "Vendas (R$)",
              data: vendas12Meses.data,
              backgroundColor: isDark ? "#60a5fa" : "#007bff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: { padding: { top: 28 } },
          plugins: {
            legend: {
              display: false,
              labels: { color: isDark ? "#f3f4f6" : "#222" },
            },
            datalabels: {
              anchor: "end",
              align: "end",
              color: isDark ? "#fff" : "#000",
              font: { weight: "bold", size: 12 },
              formatter: function (value: number) {
                return value.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
              },
            },
          },
          animation: false,
          scales: {
            x: {
              ticks: { color: isDark ? "#f3f4f6" : "#222" },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
            y: {
              ticks: {
                color: isDark ? "#f3f4f6" : "#222",
                callback: function (value: number) {
                  return value.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
                },
              },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
          },
        },
        plugins: [ChartDataLabels],
      });
    }
    return () => {
      if (vendasChartInstance.current) vendasChartInstance.current.destroy();
    };
  }, [vendas12Meses, isDark]);

    useEffect(() => {
    if (fluxoChartRef.current && fluxoMensal.labels.length) {
      if (fluxoChartInstance.current) fluxoChartInstance.current.destroy();
      fluxoChartInstance.current = new Chart(fluxoChartRef.current, {
        type: "bar",
        data: {
          labels: fluxoMensal.labels,
          datasets: [
            {
              label: "Entradas (R$)",
              data: fluxoMensal.entrada,
              backgroundColor: isDark ? "#60d394" : "#28a745", // Green
            },
            {
              label: "Saídas (R$)",
              data: fluxoMensal.saida,
              backgroundColor: isDark ? "#f87171" : "#ef4444", // Red
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          layout: { padding: { top: 28 } },
          plugins: {
            legend: {
              display: false, // Show legend to distinguish Entrada/Saída
              position: "top",
              labels: { color: isDark ? "#f3f4f6" : "#222" },
            },
            datalabels: {
              anchor: "end",
              align: "end",
              color: isDark ? "#fff" : "#000",
              font: { weight: "bold", size: 12 },
              formatter: function (value: number) {
                return value.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
              },
            },
          },
          animation: false,
          scales: {
            x: {
              ticks: { color: isDark ? "#f3f4f6" : "#222" },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
            y: {
              ticks: {
                color: isDark ? "#f3f4f6" : "#222",
                callback: function (value: number) {
                  return value.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
                },
              },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
          },
        },
        plugins: [ChartDataLabels],
      });
    }
    return () => {
      if (fluxoChartInstance.current) fluxoChartInstance.current.destroy();
    };
  }, [fluxoMensal, isDark]);



  return {
        funcionariosMes,
    vendedoresChartRef,
    clientes,
    osEmAberto,
    receberHoje,
    vendas12Meses,
    fluxoMensal,
    vendasChartRef,
    fluxoChartRef,
    isDark,
  };
}