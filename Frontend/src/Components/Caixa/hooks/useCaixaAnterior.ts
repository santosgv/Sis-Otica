import { useState } from "react";
import api from "../../../utils/axiosConfig";

interface Lancamento {
  id: number;
  DATA: string;
  DESCRICAO: string;
  TIPO: string;
  VALOR: number;
  FORMA: string;
  FECHADO: boolean;
  SALDO_FINAL: number;
  REFERENCIA: string | null;
}

export function useCaixaAnterior() {
  const [lancamentos, setLancamentos] = useState<Lancamento[]>([]);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  const fetchLancamentos = async (dataInicio: string, dataFim: string) => {
    if (!dataInicio || !dataFim) {
      setErro("Por favor, informe as datas de início e término.");
      return;
    }

    try {
      setLoading(true);
      setErro("");
      setMensagem("");
      const res = await api.get("/caixa_anterior/", {
        params: { data_inicio: dataInicio, data_fim: dataFim },
      });
      console.log("Resposta /caixa_anterior:", res.data);
      setLancamentos(res.data.results || []);
      setMensagem(
        res.data.results.length > 0
          ? "Dados carregados com sucesso!"
          : "Nenhuma entrada nesse período."
      );
      setTimeout(() => setMensagem(""), 2500);
    } catch (e) {
      console.error("Erro ao carregar lançamentos:", e);
      setErro("Erro ao carregar lançamentos.");
      setLancamentos([]);
      setMensagem("");
    } finally {
      setLoading(false);
    }
  };

  return { lancamentos, loading, erro, mensagem, fetchLancamentos };
}