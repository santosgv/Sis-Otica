import { useState, useEffect } from "react";
import api from "../../../utils/axiosConfig";

interface Laboratorio {
  id: number;
  LABORATORIO: string;
}

export function useLaboratorios() {
  const [laboratorios, setLaboratorios] = useState<Laboratorio[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  // Busca laboratórios do endpoint /laboratorios
  const fetchLaboratorios = async () => {
    try {
      setLoading(true);
      setErro("");
      const res = await api.get("/laboratorios");
      console.log("Resposta /laboratorios:", res.data);
      setLaboratorios(res.data.results || []); // Acessa o campo results
    } catch (e) {
      console.error("Erro ao carregar laboratórios:", e);
      setErro("Erro ao carregar laboratórios.");
      setLaboratorios([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLaboratorios();
  }, []);

  // Criar novo laboratório
  const criarLaboratorio = async (LABORATORIO: string) => {
    if (!LABORATORIO.trim()) {
      setErro("O nome do laboratório é obrigatório.");
      return false;
    }
    try {
      setLoading(true);
      setErro("");
      const res = await api.post("/laboratorios/", { LABORATORIO });
      console.log("Resposta POST /laboratorios:", res.data);
      setLaboratorios([...laboratorios, res.data]);
      setMensagem("Laboratório cadastrado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao criar laboratório:", e);
      setErro("Erro ao criar laboratório.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Editar laboratório
  const editarLaboratorio = async (id: number, LABORATORIO: string) => {
    if (!LABORATORIO.trim()) {
      setErro("O nome do laboratório é obrigatório.");
      return false;
    }
    try {
      setLoading(true);
      setErro("");
      const res = await api.put(`/laboratorios/${id}/`, { LABORATORIO });
      console.log("Resposta PUT /laboratorios:", res.data);
      setLaboratorios(laboratorios.map((l) => (l.id === id ? res.data : l)));
      setMensagem("Laboratório atualizado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao editar laboratório:", e);
      setErro("Erro ao editar laboratório.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Excluir laboratório
  const excluirLaboratorio = async (id: number) => {
    try {
      setLoading(true);
      setErro("");
      await api.delete(`/laboratorios/${id}/`);
      console.log(`Laboratório ${id} excluído`);
      setLaboratorios(laboratorios.filter((l) => l.id !== id));
      setMensagem("Laboratório excluído com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
      return true;
    } catch (e) {
      console.error("Erro ao excluir laboratório:", e);
      setErro("Erro ao excluir laboratório.");
      setMensagem("");
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    laboratorios,
    loading,
    erro,
    mensagem,
    criarLaboratorio,
    editarLaboratorio,
    excluirLaboratorio,
    refreshLaboratorios: fetchLaboratorios,
  };
}