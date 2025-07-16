import { useState, useEffect } from "react";
import api from "../../../utils/axiosConfig";

interface Servico {
  id: number;
  SERVICO: string;
}

export function useServicos() {
  const [servicos, setServicos] = useState<Servico[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  // Busca serviços do endpoint /servicos
  const fetchServicos = async () => {
    try {
      setLoading(true);
      setErro("");
      const res = await api.get("/servicos");
      console.log("Resposta /servicos:", res.data);
      setServicos(res.data.results || []); // Acessa o campo results
    } catch (e) {
      console.error("Erro ao carregar serviços:", e);
      setErro("Erro ao carregar serviços.");
      setServicos([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServicos();
  }, []);

  // Criar novo serviço
  const criarServico = async (SERVICO: string) => {
    if (!SERVICO.trim()) {
      setErro("O nome do serviço é obrigatório.");
      return false;
    }
    try {
      setLoading(true);
      setErro("");
      const res = await api.post("/servicos/", { SERVICO });
      console.log("Resposta POST /servicos:", res.data);
      setServicos([...servicos, res.data]);
      setMensagem("Serviço cadastrado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao criar serviço:", e);
      setErro("Erro ao criar serviço.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Editar serviço
  const editarServico = async (id: number, SERVICO: string) => {
    if (!SERVICO.trim()) {
      setErro("O nome do serviço é obrigatório.");
      return false;
    }
    try {
      setLoading(true);
      setErro("");
      const res = await api.put(`/servicos/${id}/`, { SERVICO });
      console.log("Resposta PUT /servicos:", res.data);
      setServicos(servicos.map((s) => (s.id === id ? res.data : s)));
      setMensagem("Serviço atualizado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao editar serviço:", e);
      setErro("Erro ao editar serviço.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Excluir serviço
  const excluirServico = async (id: number) => {
    try {
      setLoading(true);
      setErro("");
      await api.delete(`/servicos/${id}/`);
      console.log(`Serviço ${id} excluído`);
      setServicos(servicos.filter((s) => s.id !== id));
      setMensagem("Serviço excluído com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao excluir serviço:", e);
      setErro("Erro ao excluir serviço.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    servicos,
    loading,
    erro,
    mensagem,
    criarServico,
    editarServico,
    excluirServico,
    refreshServicos: fetchServicos,
  };
}