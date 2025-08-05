import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useRelatorios } from "./hooks/useRelatorios";
import api from "../../utils/axiosConfig";





const Relatorios: React.FC = () => {
    const {
    clientes,
    funcionariosMes,
    osEmAberto,
    receberHoje,
    vendasChartRef,
    fluxoChartRef,
    } = useRelatorios();

const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");


  const handleGerarOs = async () => {
  try {
    setLoading(true);
    setErro("");
    setMensagem("");

    // Faz a requisição para o endpoint com responseType: 'blob'
    const response = await api.get("/export_os", {
      responseType: "blob", // Para receber dados binários (Excel)
    });

    // Cria um objeto Blob a partir da resposta
    const blob = new Blob(
      [response.data],
      {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      }
    );

    // Cria um URL temporário para o Blob
    const url = window.URL.createObjectURL(blob);

    // Cria um link temporário para download
    const link = document.createElement("a");
    link.href = url;
    link.download = "relatorio_ordens_servico.xlsx"; // Nome apropriado
    document.body.appendChild(link);
    link.click();

    // Limpeza
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    setMensagem("Relatório baixado com sucesso!");
    setTimeout(() => setMensagem(""), 2500);
  } catch (e) {
    console.error("Erro ao baixar relatório:", e);
    setErro("Erro ao baixar o relatório. Tente novamente.");
  } finally {
    setLoading(false);
  }
};

    const handleExportarClientes = async () => {
      try {
        setLoading(true);
        setErro("");
        setMensagem("");

        // Requisição para o endpoint que exporta os clientes
        const response = await api.get("/export_clientes", {
          responseType: "blob", // Importante para arquivos binários como Excel
        });

        // Cria o Blob com o tipo correto para Excel
        const blob = new Blob(
          [response.data],
          {
            type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          }
        );

        // Cria URL temporária para o arquivo
        const url = window.URL.createObjectURL(blob);

        // Cria o link e simula o clique para download
        const link = document.createElement("a");
        link.href = url;
        link.download = "clientes.xlsx"; // Nome do arquivo
        document.body.appendChild(link);
        link.click();

        // Limpa os recursos
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        setMensagem("Arquivo de clientes exportado com sucesso!");
        setTimeout(() => setMensagem(""), 2500);
      } catch (e) {
        console.error("Erro ao exportar clientes:", e);
        setErro("Erro ao exportar clientes. Tente novamente.");
      } finally {
        setLoading(false);
      }
    };


    return (
        <div className="w-full min-w-0 py-0 px-2 sm:px-4 md:px-8 transition-colors duration-300 dark:text-white bg-white dark:bg-[#181a20]">
            {/* Barra de botões colada no topo */}
            <div className="flex gap-2 px-2 md:px-4 xl:px-8 pt-6 pb-3 sticky top-0 z-10 bg-transparent mb-0">
                <button className="rounded-t-md rounded-b-none px-4 py-2 font-semibold text-white bg-green-500 hover:bg-green-600 focus:bg-green-700 border-0 shadow-none transition-all min-w-[110px] text-xs md:text-sm" onClick={handleExportarClientes}>Exportar Clientes</button>
                <button className="rounded-t-md rounded-b-none px-4 py-2 font-semibold text-white bg-cyan-400 hover:bg-cyan-500 focus:bg-cyan-600 border-0 shadow-none transition-all min-w-[110px] text-xs md:text-sm" onClick={handleGerarOs}>Exportar Os</button>
            </div>
            {/* Box Funcionários do mês */}
        {/* Box Funcionários do Mês (Card) */}
      <div className="mb-4 px-2 md:px-4 xl:px-8">
        <div className="border rounded-lg shadow bg-white dark:bg-gray-900 p-3 md:p-4 mx-auto max-w-[900px]">
          <h5 className="text-center font-semibold mb-2 text-base md:text-lg dark:text-gray-100">
            Funcionários do Mês
          </h5>
          {funcionariosMes.length > 0 ? (
            funcionariosMes.map((f, i) => (
              <div key={i} className="text-center text-xs md:text-base dark:text-gray-200">
                {f.nome}: {f.pedidos} Pedidos R$ {f.vendas.toLocaleString("pt-BR", { minimumFractionDigits: 2 })} em
                Vendas, Ticket Médio R$ {f.ticket.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
              </div>
            ))
          ) : (
            <div className="text-center text-xs md:text-base dark:text-gray-200">
              Nenhum dado de vendedores disponível.
            </div>
          )}
        </div>
      </div>

            {/* Cards de resumo */}
            <div className="flex flex-col md:flex-row gap-4 md:gap-6 justify-between items-stretch mb-5 px-0 md:px-0 xl:px-0 min-w-0 overflow-x-auto">
                <div className="flex-1 min-w-0 md:min-w-[220px] max-w-[320px]">
                    <div className="rounded-lg shadow text-white bg-[#1677ff] h-full min-h-[120px] flex flex-col justify-center">
                        <div className="flex flex-col justify-center items-center py-3 md:py-4 gap-1 md:gap-2">
                            <h5 className="font-bold text-base md:text-lg mb-1 dark:text-white">Ordens De Serviço Em Aberto Mês</h5>
                            <div className="dark:text-blue-100 text-xs md:text-base">Total de Vendas: {osEmAberto.total_vendas}</div>
                            <div className="dark:text-blue-100 text-xs md:text-base">Total de Valor: R$ {osEmAberto.total_valor}</div>
                        </div>
                    </div>
                </div>
                <div className="flex-1 min-w-0 md:min-w-[220px] max-w-[320px]">
                    <div className="rounded-lg shadow text-white bg-[#b28704] h-full min-h-[120px] flex flex-col justify-center">
                        <div className="flex flex-col justify-center items-center py-3 md:py-4 gap-1 md:gap-2">
                            <h5 className="font-bold text-base md:text-lg mb-1 dark:text-white">Total de Clientes Cadastrados</h5>
                            <div className="dark:text-yellow-100 text-xs md:text-base">Ativos: {clientes}</div>
                        </div>
                    </div>
                </div>
                <div className="flex-1 min-w-0 md:min-w-[220px] max-w-[320px]">
                    <div className="rounded-lg shadow text-white bg-[#198754] h-full min-h-[120px] flex flex-col justify-center">
                        <div className="flex flex-col justify-center items-center py-3 md:py-4 gap-1 md:gap-2">
                            <h5 className="font-bold text-base md:text-lg mb-1 dark:text-white">Receber Hoje</h5>
                            <div className="dark:text-green-100 text-xs md:text-base">R$ {receberHoje.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}</div>
                        </div>
                    </div>
                </div>
            </div>
            {/* Gráficos */}
            <div className="flex flex-col md:flex-row gap-6 mb-5 px-0 md:px-0 xl:px-0 min-w-0 overflow-x-auto">
                <div className="flex-1 bg-transparent min-w-0">
                    <h1 className="text-center mb-2 font-bold dark:text-white text-lg md:text-xl">Total de Vendas nos ultimos 12 Meses:</h1>
                    <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-2">
                        <canvas ref={vendasChartRef} height={240} style={{ minHeight: 180, height: 240 }} className="w-full max-w-full" />
                    </div>
                </div>
                <div className="flex-1 bg-transparent min-w-0">
                    <h1 className="text-center mb-2 font-bold dark:text-white text-lg md:text-xl">Fluxo de Caixa Mensal nos ultimos 12 Meses:</h1>
                    <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-2">
                        <canvas ref={fluxoChartRef} height={240} style={{ minHeight: 180, height: 240 }} className="w-full max-w-full" />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Relatorios;
