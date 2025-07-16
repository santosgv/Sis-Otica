import React, { useState,useEffect } from "react";
import { FaEdit, FaTrash, FaCheck, FaTimes } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { Button } from '../ui/Button';
import api from "../../utils/axiosConfig"


interface Tipo {
    id: number;
    nome: string;
}

const TipoList: React.FC = () => {
    const navigate = useNavigate();
    const [tipos, setTipos] = useState<Tipo[]>([]);
    const [paginaAtual, setPaginaAtual] = useState(1);
    const [search, setSearch] = useState("");
    const [itensPorPagina, setItensPorPagina] = useState(25);
    const tiposFiltrados = tipos.filter((t) => t.nome.toLowerCase().includes(search.toLowerCase()));
    const totalPaginas = Math.ceil(tiposFiltrados.length / itensPorPagina);
    const tiposPagina = tiposFiltrados.slice((paginaAtual - 1) * itensPorPagina, paginaAtual * itensPorPagina);

    const [editId, setEditId] = useState<number | null>(null);
    const [editNome, setEditNome] = useState("");
    const [showNovo, setShowNovo] = useState(false);
    const [novoNome, setNovoNome] = useState("");
    const [deleteId, setDeleteId] = useState<number | null>(null);
    const [mensagem, setMensagem] = useState<string>("");
    const [loading, setLoading] = useState(false);

     // Função para buscar tipos da API
  const fetchTipos = async () => {
    setLoading(true);
    try {
      const response = await api.get("/tipo/", {
        params: {
          page: paginaAtual,
          page_size: itensPorPagina,
          search: search || undefined,
        },
      });
      setTipos(response.data.results);
    } catch (error) {
      setMensagem("Erro ao carregar tipos!");
        console.log(error)
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
    } finally {
      setLoading(false);
    }
  };

  // Buscar tipos quando página, itens por página ou busca mudar
  useEffect(() => {
    fetchTipos();
  }, [paginaAtual, itensPorPagina, search]);

  // Edição inline
  const handleEdit = (tipo: Tipo) => {
    setEditId(tipo.id);
    setEditNome(tipo.nome);
  };

  const handleEditSave = async (id: number) => {
    if (!editNome.trim()) {
      setMensagem("O nome do tipo não pode estar vazio!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
      return;
    }
    try {
      await api.put(`/tipo/${id}/`, {
        nome: editNome,
      });
      setTipos((prev) =>
        prev.map((t) => (t.id === id ? { ...t, nome: editNome } : t))
      );
      setEditId(null);
      setMensagem("Tipo atualizado com sucesso!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
    } catch (error) {
      setMensagem("Erro ao atualizar tipo!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
    }
  };

  const handleEditCancel = () => {
    setEditId(null);
    setEditNome("");
  };

  // Novo tipo
  const handleNovo = async () => {
    if (!novoNome.trim()) {
      setMensagem("O nome do tipo não pode estar vazio!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
      return;
    }
    try {
      const response = await api.post("/tipo/", {
        nome: novoNome,
      });
      setTipos((prev) => [...prev, response.data]);
      setNovoNome("");
      setShowNovo(false);
      setMensagem("Tipo cadastrado com sucesso!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
      // Recarregar a lista para atualizar a paginação
      fetchTipos();
    } catch (error) {
      setMensagem("Erro ao cadastrar tipo!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
    }
  };

  // Exclusão
  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/tipo/${id}/`);
      setTipos((prev) => prev.filter((t) => t.id !== id));
      setDeleteId(null);
      setMensagem("Tipo excluído com sucesso!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
      // Recarregar a lista para atualizar a paginação
      fetchTipos();
    } catch (error) {
      setMensagem("Erro ao excluir tipo!");
      setTimeout(() => {
        setMensagem("");
        setMensagem("");
      }, 2500);
    }
  };


    return (
        <div className="w-full min-w-0 py-4 px-2 sm:px-4 md:px-8 bg-white dark:bg-gray-900 min-h-screen transition-colors duration-300">
            <div className="max-w-2xl mx-auto min-w-0">
                {/* Toast de mensagem temporária */}
                {/* Toast de mensagem fixa alinhada com a barra de pesquisa, levemente para a direita */}
                <div className="fixed z-50" style={{ top: 'calc(80px + 1.5rem)', left: 'calc(36% - 53px)', transform: 'translateX(0)' }}>
                    {mensagem && (
                        <div
                            className={`px-3 py-1 rounded shadow text-sm font-medium text-left transition-opacity duration-300 bg-green-500 text-white`}
                            style={{ minWidth: '180px', height: '32px', lineHeight: '30px', opacity: mensagem ? 1 : 0 }}
                        >
                            {mensagem}
                        </div>
                    )}
                </div>
                <h2 className="text-center text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">Tipos</h2>
                {/* Barra de pesquisa */}
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-2 mb-4">
                    <input
                        type="text"
                        className="w-full md:w-64 p-2 border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-lg shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:focus:border-blue-400 dark:focus:ring-blue-900 transition-all"
                        placeholder="Pesquisar tipo..."
                        value={search}
                        onChange={e => { setSearch(e.target.value); setPaginaAtual(1); }}
                        style={{ minWidth: 0 }}
                    />
                </div>
                {/* Botões de ação */}
                <div className="flex justify-between items-center mb-4">
                    <button
                        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        onClick={() => setShowNovo((v) => !v)}
                    >
                        Novo Tipo
                    </button>
                    {/* Botão Voltar responsivo */}
                    <div className="flex items-center">
                        <button
                            className="block sm:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150 bg-gray-500 text-white hover:bg-gray-700 focus:bg-gray-700"
                            onClick={() => navigate(-1)}
                            aria-label="Voltar"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
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
                {/* Formulário novo tipo */}
                {showNovo && (
                    <div className="mb-4 flex gap-2">
                        <input
                            className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                            placeholder="Nome do tipo"
                            value={novoNome}
                            onChange={(e) => setNovoNome(e.target.value)}
                            autoFocus
                        />
                        <Button className="bg-blue-500 hover:bg-blue-700 text-white font-bold px-4 rounded" onClick={handleNovo}>Salvar</Button>
                        <Button variant="outline" className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold px-4 rounded" onClick={() => setShowNovo(false)}>Cancelar</Button>
                    </div>
                )}
                {/* Tabela de tipos */}
                <div className="overflow-x-auto w-full">
                    <table className="min-w-full sm:min-w-[640px] table-auto w-full bg-white dark:bg-gray-800 rounded shadow">
                        <thead>
                            <tr>
                                <th className="px-4 py-2 border-b text-left">N°</th>
                                <th className="px-4 py-2 border-b text-left">Nome</th>
                                <th className="px-4 py-2 border-b text-center">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {tiposPagina.length === 0 && (
                                <tr><td colSpan={3} className="text-center py-4 text-gray-500 dark:text-gray-400">Nenhum tipo cadastrado.</td></tr>
                            )}
                            {tiposPagina.map((tipo) => (
                                <tr key={tipo.id} className="hover:bg-gray-100 dark:hover:bg-gray-700">
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
                                                <Button variant="primary" className="text-green-600 hover:text-green-800 mr-2" onClick={() => handleEditSave(tipo.id)} title="Salvar"><FaCheck /></Button>
                                                <Button variant="danger" className="text-red-600 hover:text-red-800" onClick={handleEditCancel} title="Cancelar"><FaTimes /></Button>
                                            </>
                                        ) : (
                                            <>
                                                <Button variant="primary" className="text-blue-600 hover:text-blue-800 mr-2" onClick={() => handleEdit(tipo)} title="Editar"><FaEdit /></Button>
                                                <Button variant="danger" className="text-red-600 hover:text-red-800" onClick={() => setDeleteId(tipo.id)} title="Excluir"><FaTrash /></Button>
                                            </>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                {/* Paginação e botão de voltar */}
                <div className="flex justify-between items-center gap-2 mt-4">
                                <button
              onClick={() => navigate(-1)}
              className="hidden sm:block bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            >
              Voltar
            </button>
                    <div className="flex justify-center items-center gap-2 flex-1">
                        <Button variant="outline" className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded" disabled={paginaAtual === 1} onClick={() => setPaginaAtual(paginaAtual - 1)}>{'<'}</Button>
                        <span className="text-gray-700 dark:text-gray-300">{paginaAtual} de {totalPaginas}</span>
                        <Button variant="outline" className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded" disabled={paginaAtual === totalPaginas || totalPaginas === 0} onClick={() => setPaginaAtual(paginaAtual + 1)}>{'>'}</Button>
                        {/* Select de quantidade por página ao lado direito do paginator */}
                        <div className="flex items-center gap-2 ml-4">
                            <label className="text-gray-700 dark:text-gray-300">Exibir</label>
                            <select
                                className="p-2 border rounded dark:bg-gray-700 dark:text-white"
                                value={itensPorPagina}
                                onChange={e => { setItensPorPagina(Number(e.target.value)); setPaginaAtual(1); }}
                            >
                                {[5, 10, 20, 50].map(q => <option key={q} value={q}>{q}</option>)}
                            </select>
                            <span className="text-gray-700 dark:text-gray-300">por página</span>
                        </div>
                    </div>
                </div>
                {/* Modal de confirmação de exclusão */}
                {deleteId !== null && (
                    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
                        <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
                            <h3 className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100">Confirmar exclusão</h3>
                            <p className="mb-4 text-gray-700 dark:text-gray-300">Deseja realmente excluir este tipo?</p>
                            <div className="flex justify-end gap-2">
                                <Button variant="danger" className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded" onClick={() => handleDelete(deleteId)}>Excluir</Button>
                                <Button variant="outline" className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded" onClick={() => setDeleteId(null)}>Cancelar</Button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TipoList;
