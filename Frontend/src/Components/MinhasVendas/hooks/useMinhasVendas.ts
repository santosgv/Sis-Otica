import { useState, useEffect } from "react";
import api from "../../../utils/axiosConfig";

export function useMinhasVendas(dataInicio: string, dataFim: string) {
  const [vendasResumo, setVendasResumo] = useState<any[]>([]);
  const [servicos, setServicos] = useState<{ id: number; nome: string }[]>([]);
  const [loadingServicos, setLoadingServicos] = useState(true);
  const [pedidos, setPedidos] = useState([]);
  const [loadingResumo, setLoadingResumo] = useState(true);
  const [loadingPedidos, setLoadingPedidos] = useState(true);
  const [erro, setErro] = useState("");


    // Mapeamento de formas de pagamento
  const formasPagamento: { [key: string]: string } = {
    A: "PIX",
    B: "DINHEIRO",
    C: "DEBITO",
    D: "CREDITO",
    E: "CARNER",
    F: "PERMUTA",
  };

  const getFormaPagamento = (codigo: string) => formasPagamento[codigo] || "N/A";

  // Validação de formato de data
  const isValidDate = (date: string) => {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    return regex.test(date) && !isNaN(new Date(date).getTime());
  };

    // Busca serviços do endpoint /servicos
  useEffect(() => {
    const fetchServicos = async () => {
      try {
        setLoadingServicos(true);
        setErro("");
        const res = await api.get("/servicos");
        setServicos(res.data.results || []); // Assume que /servicos retorna [{ id: number, nome: string }, ...]
      } catch (e) {
        console.error("Erro ao carregar serviços:", e);
        setErro("Erro ao carregar serviços.");
        setServicos([]);
      } finally {
        setLoadingServicos(false);
      }
    };

    fetchServicos();
  }, []);

  // Busca resumo de vendas do endpoint /minhas_vendas_mes_atual
  useEffect(() => {
    const fetchResumo = async () => {
      try {
        setLoadingResumo(true);
        setErro("");
        if (!dataInicio || !dataFim || !isValidDate(dataInicio) || !isValidDate(dataFim)) {
          setErro("Datas de início e fim devem ser válidas (YYYY-MM-DD).");
          setVendasResumo([]);
          return;
        }
        if (new Date(dataInicio) > new Date(dataFim)) {
          setErro("Data de início deve ser anterior ou igual à data de fim.");
          setVendasResumo([]);
          return;
        }

        console.log("Chamando /minhas_vendas_mes_atual com:", { data_inicio: dataInicio, data_fim: dataFim });
        const res = await api.get("/minhas_vendas_mes_atual", {
          params: {
            data_inicio: dataInicio,
            data_fim: dataFim,
            withCredentials: true
          },
        });
        console.log("Resposta /minhas_vendas_mes_atual:", res.data);
        setVendasResumo(res.data.minhas_vendas_mes || []);
      } catch (e) {
        console.error("Erro ao carregar resumo:", e);
        setErro("Erro ao carregar as vendas.");
        setVendasResumo([]);
      } finally {
        setLoadingResumo(false);
      }
    };

    fetchResumo();
  }, [dataInicio, dataFim]);

  // Busca pedidos do endpoint /pedidos_vendedor
  useEffect(() => {
    async function carregarPedidos() {
      try {
        setLoadingPedidos(true);
        setErro("");
        if (!dataInicio || !dataFim || !isValidDate(dataInicio) || !isValidDate(dataFim)) {
          setErro("Datas de início e fim devem ser válidas (YYYY-MM-DD).");
          setPedidos([]);
          return;
        }
        if (new Date(dataInicio) > new Date(dataFim)) {
          setErro("Data de início deve ser anterior ou igual à data de fim.");
          setPedidos([]);
          return;
        }

        console.log("Chamando /pedidos_vendedor com:", { data_inicio: dataInicio, data_fim: dataFim });
        const response = await api.get("/pedidos_vendedor", {
          params: {
            data_inicio: dataInicio,
            data_fim: dataFim,
            withCredentials: true
          },
        });
        console.log("Resposta /pedidos_vendedor:", response.data);
        // Mapear o campo SERVICO para o nome do serviço
        const pedidosComNomeServico = response.data.pedidos.map((pedido: any) => ({
          ...pedido,
          SERVICO_NOME: servicos.find((s) => s.id === pedido.SERVICO)?.SERVICO || "N/A",
          FORMA_PAG: getFormaPagamento(pedido.FORMA_PAG),
        }));
        setPedidos(pedidosComNomeServico);
      } catch (err) {
        console.error("Erro ao carregar pedidos:", err);
        setErro("Erro ao carregar pedidos.");
        setPedidos([]);
      } finally {
        setLoadingPedidos(false);
      }
    }

    carregarPedidos();
  }, [dataInicio, dataFim, servicos]);

  return {
    vendasResumo,
    pedidos,
    loading: loadingResumo || loadingPedidos|| loadingServicos,
    erro,
  };
}