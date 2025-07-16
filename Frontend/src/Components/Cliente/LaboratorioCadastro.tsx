import React, { useState } from "react";
import { FaArrowLeft } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useLaboratorios } from "./hooks/useLaboratorios";

interface Laboratorio {
  id: number;
  LABORATORIO: string;
}

const LaboratorioCadastro: React.FC = () => {
  const navigate = useNavigate();
  const {
    laboratorios,
    loading,
    erro,
    mensagem,
    criarLaboratorio,
    editarLaboratorio,
    excluirLaboratorio,
  } = useLaboratorios();
  const [search, setSearch] = useState("");
  const [editId, setEditId] = useState<number | null>(null);
  const [editNome, setEditNome] = useState("");
  const [showNovo, setShowNovo] = useState(false);
  const [novoNome, setNovoNome] = useState("");
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const laboratoriosFiltrados = laboratorios.filter((l) =>
    search ? (l.LABORATORIO || "").toLowerCase().includes(search.toLowerCase()) : true
  );

  // Edição inline
  const handleEdit = (lab: Laboratorio) => {
    setEditId(lab.id);
    setEditNome(lab.LABORATORIO);
  };

  const handleEditSave = async (id: number) => {
    const sucesso = await editarLaboratorio(id, editNome);
    if (sucesso) {
      setEditId(null);
      setEditNome("");
    }
  };

  const handleEditCancel = () => {
    setEditId(null);
    setEditNome("");
  };

  // Novo laboratório
  const handleNovo = async () => {
    const sucesso = await criarLaboratorio(novoNome);
    if (sucesso) {
      setNovoNome("");
      setShowNovo(false);
    }
  };

  // Excluir laboratório
  const handleDelete = async (id: number) => {
    const sucesso = await excluirLaboratorio(id);
    if (sucesso) {
      setDeleteId(null);
    }
  };

  return (
    <section className="w-full min-w-0 min-h-[calc(100vh-80px)] bg-gray-50 dark:bg-gray-900 transition-colors py-3 sm:py-6 font-inter">
      <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 flex flex-col flex-1 items-start">
        <div className="w-full flex flex-col flex-1 md:pr-8 md:pl-2 xl:pr-16 xl:pl-6 items-start">
          {/* Título com ícone de voltar */}
          <div className="w-full flex items-center mb-2">
            <button
              className="mr-2 p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-400"
              onClick={() => navigate(-1)}
              aria-label="Voltar"
            >
              <FaArrowLeft className="text-xl text-gray-700 dark:text-gray-200" />
            </button>
            <h2 className="text-2xl font-bold text-left text-gray-900 dark:text-white pl-0">Laboratórios</h2>
          </div>

          {/* Mensagem de erro */}
          {erro && (
            <div className="w-full max-w-2xl mb-4 ml-0 mr-auto text-red-600 bg-red-100 border border-red-300 rounded px-3 py-2 text-sm text-center">
              {erro}
            </div>
          )}

          {/* Mensagem de feedback */}
          {mensagem && (
            <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-2 rounded shadow-lg z-50">
              {mensagem}
            </div>
          )}

          {/* Campo de pesquisa e botões */}
          <div className="w-full max-w-2xl mb-4 ml-0 mr-auto flex flex-col md:flex-row md:items-center md:gap-4">
            <input
              type="text"
              className="w-full md:w-64 p-2 border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 rounded-lg shadow-sm dark:bg-gray-700 dark:text-white dark:border-gray-600 dark:focus:border-blue-400 dark:focus:ring-blue-900 transition-all"
              placeholder="Pesquisar laboratório..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ minWidth: 0 }}
            />
            <div className="flex gap-2 mt-2 md:mt-0">
              <button
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                onClick={() => setShowNovo((v) => !v)}
                disabled={loading}
              >
                Novo Laboratório
              </button>
            </div>
          </div>

          {/* Formulário para novo laboratório */}
          {showNovo && (
            <div className="mb-4 flex gap-2 w-full max-w-2xl ml-0 mr-auto">
              <input
                className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                placeholder="Nome do laboratório"
                value={novoNome}
                onChange={(e) => setNovoNome(e.target.value)}
                autoFocus
                disabled={loading}
              />
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold px-4 rounded"
                onClick={handleNovo}
                disabled={loading}
              >
                Salvar
              </button>
              <button
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold px-4 rounded"
                onClick={() => setShowNovo(false)}
                disabled={loading}
              >
                Cancelar
              </button>
            </div>
          )}

          {/* Scrollbar customizada e tabela responsiva */}
          <style>{`
            #laboratorios-scroll::-webkit-scrollbar { display: none !important; }
            #laboratorios-scroll { -ms-overflow-style: none !important; scrollbar-width: none !important; }
          `}</style>
          <div
            id="laboratorios-scroll"
            className="overflow-x-auto overflow-y-auto max-h-[70vh] min-h-[300px] custom-scrollbar-hide w-full max-w-2xl ml-0 mr-auto rounded-xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
          >
            {loading ? (
              <div className="text-center text-sm text-gray-600 dark:text-gray-300 py-8">
                Carregando laboratórios...
              </div>
            ) : laboratoriosFiltrados.length === 0 ? (
              <table className="min-w-full w-full text-xs sm:text-sm text-left text-gray-900 dark:text-white">
                <thead>
                  <tr>
                    <th className="px-2 sm:px-4 py-2">N°</th>
                    <th className="px-2 sm:px-4 py-2">Nome</th>
                    <th className="px-2 sm:px-4 py-2 text-center">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colSpan={3} className="px-2 sm:px-4 py-8 text-center text-gray-500 dark:text-gray-400 text-xs sm:text-sm">
                      Nenhum laboratório cadastrado.
                    </td>
                  </tr>
                </tbody>
              </table>
            ) : (
              <table className="min-w-full w-full text-xs sm:text-sm text-left text-gray-900 dark:text-white">
                <thead>
                  <tr>
                    <th className="px-2 sm:px-4 py-2">N°</th>
                    <th className="px-2 sm:px-4 py-2">Nome</th>
                    <th className="px-2 sm:px-4 py-2 text-center">Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {laboratoriosFiltrados.map((lab) => (
                    <tr key={lab.id} className="hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                      <td className="px-2 sm:px-4 py-2">{lab.id}</td>
                      <td className="px-2 sm:px-4 py-2">
                        {editId === lab.id ? (
                          <input
                            className="p-1 border rounded dark:bg-gray-700 dark:text-white"
                            value={editNome}
                            onChange={(e) => setEditNome(e.target.value)}
                            autoFocus
                            disabled={loading}
                          />
                        ) : (
                          <span>{lab.LABORATORIO || "N/A"}</span>
                        )}
                      </td>
                      <td className="px-2 sm:px-4 py-2 text-center">
                        {editId === lab.id ? (
                          <>
                            <button
                              className="text-green-600 hover:text-green-800 mr-2"
                              onClick={() => handleEditSave(lab.id)}
                              title="Salvar"
                              disabled={loading}
                            >
                              ✔
                            </button>
                            <button
                              className="text-red-600 hover:text-red-800"
                              onClick={handleEditCancel}
                              title="Cancelar"
                              disabled={loading}
                            >
                              ✖
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              className="text-blue-600 hover:text-blue-800 mr-2"
                              onClick={() => handleEdit(lab)}
                              title="Editar"
                              disabled={loading}
                            >
                              ✎
                            </button>
                            <button
                              className="text-red-600 hover:text-red-800"
                              onClick={() => setDeleteId(lab.id)}
                              title="Excluir"
                              disabled={loading}
                            >
                              🗑
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Modal de confirmação de exclusão */}
          {deleteId !== null && (
            <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
              <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
                <h3 className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100">Confirmar exclusão</h3>
                <p className="mb-4 text-gray-700 dark:text-gray-300">Deseja realmente excluir este laboratório?</p>
                <div className="flex justify-end gap-2">
                  <button
                    className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded"
                    onClick={() => handleDelete(deleteId)}
                    disabled={loading}
                  >
                    Excluir
                  </button>
                  <button
                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                    onClick={() => setDeleteId(null)}
                    disabled={loading}
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default LaboratorioCadastro;