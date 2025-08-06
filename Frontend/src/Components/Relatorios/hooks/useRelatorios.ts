import { useEffect, useRef, useState } from "react";
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import api from "../../../utils/axiosConfig";

Chart.register(ChartDataLabels);

export function useRelatorios() {
  const [clientes, setClientes] = useState<number>(0);
  const [receberHoje, setReceberHoje] = useState<number>(0);
  const [osEmAberto, setOsEmAberto] = useState<{ total_vendas: number; total_valor: number }>({
    total_vendas: 0,
    total_valor: 0,
  });

  const [vendas12Meses, setVendas12Meses] = useState<{ labels: string[]; data: number[] }>({
    labels: [],
    data: [],
  });

  const [fluxoMensal, setFluxoMensal] = useState<{
    labels: string[];
    data: number[];
    entrada: number[];
    saida: number[];
  }>({
    labels: [],
    data: [],
    entrada: [],
    saida: [],
  });

  const vendasChartRef = useRef<HTMLCanvasElement | null>(null);
  const fluxoChartRef = useRef<HTMLCanvasElement | null>(null);
  const vendasChartInstance = useRef<Chart | null>(null);
  const fluxoChartInstance = useRef<Chart | null>(null);

  const [isDark, setIsDark] = useState(
    document.documentElement.classList.contains("dark")
  );

  const [funcionariosMes, setFuncionariosMes] = useState<
    { nome: string; pedidos: number; vendas: number; ticket: number }[]
  >([]);

  const [vendedoresChartData, setVendedoresChartData] = useState<{
    labels: string[];
    data: number[];
  }>({ labels: [], data: [] });

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
    const fetchCardData = async () => {
      try {
        const clientesRes = await api.get("/total_clientes_ativos");
        setClientes(clientesRes.data.total_clientes || 0);

        const osRes = await api.get("/obter_os_em_aberto");
        const osData = osRes.data.data?.[0] || { total_vendas: 0, total_valor: 0 };
        setOsEmAberto({
          total_vendas: osData.total_vendas || 0,
          total_valor: parseFloat(osData.total_valor.replace(/\./g, "").replace(",", ".")) || 0,
        });


        const receberRes = await api.get("/total_vendido_hoje");
        setReceberHoje(parseFloat(receberRes.data.total_vendido_hoje) || 0);

        const vendedoresRes = await api.get("/maiores_vendedores_30_dias");
        const vendedoresData = vendedoresRes.data.maiores_vendedores_30_dias || [];

        setFuncionariosMes(
          vendedoresData.slice(0, 5).map((v: any) => ({
            nome: v.VENDEDOR__first_name,
            pedidos: v.total_pedidos,
            vendas: parseFloat(v.total_valor_vendas.replace(/\./g, "").replace(",", ".")) || 0,
            ticket: parseFloat(v.ticket_medio.replace(/\./g, "").replace(",", ".")) || 0,
          }))
        );

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

    const fetchChartData = async () => {
      try {
        const vendasRes = await api.get("/vendas_ultimos_12_meses");
        const vendasData = vendasRes.data.data || [];
        setVendas12Meses({
          labels: vendasData.map((item: any) => item.mes_venda),
          data: vendasData.map((item: any) => parseFloat(item.total_vendas) || 0),
        });

        const fluxoRes = await api.get("/caixa_transacoes_mensais");
        const fluxoData = fluxoRes.data.data || [];

        setFluxoMensal({
          labels: fluxoData.map((item: any) => `${item.mes}/${item.ano}`),
          data: [],
          entrada: fluxoData.map((item: any) => item.entrada.total || 0),
          saida: fluxoData.map((item: any) => item.saida.total || 0),
        });
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        setFluxoMensal({ labels: [], data: [], entrada: [], saida: [] });
      }
    };

    fetchCardData();
    fetchChartData();
  }, []);

  useEffect(() => {
    if (vendasChartRef.current && vendas12Meses.labels.length) {
      vendasChartInstance.current?.destroy();
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
              formatter: (value: number) =>
                value.toLocaleString("pt-BR", { minimumFractionDigits: 2 }),
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
                callback(tickValue: string | number) {
                  return typeof tickValue === "number"
                    ? tickValue.toLocaleString("pt-BR", {
                        minimumFractionDigits: 2,
                      })
                    : tickValue;
                },
              },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
          },
        },
        plugins: [ChartDataLabels],
      });
    }
    return () => vendasChartInstance.current?.destroy();
  }, [vendas12Meses, isDark]);

  useEffect(() => {
    if (fluxoChartRef.current && fluxoMensal.labels.length) {
      fluxoChartInstance.current?.destroy();
      fluxoChartInstance.current = new Chart(fluxoChartRef.current, {
        type: "bar",
        data: {
          labels: fluxoMensal.labels,
          datasets: [
            {
              label: "Entradas (R$)",
              data: fluxoMensal.entrada,
              backgroundColor: isDark ? "#60d394" : "#28a745",
            },
            {
              label: "Saídas (R$)",
              data: fluxoMensal.saida,
              backgroundColor: isDark ? "#f87171" : "#ef4444",
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
              position: "top",
              labels: { color: isDark ? "#f3f4f6" : "#222" },
            },
            datalabels: {
              anchor: "end",
              align: "end",
              color: isDark ? "#fff" : "#000",
              font: { weight: "bold", size: 12 },
              formatter: (value: number) =>
                value.toLocaleString("pt-BR", { minimumFractionDigits: 2 }),
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
                callback(tickValue: string | number) {
                  return typeof tickValue === "number"
                    ? tickValue.toLocaleString("pt-BR", {
                        minimumFractionDigits: 2,
                      })
                    : tickValue;
                },
              },
              grid: { color: isDark ? "#374151" : "#e5e7eb" },
            },
          },
        },
        plugins: [ChartDataLabels],
      });
    }
    return () => fluxoChartInstance.current?.destroy();
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
