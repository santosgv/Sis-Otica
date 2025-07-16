import React, { useState, useContext, useEffect } from "react";
import { ThemeContext } from "../../ThemeContext/themecontext";
import { Link, useNavigate } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import { useCaixaAnterior } from "./hooks/useCaixaAnterior";

interface VisualizarMesAnteriorProps {
  onClose?: () => void;
}

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

const VisualizarMesAnterior: React.FC<VisualizarMesAnteriorProps> = ({
  onClose,
}) => {
  const [dataInicio, setDataInicio] = useState("2025-07-01");
  const [dataFim, setDataFim] = useState("2025-07-09");
  const { lancamentos, loading, erro, mensagem, fetchLancamentos } =
    useCaixaAnterior();
  const { theme } = useContext(ThemeContext);
  const navigate = useNavigate();

  const isDark = theme === "dark";

  const handleBuscar = (e: React.FormEvent) => {
    e.preventDefault();
    fetchLancamentos(dataInicio, dataFim);
  };

  // Formata a data para DD/MM/YYYY
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("pt-BR");
  };

  // Formata o tipo (E/S para Entrada/Saída)
  const formatTipo = (tipo: string) => {
    return tipo === "E" ? "Entrada" : tipo === "S" ? "Saída" : tipo;
  };

  // Formata a forma de pagamento
  const formatForma = (forma: string) => {
    const formas: { [key: string]: string } = {
      A: "Dinheiro",
      P: "PIX",
      D: "Débito",
      C: "Crédito",
      B: "Boleto",
    };
    return formas[forma] || forma;
  };

  // Formata o valor para R$ com duas casas decimais
  const formatValor = (valor: number) => {
    return `R$ ${valor.toFixed(2).replace(".", ",")}`;
  };

  return (
    <div
      className={`w-full h-full transition-colors duration-300 ${
        isDark ? "bg-gray-900 text-gray-100" : "bg-gray-100 text-gray-900"
      } pl-4 md:pl-8 lg:pl-16`}
      style={{ minHeight: "100vh", maxHeight: "100vh", overflowY: "auto", overflowX: "hidden" }}
    >
      {/* Mensagem de feedback */}
      {mensagem && (
        <div
          className={`fixed left-1/2 transform -translate-x-1/2 px-6 py-2 rounded shadow-lg z-50 ${
            mensagem.includes("Nenhuma")
              ? isDark
                ? "bg-gray-700 text-gray-300"
                : "bg-gray-300 text-gray-700"
              : "bg-green-500 text-white"
          }`}
          style={{ top: 88 }}
        >
          {mensagem}
        </div>
      )}
      {erro && (
        <div
          className="fixed left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-2 rounded shadow-lg z-50"
          style={{ top: 88 }}
        >
          {erro}
        </div>
      )}
      <div
        className="max-w-5xl ml-0 mr-auto mt-10 mb-10 flex flex-col gap-4"
        style={{ boxSizing: "border-box" }}
      >
        {/* Título com ícone de voltar */}
        <div className="w-full flex items-center mb-4">
          <button
            className={`mr-2 p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150 ${
              isDark
                ? "bg-gray-700 text-gray-100 hover:bg-gray-600 focus:bg-gray-600"
                : "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:bg-gray-300"
            }`}
            onClick={() => navigate(-1)}
            aria-label="Voltar"
          >
            <FaArrowLeft className="text-xl" />
          </button>
          <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-100 text-left">
            Consultar Período
          </h2>
          {onClose && (
            <button
              className={`btn btn-secondary ml-auto px-3 py-1 rounded ${
                isDark
                  ? "bg-gray-700 text-gray-100 hover:bg-gray-600 focus:bg-gray-600"
                  : "bg-gray-300 text-gray-800 hover:bg-gray-400 focus:bg-gray-400"
              }`}
              onClick={onClose}
              aria-label="Fechar"
            >
              Fechar
            </button>
          )}
        </div>
        {/* Filtros e botão */}
        <form onSubmit={handleBuscar} className="mb-5 w-full">
          <div className="flex flex-wrap gap-4 items-center justify-start w-full">
            <label htmlFor="data-inicio" className="font-medium">
              Data de Início:
            </label>
            <input
              id="data-inicio"
              type="date"
              className={`form-control px-2 py-1 rounded border focus:outline-none focus:ring-2 ${
                isDark
                  ? "bg-gray-800 border-gray-700 text-gray-100 focus:ring-gray-600"
                  : "bg-white border-gray-300 text-gray-900 focus:ring-blue-200"
              } w-40 md:w-48 lg:w-56`}
              value={dataInicio}
              onChange={(e) => setDataInicio(e.target.value)}
              required
              style={{ colorScheme: isDark ? "dark" : "light" }}
            />
            <label htmlFor="data-fim" className="font-medium">
              Data de Término:
            </label>
            <input
              id="data-fim"
              type="date"
              className={`form-control px-2 py-1 rounded border focus:outline-none focus:ring-2 ${
                isDark
                  ? "bg-gray-800 border-gray-700 text-gray-100 focus:ring-gray-600"
                  : "bg-white border-gray-300 text-gray-900 focus:ring-blue-200"
              } w-40 md:w-48 lg:w-56`}
              value={dataFim}
              onChange={(e) => setDataFim(e.target.value)}
              required
              style={{ colorScheme: isDark ? "dark" : "light" }}
            />
            <button
              type="submit"
              className={`btn btn-primary min-w-[180px] px-4 py-2 rounded ${
                isDark
                  ? "bg-blue-700 hover:bg-blue-800 focus:bg-blue-800 text-white"
                  : "bg-blue-500 hover:bg-blue-600 focus:bg-blue-600 text-white"
              }`}
              disabled={loading}
            >
              {loading ? "Carregando..." : "Buscar"}
            </button>
          </div>
        </form>
        {/* Tabela */}
        <div
          style={{
            maxHeight: "calc(100vh - 260px)",
            minHeight: 200,
            overflowY: "auto",
            overflowX: "auto",
          }}
        >
          <table className="w-full border-collapse">
            <thead>
              <tr className={`${isDark ? "bg-gray-800" : "bg-gray-100"}`}>
                <th className="p-2 font-bold text-left">Data</th>
                <th className="p-2 font-bold text-left">Descrição</th>
                <th className="p-2 font-bold text-left">Os</th>
                <th className="p-2 font-bold text-left">Tipo</th>
                <th className="p-2 font-bold text-left">Valor</th>
                <th className="p-2 font-bold text-left">Forma</th>
              </tr>
            </thead>
            <tbody>
              {lancamentos.length === 0 && !loading ? (
                <tr>
                  <td
                    colSpan={6}
                    className={`p-4 ${isDark ? "text-gray-300" : "text-gray-700"}`}
                  >
                    Nenhuma entrada nesse período.
                  </td>
                </tr>
              ) : (
                lancamentos.map((item) => (
                  <tr key={item.id}>
                    <td className="p-2">{formatDate(item.DATA)}</td>
                    <td className="p-2">{item.DESCRICAO}</td>
                    <td className="p-2">
                        <Link
                        to={`/os?id=${item.REFERENCIA}`}
                        className="text-blue-600 hover:text-blue-800">
                        <a>{item.REFERENCIA}</a>
                        </Link>

                    </td>
                    <td className="p-2">{formatTipo(item.TIPO)}</td>
                    <td className="p-2">{formatValor(item.VALOR)}</td>
                    <td className="p-2">{formatForma(item.FORMA)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default VisualizarMesAnterior;