import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../../utils/axiosConfig"

interface Cliente {
  id: number;
  NOME: string;
  LOGRADOURO: string;
  NUMERO: string;
  BAIRRO: string;
  CIDADE: string;
  CPF: string;
  EMAIL: string;
  TELEFONE: string;
}

interface ApiResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Cliente[];
}

const PAGE_SIZE_OPTIONS = [25, 50, 100];

const SearchBar: React.FC<{ search: string; setSearch: (value: string) => void }> = ({ search, setSearch }) => (
  <div className="flex items-center gap-4 w-full px-4 pt-4">
    <input
      type="search"
      placeholder="Pesquisar por nome..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="w-64 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
      aria-label="Pesquisar clientes"
    />
    <Link
      to="/cadastro-cliente"
      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
    >
      Cadastrar Cliente
    </Link>
  </div>
);

const Paginator: React.FC<{
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  pageSize: number;
  setPageSize: (size: number) => void;
}> = ({ currentPage, totalPages, onPageChange, pageSize, setPageSize }) => {
  return (
    <div className="flex flex-col md:flex-row justify-center items-center gap-4 mt-8 w-full max-w-full px-2 overflow-x-auto">
      <div className="flex items-center gap-2 flex-shrink-0">
        <span className="text-xs text-gray-600 dark:text-gray-300 font-medium">Itens por página:</span>
        <select
          value={pageSize}
          onChange={(e) => setPageSize(Number(e.target.value))}
          className="rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        >
          {PAGE_SIZE_OPTIONS.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        <button
          className="px-3 py-1 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 disabled:opacity-50 shadow-sm transition"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          aria-label="Página anterior"
        >
          &lt;
        </button>
        <span className="px-3 py-1 text-gray-700 dark:text-gray-200 font-semibold rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm">
          Página {currentPage} de {totalPages}
        </span>
        <button
          className="px-3 py-1 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 disabled:opacity-50 shadow-sm transition"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          aria-label="Próxima página"
        >
          &gt;
        </button>
      </div>
    </div>
  );
};

const Clientes: React.FC = () => {
  const [search, setSearch] = useState("");
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZE_OPTIONS[0]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar clientes da API
  const fetchClientes = async (page: number, size: number, searchQuery: string = "") => {
    setLoading(true);
    setError(null);
    try {
      const params = {
        page: page.toString(),
        page_size: size.toString(),
        ...(searchQuery && { search: searchQuery }),
      };
      const response = await api.get("/clientes/", { params });
      const data: ApiResponse = response.data;
      setClientes(data.results);
      setTotalCount(data.count);
    } catch (err) {
      console.error("Erro ao buscar clientes:", err);
      setError("Não foi possível carregar os clientes. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  // Carregar clientes quando a página, o tamanho da página ou a busca mudar
  useEffect(() => {
    fetchClientes(currentPage, pageSize, search);
  }, [currentPage, pageSize, search]);

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));

  return (
    <section className="flex-1 flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors">
      <div className="w-full flex flex-col flex-1">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white mb-2 px-4">Clientes</h1>
        <SearchBar search={search} setSearch={setSearch} />
        {error && (
          <div className="px-4 py-2 text-red-600 dark:text-red-400">{error}</div>
        )}
        {loading ? (
          <div className="px-4 py-8 text-center text-gray-500 dark:text-gray-300">
            Carregando clientes...
          </div>
        ) : (
          <>
            <div className="overflow-auto rounded-lg shadow bg-white dark:bg-gray-800 mt-6">
              <table className="min-w-full w-full text-sm text-left text-gray-900 dark:text-white">
                <thead>
                  <tr>
                    {["Nome", "Logradouro", "Número", "Bairro", "Cidade", "CPF", "Email", "Telefone", "Ação"].map(
                      (header) => (
                        <th
                          key={header}
                          className="px-4 py-2 text-left text-xs font-medium text-gray-700 dark:text-white uppercase tracking-wider"
                        >
                          {header}
                        </th>
                      )
                    )}
                  </tr>
                </thead>
                <tbody>
                  {clientes.length === 0 ? (
                    <tr>
                      <td colSpan={9} className="px-4 py-8 text-center text-gray-500 dark:text-gray-300">
                        Nenhum cliente encontrado.
                      </td>
                    </tr>
                  ) : (
                    clientes.map((cliente) => (
                      <tr key={cliente.id} className="hover:bg-gray-100 dark:hover:bg-gray-700 transition">
                        <td className="px-4 py-2">
                          <Link
                            className="text-blue-600 dark:text-blue-400 hover:underline"
                            to={`/cliente?id=${cliente.id}`}
                            rel="noopener noreferrer"
                          >
                            {cliente.NOME}
                          </Link>
                        </td>
                        <td className="px-4 py-2 max-w-[150px] truncate">{cliente.LOGRADOURO}</td>
                        <td className="px-4 py-2">{cliente.NUMERO}</td>
                        <td className="px-4 py-2 max-w-[150px] truncate">{cliente.BAIRRO}</td>
                        <td className="px-4 py-2 max-w-[150px] truncate">{cliente.CIDADE}</td>
                        <td className="px-4 py-2">{cliente.CPF}</td>
                        <td className="px-4 py-2 max-w-[150px] truncate">{cliente.EMAIL}</td>
                        <td className="px-4 py-2 flex items-center gap-2">
                          {cliente.TELEFONE}
                          <a
                            href={`https://wa.me/55${cliente.TELEFONE.replace(/\D/g, "")}?text=Olá! ${cliente.NOME}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            aria-label={`Enviar mensagem para ${cliente.NOME} via WhatsApp`}
                          >
                            <img
                              width="24"
                              height="24"
                              src="https://img.icons8.com/color/48/whatsapp--v1.png"
                              alt="WhatsApp"
                            />
                          </a>
                        </td>
                        <td className="px-4 py-2">
                          <Link
                            to={`/cadastro-os?cliente=${cliente.id}`}
                            aria-label="Criar ordem de serviço"
                          >
                            <svg
                              className="w-6 h-6 text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                              xmlns="http://www.w3.org/2000/svg"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M9 12h6m-3-3v6m-7 4h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                              />
                            </svg>
                          </Link>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
            <Paginator
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
              pageSize={pageSize}
              setPageSize={setPageSize}
            />
          </>
        )}
      </div>
    </section>
  );
};

export default Clientes;