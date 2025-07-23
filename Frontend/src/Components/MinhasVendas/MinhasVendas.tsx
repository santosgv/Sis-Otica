import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useMinhasVendas } from "./hooks/useMinhasVendas";

const MinhasVendas: React.FC = () => {
  const [search, setSearch] = useState("");
  const [dataInicio, setDataInicio] = useState("2025-07-01");
  const [dataFim, setDataFim] = useState("2025-07-09");

  const {
    vendasResumo,
    pedidos,
    loading,
    erro,
  } = useMinhasVendas(dataInicio, dataFim);

  const resumo = vendasResumo?.[0];

  // Formatar data manualmente para DD/MM/YYYY
  const formatDateToDisplay = (dateStr: string) => {
    if (!dateStr) return "N/A";
    const [year, month, day] = dateStr.split("-");
    return `${day}/${month}/${year}`; // Ex.: 09/07/2025
  };

  // Filtrar pedidos por descrição ou forma de pagamento
  const pedidosFiltrados = pedidos.filter((pedido) =>
    search
      ? (pedido.OBSERVACAO || "").toLowerCase().includes(search.toLowerCase()) ||
        (pedido.FORMA_PAG || "").toLowerCase().includes(search.toLowerCase())
      : true
  );

  return (
    <>
      <div className="font-sans bg-gray-50 dark:bg-gray-900 min-h-screen">
        <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-3 sm:py-6">
          <h5 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-white">
            Extrato de Vendas Registradas
          </h5>

          <div className="w-full flex flex-col flex-1 min-w-0">
            {/* Exibe erro, se houver */}
            {erro && (
              <div className="text-red-600 bg-red-100 border border-red-300 rounded px-3 py-2 text-sm mb-3 text-center">
                {erro}
              </div>
            )}

            {/* Indicadores com dados do resumo da API */}
            <div className="border rounded-lg shadow bg-white dark:bg-gray-900 p-3 md:p-4 mx-auto">
              <h5 className="text-sm font-semibold text-gray-800 dark:text-gray-100 mb-1">
                Minhas vendas - Período
              </h5>

              {loading ? (
                <div className="text-gray-600 dark:text-gray-300 text-sm">Carregando...</div>
              ) : resumo ? (
                <div className="flex flex-col gap-0.5">
                  <span className="text-base text-gray-700 dark:text-gray-200">
                    Total vendido:{" "}
                    {Number(resumo.total_valor_vendas || 0).toLocaleString("pt-BR", {
                      style: "currency",
                      currency: "BRL",
                    })}
                  </span>
                  <span className="text-base text-gray-700 dark:text-gray-200">
                    Pedidos: {resumo.total_pedidos || 0}
                  </span>
                  <span className="text-base text-gray-700 dark:text-gray-200">
                    Ticket médio:{" "}
                    {Number(resumo.ticket_medio || 0).toLocaleString("pt-BR", {
                      style: "currency",
                      currency: "BRL",
                    })}
                  </span>
                </div>
              ) : (
                <div className="text-gray-600 dark:text-gray-400 text-sm">Nenhum dado encontrado.</div>
              )}
              
            </div>

                        {/* Filtros de data e busca */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 sm:p-6 mt-4 mb-4">
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                {/* Campo de busca */}
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                    Buscar por descrição ou forma
                  </label>
                  <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Ex: Pix, Dinheiro..."
                    className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-sm"
                  />
                </div>

                {/* Data início */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                    Data início
                  </label>
                  <input
                    type="date"
                    value={dataInicio}
                    onChange={(e) => setDataInicio(e.target.value)}
                    className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-sm"
                  />
                </div>

                {/* Data fim */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                    Data fim
                  </label>
                  <input
                    type="date"
                    value={dataFim}
                    onChange={(e) => setDataFim(e.target.value)}
                    className="w-full px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Tabela de pedidos detalhados */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 sm:p-6 mt-4">
              {loading ? (
                <div className="text-center text-sm text-gray-600 dark:text-gray-300">
                  Carregando pedidos...
                </div>
              ) : pedidosFiltrados.length === 0 ? (
                <div className="text-center text-sm text-gray-600 dark:text-gray-300">
                  Nenhum pedido encontrado no período selecionado.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm text-gray-700 dark:text-gray-200">
                    <thead>
                      <tr className="bg-gray-200 dark:bg-gray-700">
                        <th className="px-4 py-2 text-left">Data</th>
                        <th className="px-4 py-2 text-left">Descrição</th>
                        <th className="px-4 py-2 text-left">Os</th>
                        <th className="px-4 py-2 text-left">Serviço</th>
                        <th className="px-4 py-2 text-left">Valor</th>
                        <th className="px-4 py-2 text-left">Pagamento</th>
                      </tr>
                    </thead>
                    <tbody>
                      {pedidosFiltrados.map((pedido) => (
                        <tr key={pedido.id} className="border-b border-gray-300 dark:border-gray-700">
                          <td className="px-4 py-2">
                            {formatDateToDisplay(pedido.DATA_SOLICITACAO)}
                          </td>
                          <td className="px-4 py-2">{pedido.OBSERVACAO || ""}</td>
                          <td className="px-4 py-2">

                        <Link
                        to={`/os?id=${pedido.id}`}
                        className="text-blue-600 hover:text-blue-800">
                        <a>{pedido.id}</a>
                        </Link>

                          </td>
                          <td className="px-4 py-2">{pedido.SERVICO_NOME}</td>
                          <td className="px-4 py-2">
                            {Number(pedido.VALOR || 0).toLocaleString("pt-BR", {
                              style: "currency",
                              currency: "BRL",
                            })}
                          </td>
                          <td className="px-4 py-2">{pedido.FORMA_PAG}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default MinhasVendas;