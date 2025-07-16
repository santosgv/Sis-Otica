import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaEdit, FaTrash, FaCheck, FaTimes } from "react-icons/fa";
import api from "../../utils/axiosConfig"
import { Button } from "../ui/Button";

interface TipoUnitario {
  id: number;
  nome: string;
}

const TipoUnitarioList: React.FC = () => {
  const navigate = useNavigate();
  const [tipos, setTipos] = useState<TipoUnitario[]>([]);
  const [editId, setEditId] = useState<number | null>(null);
  const [editNome, setEditNome] = useState("");
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [showNovo, setShowNovo] = useState(false);
  const [novoNome, setNovoNome] = useState("");
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [search, setSearch] = useState("");
  const [itensPorPagina, setItensPorPagina] = useState(5);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [mensagem, setMensagem] = useState<string>("");
  const [mensagemTipo, setMensagemTipo] = useState<"sucesso" | "erro" | "">("");
  const [loading, setLoading] = useState(false);

  // Função para buscar tipos unitários da API
  const fetchTiposUnitarios = async () => {
    setLoading(true);
    try {
      const response = await api.get("/tipounitario/", {
        params: {
          page: paginaAtual,
          page_size: itensPorPagina,
          search: search || undefined,
        },
      });
      setTipos(response.data.results);
      setTotalPaginas(Math.ceil(response.data.count / itensPorPagina));
    } catch (error) {
      setMensagem("Erro ao carregar tipos unitários!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    } finally {
      setLoading(false);
    }
  };

  // Buscar tipos unitários quando página, itens por página ou busca mudar
  useEffect(() => {
    fetchTiposUnitarios();
  }, [paginaAtual, itensPorPagina, search]);

  // Edição inline
  const handleEdit = (tipo: TipoUnitario) => {
    setEditId(tipo.id);
    setEditNome(tipo.nome);
  };

  const handleEditSave = async (id: number) => {
    if (!editNome.trim()) {
      setMensagem("O nome do tipo unitário não pode estar vazio!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      await api.put(`/tipounitario/${id}/`, {
        nome: editNome,
      });
      setTipos((prev) =>
        prev.map((t) => (t.id === id ? { ...t, nome: editNome } : t))
      );
      setEditId(null);
      setMensagem("Tipo unitário atualizado com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    } catch (error) {
      setMensagem("Erro ao atualizar tipo unitário!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const handleEditCancel = () => {
    setEditId(null);
    setEditNome("");
  };

  // Novo tipo unitário
  const handleNovo = async () => {
    if (!novoNome.trim()) {
      setMensagem("O nome do tipo unitário não pode estar vazio!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      const response = await api.post("/tipounitario/", {
        nome: novoNome,
      });
      setTipos((prev) => [...prev, response.data]);
      setNovoNome("");
      setShowNovo(false);
      setMensagem("Tipo unitário cadastrado com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      // Recarregar a lista para atualizar a paginação
      fetchTiposUnitarios();
    } catch (error) {
      setMensagem("Erro ao cadastrar tipo unitário!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  // Exclusão
  const handleDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    try {
      await api.delete(`/tipounitario/${deleteId}/`);
      setTipos((prev) => prev.filter((t) => t.id !== deleteId));
      setDeleteId(null);
      setMensagem("Tipo unitário excluído com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      // Recarregar a lista para atualizar a paginação
      fetchTiposUnitarios();
    } catch (error) {
      setMensagem("Erro ao excluir tipo unitário!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const cancelDelete = () => {
    setDeleteId(null);
  };

  return (
    <div className="container mx-auto py-4 px-4 bg-white dark:bg-gray-900 min-h-screen transition-colors duration-300">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 text-center mb-4">
          Tipos Unitários
        </h2>
        {/* Mensagem fixa */}
        <div
          className="fixed z-50"
          style={{
            top: "calc(80px + 1.5rem)",
            left: "calc(36% - 53px)",
            transform: "translateX(0)",
          }}
        >
          {mensagem && (
            <div
              className={`px-3 py-1 rounded shadow text-sm font-medium text-left transition-opacity duration-300 ${
                mensagemTipo === "sucesso" ? "bg-green-500 text-white" : "bg-red-500 text-white"
              }`}
              style={{
                minWidth: "180px",
                height: "32px",
                lineHeight: "30px",
                opacity: mensagem ? 1 : 0,
              }}
            >
              {mensagem}
            </div>
          )}
        </div>
        {/* Barra de pesquisa */}
        <div className="mb-4">
          <div className="flex flex-col md:flex-row md:items-center md:justify-start gap-2 h-full">
            <input
              type="text"
              className="w-full md:w-64 p-2 border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-lg shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:focus:border-blue-400 dark:focus:ring-blue-900 transition-all"
              placeholder="Pesquisar tipo unitário..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPaginaAtual(1);
              }}
              style={{ minWidth: 0 }}
            />
          </div>
        </div>
        {/* Botões de ação */}
        <div className="flex justify-between items-center mb-4">
          <Button
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            onClick={() => setShowNovo((v) => !v)}
          >
            Novo Tipo Unitário
          </Button>
          <div className="flex items-center">
            <button
              className="block sm:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150 bg-gray-500 text-white hover:bg-gray-700 focus:bg-gray-700"
              onClick={() => navigate(-1)}
              aria-label="Voltar"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
            <button
              onClick={() => navigate(-1)}
              className="hidden sm:block bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded ml-2"
            >
              Voltar
            </button>
          </div>
        </div>
        {/* Formulário novo tipo unitário */}
        {showNovo && (
          <div className="mb-4 flex gap-2">
            <input
              className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
              placeholder="Nome do tipo unitário"
              value={novoNome}
              onChange={(e) => setNovoNome(e.target.value)}
              autoFocus
            />
            <Button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold px-4 rounded"
              onClick={handleNovo}
            >
              Salvar
            </Button>
            <Button
              variant="outline"
              className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold px-4 rounded"
              onClick={() => setShowNovo(false)}
            >
              Cancelar
            </Button>
          </div>
        )}
        {/* Tabela de tipos unitários */}
        <div className="w-full">
          <table className="w-full bg-white dark:bg-gray-800 rounded shadow">
            <thead>
              <tr>
                <th className="px-4 py-2 border-b text-left">N°</th>
                <th className="px-4 py-2 border-b text-left">Nome</th>
                <th className="px-4 py-2 border-b text-center">Ações</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td
                    colSpan={3}
                    className="text-center py-4 text-gray-500 dark:text-gray-400"
                  >
                    Carregando...
                  </td>
                </tr>
              ) : tipos.length === 0 ? (
                <tr>
                  <td
                    colSpan={3}
                    className="text-center py-4 text-gray-500 dark:text-gray-400"
                  >
                    Nenhum tipo unitário cadastrado.
                  </td>
                </tr>
              ) : (
                tipos.map((tipo) => (
                  <tr
                    key={tipo.id}
                    className="hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    <td className="px-4 py-2 border-b">{tipo.id}</td>
                    <td className="px-4 py-2 border-b">
                      {editId === tipo.id ? (
                        <input
                          className="p-1 border rounded dark:bg-gray-700 dark:text-white"
                          value={editNome}
                          onChange={(e) => setEditNome(e.target.value)}
                          autoFocus
                        />
                      ) : (
                        <span>{tipo.nome}</span>
                      )}
                    </td>
                    <td className="px-4 py-2 border-b text-center">
                      {editId === tipo.id ? (
                        <>
                          <Button
                            className="text-green-600 hover:text-green-800 mr-2"
                            onClick={() => handleEditSave(tipo.id)}
                            title="Salvar"
                          >
                            <FaCheck />
                          </Button>
                          <Button
                            className="text-red-600 hover:text-red-800"
                            onClick={handleEditCancel}
                            title="Cancelar"
                          >
                            <FaTimes />
                          </Button>
                        </>
                      ) : (
                        <>
                          <Button
                            className="text-blue-600 hover:text-blue-800 mr-2"
                            onClick={() => handleEdit(tipo)}
                            title="Editar"
                          >
                            <FaEdit />
                          </Button>
                          <Button
                            variant="danger" className="text-red-600 hover:text-red-800"
                            onClick={() => handleDelete(tipo.id)}
                            title="Excluir"
                          >
                            <FaTrash />
                          </Button>
                        </>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        {/* Paginação e botão de voltar */}
        <div className="flex justify-between items-center gap-2 mt-4">
          <div className="mt-4 flex justify-center">
            <button
              className="block sm:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150 bg-gray-500 text-white hover:bg-gray-700 focus:bg-gray-700"
              onClick={() => navigate(-1)}
              aria-label="Voltar"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 19l-7-7 7-7"
                />
              </svg>
            </button>
            <button
              onClick={() => navigate(-1)}
              className="hidden sm:block bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            >
              Voltar
            </button>
          </div>
          <div className="flex justify-center items-center gap-2 flex-1">
            <Button
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded"
              disabled={paginaAtual === 1}
              onClick={() => setPaginaAtual(paginaAtual - 1)}
            >
              {"<"}
            </Button>
            <span className="text-gray-700 dark:text-gray-300">
              {paginaAtual} de {totalPaginas}
            </span>
            <Button
              className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded"
              disabled={paginaAtual === totalPaginas || totalPaginas === 0}
              onClick={() => setPaginaAtual(paginaAtual + 1)}
            >
              {">"}
            </Button>
            <div className="flex items-center gap-2 ml-4">
              <label className="text-gray-700 dark:text-gray-300">Exibir</label>
              <select
                className="p-2 border rounded dark:bg-gray-700 dark:text-white"
                value={itensPorPagina}
                onChange={(e) => {
                  setItensPorPagina(Number(e.target.value));
                  setPaginaAtual(1);
                }}
              >
                {[5, 10, 20, 50].map((q) => (
                  <option key={q} value={q}>
                    {q}
                  </option>
                ))}
              </select>
              <span className="text-gray-700 dark:text-gray-300">por página</span>
            </div>
          </div>
        </div>
        {/* Modal de confirmação de exclusão */}
        {deleteId !== null && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
            <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
              <h3 className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100">
                Confirmar exclusão
              </h3>
              <p className="mb-4 text-gray-700 dark:text-gray-300">
                Deseja realmente excluir este tipo unitário?
              </p>
              <div className="flex justify-end gap-2">
                <Button
                  className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded"
                  onClick={confirmDelete}
                >
                  Excluir
                </Button>
                <Button
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                  onClick={cancelDelete}
                >
                  Cancelar
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TipoUnitarioList;