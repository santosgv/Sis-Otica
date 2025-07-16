import React, { useEffect, useState } from "react";
import { useNavigate,Link } from "react-router-dom";
import AdicionarCaixa from "./AdicionarCaixa";
import Money from "./Money";
import api from "../../utils/axiosConfig";

export interface Lancamento {
  id: number;
  data: string;
  descricao: string;
  os: string;
  tipo: string;
  valor: string;
  forma: string;
}

const Caixa: React.FC = () => {
  const navigate = useNavigate();
  const [lancamentos, setLancamentos] = useState<Lancamento[]>([]);
  const [saldoDinheiro, setSaldoDinheiro] = useState(0);
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [itensPorPagina] = useState(25);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [loading, setLoading] = useState(false);
  const [editIdx, setEditIdx] = useState<number | null>(null);
  const [editData, setEditData] = useState<Lancamento | null>(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const fetchFechamentoCaixa = async () => {
  try {
    const response = await api.get("/fechamento-caixa/");
    setSaldoDinheiro(response.data.saldo_total_dinheiro); // Ex.: -1190
  } catch (error) {
    console.error("Erro ao carregar fechamento de caixa:", error);
    setSuccessMsg("Erro ao carregar saldo de caixa!");
    setShowSuccess(true);
  }
};

useEffect(() => {
  fetchLancamentos();
  fetchFechamentoCaixa();
}, [paginaAtual]);

  // Mapeamento de TIPO e FORMA
  const mapTipo = (tipo: string) => (tipo === "E" ? "Entrada" : "Saída");
  const mapForma = (forma: string) => {
    switch (forma) {
      case "A": return "Pix";
      case "B": return "Dinheiro";
      case "C": return "Débito";
      case "D": return "Crédito";
      case "E": return "Carnê";
      case "F": return "Permuta";
      default: return forma;
    }
  };

  // Função para buscar lançamentos do endpoint
  const fetchLancamentos = async () => {
    setLoading(true);
    try {
      const response = await api.get("/dados-caixa/");
      console.log("Resposta do endpoint /dados-caixa/:", response.data);

      // A resposta é um array direto
      const lancamentosMapeados = response.data.map((item: any) => {
        // Converte a data manualmente para garantir 09/07/2025
        const [year, month, day] = item.DATA.split("-");
        const formattedDate = `${day}/${month}/${year}`;
        return {
          id: item.id,
          data: formattedDate,
          descricao: item.DESCRICAO.replace(/\r\n/g, "").trim(),
          os: item.REFERENCIA ? String(item.REFERENCIA) : "",
          tipo: mapTipo(item.TIPO),
          valor: String(item.VALOR),
          forma: mapForma(item.FORMA),
        };
      });
      setLancamentos(lancamentosMapeados);
      setTotalPaginas(Math.ceil(response.data.length / itensPorPagina));
    } catch (error) {
      console.error("Erro ao carregar lançamentos:", error);
      setSuccessMsg("Erro ao carregar lançamentos!");
      setShowSuccess(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLancamentos();
  }, [paginaAtual]);

  useEffect(() => {
    if (showSuccess || successMsg) {
      const timer = setTimeout(() => {
        setShowSuccess(false);
        setSuccessMsg(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess, successMsg]);

  // Cálculo dos totais baseado em todos os lançamentos
  const totalEntradas = lancamentos
    .filter((l) => l.tipo === "Entrada")
    .reduce((acc, l) => acc + Number(l.valor.replace(/[^\d,.-]/g, "").replace(",", ".")), 0);


  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");


 const handleFechaCaixa = async () => {
    try {
      setLoading(true);
      setMensagem("");

      // Faz a requisição para o endpoint com responseType: 'blob'
      const response = await api.get("/fechar_caixa", {
  
      });

      const url = (response.data);

      // Cria um link temporário para download
      const link = document.createElement("a");
      link.href = url;
      link.click();

      setMensagem("Fechado com sucesso!");
      window.location.assign("caixa");
      setTimeout(() => setMensagem(""), 2500);
    } catch (e) {
      setMensagem("Erro ao baixar o relatório. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };
 



  return (
    <div className="relative bg-white dark:bg-gray-900 py-8 px-4 flex flex-col items-center transition-colors duration-300">
      {/* Mensagem de feedback fixa logo abaixo da navbar */}
      {successMsg && (
        <div
          className={`fixed left-1/2 transform -translate-x-1/2 px-6 py-2 rounded shadow-lg z-50 text-sm font-medium ${
            successMsg.includes("Erro") ? "bg-red-500 text-white" : "bg-green-500 text-white"
          }`}
          style={{ top: 88 }}
        >
          {successMsg}
        </div>
      )}
      {/* Linha de topo com botões compactos e espaçados */}
      <div className="w-full max-w-5xl mx-auto flex mb-4 gap-2 justify-between flex-wrap items-center">
        <button
          className="bg-blue-700 hover:bg-blue-800 text-white rounded-md px-3 py-1.5 h-8 text-sm font-semibold shadow flex-1 sm:flex-none min-w-[140px]"
          onClick={() => navigate("/caixa-mes")}
        >
          Meses anteriores
        </button>
      </div>

      {/* Tabela de lançamentos */}
      <div
        id="caixa-scroll"
        className="w-full max-w-5xl mx-auto overflow-auto max-h-[70vh] min-h-[300px] custom-scrollbar-hide rounded-xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 xl:pr-[320px]"
      >
        <style>{`
          #caixa-scroll::-webkit-scrollbar { display: none !important; }
          #caixa-scroll { -ms-overflow-style: none !important; scrollbar-width: none !important; }
        `}</style>
        {loading ? (
          <div className="text-center py-6 text-gray-500 dark:text-gray-400">Carregando...</div>
        ) : (
          <table className="min-w-[800px] w-full text-xs sm:text-sm text-left text-gray-900 dark:text-white">
            <thead>
              <tr className="bg-blue-50 dark:bg-gray-900">
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[80px]">
                  DATA
                </th>
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[120px]">
                  DESCRIÇÃO
                </th>
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[60px]">
                  OS
                </th>
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[70px]">
                  TIPO
                </th>
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[90px]">
                  VALOR
                </th>
                <th className="px-2 sm:px-4 py-2 sm:py-3 text-left text-xs font-bold text-gray-700 dark:text-white uppercase tracking-wider border-b border-gray-200 dark:border-gray-700 min-w-[80px]">
                  FORMA
                </th>
              </tr>
            </thead>
            <tbody>
              {lancamentos.length === 0 && (
                <tr>
                  <td
                    colSpan={7}
                    className="text-center py-6 text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 rounded-b-xl"
                  >
                    Nenhum lançamento cadastrado.
                  </td>
                </tr>
              )}
              {lancamentos.map((l, idx) => (
                <tr
                  key={l.id}
                  className={`transition ${idx % 2 === 0 ? "bg-white dark:bg-gray-800" : "bg-blue-50 dark:bg-gray-900"} hover:bg-blue-100 dark:hover:bg-gray-700`}
                >
                  {editIdx === idx ? (
                    <>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <input
                          className="form-input w-full text-black"
                          value={editData?.data || ""}
                          onChange={(e) => setEditData((d) => (d ? { ...d, data: e.target.value } : d))}
                        />
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <input
                          className="form-input w-full text-black"
                          value={editData?.descricao || ""}
                          onChange={(e) => setEditData((d) => (d ? { ...d, descricao: e.target.value } : d))}
                        />
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <input
                          className="form-input w-full text-black"
                          value={editData?.os || ""}
                          onChange={(e) => setEditData((d) => (d ? { ...d, os: e.target.value } : d))}
                        />
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <select
                          className="form-input w-full text-black"
                          value={editData?.tipo || ""}
                          onChange={(e) => setEditData((d) => (d ? { ...d, tipo: e.target.value } : d))}
                        >
                          <option value="Entrada">Entrada</option>
                          <option value="Saída">Saída</option>
                        </select>
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <input
                          className="form-input w-full text-black"
                          value={editData?.valor || ""}
                          onChange={(e) => {
                            let v = e.target.value.replace(/[^\d,.-]/g, "").replace(",", ".");
                            v = Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
                            setEditData((d) => (d ? { ...d, valor: v } : d));
                          }}
                        />
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700">
                        <select
                          className="form-input w-full text-black"
                          value={editData?.forma || ""}
                          onChange={(e) => setEditData((d) => (d ? { ...d, forma: e.target.value } : d))}
                        >
                          <option value="Pix">Pix</option>
                          <option value="Dinheiro">Dinheiro</option>
                          <option value="Débito">Débito</option>
                          <option value="Crédito">Crédito</option>
                          <option value="Carnê">Carnê</option>
                          <option value="Permuta">Permuta</option>
                        </select>
                      </td>
                    </>
                  ) : (
                    <>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                        {l.data}
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                        {l.descricao}
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                       <Link to={`/os?id=${l.os}`} className="text-blue-600 dark:text-blue-400 hover:underline text-xs sm:text-sm">{l.os}</Link>
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                        {l.tipo}
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                        <Money value={l.valor} />
                      </td>
                      <td className="px-2 sm:px-4 py-2 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                        {l.forma}
                      </td>

                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Painel lateral responsivo */}
      <div className="hidden xl:block fixed top-[88px] right-12 w-[300px] z-40">
        <div className="mb-2">
          <div className="border border-indigo-500 rounded px-4 py-2 mb-2 text-center font-semibold bg-white dark:bg-gray-800">
            Saldo em dinheiro
            <div className="font-bold">
              <Money value={saldoDinheiro} />
            </div>
          </div>
          <div className="border border-indigo-500 rounded px-4 py-2 mb-2 text-center font-semibold bg-white dark:bg-gray-800">
            Total de entradas
            <div className="font-bold">
              <Money value={totalEntradas} />
            </div>
          </div>
        </div>
        <button className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded px-4 py-2 w-full shadow mb-2">
          Fechar Caixa
        </button>
        <button
          className="bg-green-600 hover:bg-green-700 text-white rounded px-4 py-2 w-full shadow font-semibold"
          onClick={() => setShowForm((v) => !v)}
        >
          {showForm ? "Cancelar" : "Adicionar Caixa"}
        </button>
        {showForm && (
          <div className="mt-4">
            <AdicionarCaixa
              onClose={() => setShowForm(false)}
              onSuccess={() => {
                setShowSuccess(true);
                setSuccessMsg("Caixa adicionado com sucesso!");
                fetchFechamentoCaixa(); 
                fetchLancamentos();
              }}
            />
          </div>
        )}
      </div>

      {/* Bloco normal abaixo da tabela em telas menores que xl */}
      <div className="block xl:hidden w-full max-w-5xl mx-auto mt-6">
        <div className="mb-2">
          <div className="border border-indigo-500 rounded px-1.5 py-1 mb-2 text-center font-semibold bg-white dark:bg-gray-800 text-xs">
            Saldo em dinheiro
            <div className="font-bold text-sm">
              <Money value={saldoDinheiro} />
            </div>
          </div>
          <div className="border border-indigo-500 rounded px-1.5 py-1 mb-2 text-center font-semibold bg-white dark:bg-gray-800 text-xs">
            Total de entradas
            <div className="font-bold text-sm">
              <Money value={totalEntradas} />
            </div>
          </div>
        </div>
        <div className="relative flex flex-col gap-2 mb-2 justify-center">
          <button onClick={handleFechaCaixa} className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-bold rounded px-2 py-1 w-full shadow text-xs mb-1">
            Fechar Caixa
          </button>
          <button
            className="bg-green-600 hover:bg-green-700 text-white rounded px-2 py-1 w-full shadow text-xs font-semibold"
            onClick={() => setShowForm((v) => !v)}
          >
            {showForm ? "Cancelar" : "Adicionar Caixa"}
          </button>
        </div>
        {showForm && (
          <div className="mt-4">
            <AdicionarCaixa
              onClose={() => setShowForm(false)}
              onSuccess={() => {
                setShowSuccess(true);
                setSuccessMsg("Caixa adicionado com sucesso!");
                fetchLancamentos();
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Caixa;