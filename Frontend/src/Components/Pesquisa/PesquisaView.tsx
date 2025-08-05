
import React, { useState, useEffect } from "react";
import { Link, useSearchParams,useNavigate } from "react-router-dom";
import { Button } from '../ui/Button';
import ImprimirOsButton from "./ImprimirOsButton";
import MoverParaLojaButton from "./MoverParaLojaButton";
import MoverParaEntregueButton from "./MoverParaEntregue";
import MoverParaLaboratorioButton from "./MoverParaLaboratorio";
import MoverParaCanceladoButton from "./MoverParaCanceladoButton"
import api from "../../utils/axiosConfig"

interface Cliente {
    id: number;
    NOME: string;
}

interface Vendedor {
    id: number;
    first_name: string;
}

interface Laboratorio {
  id: number;
  LABORATORIO: string; 
}



interface VisualizarOS {
    id: number;
    solicitar_avaliacao?: boolean;
    ANEXO?:  string | null;
    ASSINATURA: string  | null;
    DATA_SOLICITACAO: string;
    PREVISAO_ENTREGA: string;
    VENDEDOR: Vendedor;
    CLIENTE: Cliente | string;
    SERVICO: string;
    LABORATORIO: Laboratorio;
    OD_ESF: string;
    OD_CIL: string;
    OD_EIXO: string;
    OE_ESF: string;
    OE_CIL: string;
    OE_EIXO: string;
    AD: string;
    DNP: string;
    P: string;
    DPA: string;
    DIAG: string;
    V: string;
    H: string;
    ALT: string;
    ARM: string;
    MONTAGEM: string;
    LENTES: string;
    ARMACAO: string;
    OBSERVACAO: string;
    FORMA_PAG: string;
    VALOR: string;
    QUANTIDADE_PARCELA: number;
    ENTRADA: string;
    STATUS: string;
}

interface OsViewProps {
    unidade?: string;
    VISUALIZAR_OS: VisualizarOS;
    messages?: { tags: string; message: string }[];
}

const statusLabels: Record<string, { label: string; className: string }> = {
    A: { label: "Solicitado", className: "bg-gray-500 text-white" },
    E: { label: "Entregue", className: "bg-green-500 text-white" },
    C: { label: "Cancelado", className: "bg-red-500 text-white" },
    L: { label: "Laboratório", className: "bg-blue-500 text-white" },
    J: { label: "Loja", className: "bg-yellow-500 text-gray-900" },
    F: { label: "Finalizado", className: "bg-gray-900 text-white" },
};

const formaPagLabels: Record<string, string> = {
    A: "Pix",
    B: "Dinheiro",
    C: "Débito",
    D: "Crédito",
    E: "Carnê",
    F: "Permuta",
};

const OsView: React.FC<OsViewProps> = ({ unidade = "", VISUALIZAR_OS, messages = [] }) => {
    const [editMode, setEditMode] = React.useState(false);
    const [osData, setOsData] = React.useState({ ...VISUALIZAR_OS });
    type Msg = { type: "success" | "error"; message: string } | null;
    const [showMsg, setShowMsg] = useState<Msg>(null);
    const navigate = useNavigate();

    React.useEffect(() => {
        setOsData({ ...VISUALIZAR_OS });
    }, [VISUALIZAR_OS]);


      const parseCurrency = (value: string): string => {
            if (!value) return "";
            const cleanValue = value.replace(/\./g, "").replace(",", ".");
            return cleanValue;
        };

        const formatCurrency = (value: string): string => {
        if (!value) return "";
        const cleanValue = value.replace(/\D/g, "");
        const numberValue = parseFloat((parseInt(cleanValue) / 100).toFixed(2));
        if (isNaN(numberValue)) return "";
        return numberValue.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
        });
    };

        function handleChange(
        e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
        ) {
        const { name, value } = e.target;
        let newValue = value;

        if (name === "VALOR" || name === "ENTRADA") {
            newValue = formatCurrency(value);
        }

        setOsData((prev: any) => ({ ...prev, [name]: newValue }));
        }




async function handleSave() {
  try {

        if (!["A", "B", "C", "D", "E", "F"].includes(osData.FORMA_PAG)) {
        alert("Forma de pagamento inválida.");
        return;
        }

    // Selecionar apenas os campos editáveis para enviar ao backend
    const updatedData = {
      PREVISAO_ENTREGA: osData.PREVISAO_ENTREGA,
      OD_ESF: osData.OD_ESF,
      OD_CIL: osData.OD_CIL,
      OD_EIXO: osData.OD_EIXO,
      OE_ESF: osData.OE_ESF,
      OE_CIL: osData.OE_CIL,
      OE_EIXO: osData.OE_EIXO,
      AD: osData.AD,
      DNP: osData.DNP,
      P: osData.P,
      DPA: osData.DPA,
      DIAG: osData.DIAG,
      V: osData.V,
      H: osData.H,
      ALT: osData.ALT,
      ARM: osData.ARM,
      MONTAGEM: osData.MONTAGEM,
      LENTES: osData.LENTES,
      OBSERVACAO: osData.OBSERVACAO,
      FORMA_PAG: osData.FORMA_PAG,
      VALOR: parseCurrency(osData.VALOR),
      QUANTIDADE_PARCELA: parseInt(osData.QUANTIDADE_PARCELA.toString(), 10) || 0,
      ENTRADA: parseCurrency(osData.ENTRADA)
    };  

    // Enviar requisição PATCH para atualizar apenas os campos editáveis
    await api.patch(`/ordens/${osData.id}/`, updatedData);

    setEditMode(false);
    setShowMsg({ type: 'success', message: 'Dados salvos com sucesso!' });
    setTimeout(() => setShowMsg(null), 2500);
  } catch (error: any) {
    console.error('Erro ao salvar os dados:', error);
    const errorMessage = error.response?.data?.detail || 'Erro ao salvar os dados. Tente novamente.';
    setShowMsg({ type: 'error', message: errorMessage });
    setTimeout(() => setShowMsg(null), 2500);
  }
}
    function handleCancelEdit() {
        setEditMode(false);
        setOsData({ ...VISUALIZAR_OS });
    }

 function formatLocalDate(dateStr: string | undefined): string {
  if (!dateStr) return "";
  const [year, month, day] = dateStr.slice(0, 10).split("-");
  return `${day}/${month}/${year}`;
}

    return (
<section className="min-h-screen w-full min-w-0 bg-gradient-to-br from-blue-50 via-white to-blue-100 dark:from-gray-900 dark:via-gray-950 dark:to-gray-900 flex flex-col justify-center items-center py-10 px-2 sm:px-4 md:px-8">
  <div className="w-full px-2 md:px-10">
    {/* Botão Voltar */}
    <div className="mb-4 flex justify-start">
      <Button type="button" variant="outline" className="px-4 py-2 font-semibold shadow" onClick={() => navigate(-1)}>
        ← Voltar
      </Button>
    </div>

    {/* Toast de sucesso */}
    {showMsg && (
      <div className="fixed top-6 left-1/2 -translate-x-1/2 z-50 p-4 rounded-xl border bg-green-100 text-green-800 border-green-200 dark:bg-green-900 dark:text-green-100 dark:border-green-700 text-center font-semibold shadow-lg min-w-[220px] max-w-[90vw]">
        Dados salvos com sucesso!
      </div>
    )}

    {/* Mensagens do backend */}
    {messages.length > 0 && (
      <div className="mb-6 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-4 rounded-xl border ${msg.tags === "error"
              ? "bg-red-100 text-red-800 border-red-200 dark:bg-red-900 dark:text-red-100 dark:border-red-700"
              : "bg-blue-50 text-blue-800 border-blue-100 dark:bg-blue-900 dark:text-blue-100 dark:border-blue-700"
              }`}
          >
            {msg.message}
          </div>
        ))}
      </div>
    )}

    {/* Alerta de avaliação */}
    {VISUALIZAR_OS.solicitar_avaliacao && (
      <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-900 p-4 rounded-xl flex items-center gap-2 shadow-sm dark:bg-yellow-900 dark:text-yellow-100 dark:border-yellow-700">
        <span className="text-xl">⚠️</span>
        <p>
          Como foi a experiência com esse cliente?{" "}
          <Link
            to={`/cliente/avaliar/${typeof VISUALIZAR_OS.CLIENTE === 'object' ? VISUALIZAR_OS.CLIENTE.id : ''}`}
            className="font-semibold text-yellow-900 underline hover:text-yellow-700 dark:text-yellow-200 dark:hover:text-yellow-100"
          >
            Clique aqui para avaliar
          </Link>.
        </p>
      </div>
    )}

    <div className="space-y-10">
      {/* Cabeçalho */}
      <div className="text-center">
        <h1 className="text-4xl font-extrabold text-blue-800 dark:text-white tracking-tight drop-shadow mb-2">
          {unidade}{osData.id}
        </h1>
        <div className="flex justify-center gap-4 text-sm text-blue-700 dark:text-blue-300">
          <span>Data Pedido: {formatLocalDate(osData.DATA_SOLICITACAO)}</span>
          <span>Previsão Entrega: {formatLocalDate(osData.PREVISAO_ENTREGA)}</span>
        </div>
      </div>

      {/* Botões de ação */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        {VISUALIZAR_OS.ANEXO && (
          <a
            href={VISUALIZAR_OS.ANEXO || "#"}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 text-center py-2 px-4 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors font-medium shadow dark:bg-blue-900 dark:text-blue-100 dark:hover:bg-blue-800"
          >
            Visualizar Anexo
          </a>
        )}
        {VISUALIZAR_OS.ASSINATURA && (
          <a
            href={VISUALIZAR_OS.ASSINATURA || "#"}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 text-center py-2 px-4 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors font-medium shadow dark:bg-blue-900 dark:text-blue-100 dark:hover:bg-blue-800"
          >
            Visualizar Assinatura
          </a>
        )}
      </div>

      {/* Grid principal de informações */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full">
        {/* Seção Cliente/Vendedor */}
        <div className="space-y-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow">
          <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 border-b pb-2 text-center">
            Informações do Cliente
          </h2>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Cliente</label>
              <Link
                to={`/cliente?id=${typeof osData.CLIENTE === 'object' ? osData.CLIENTE.id : ''}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600 hover:bg-blue-100 dark:hover:bg-gray-600 transition-colors cursor-pointer">
                  {typeof osData.CLIENTE === 'object' ? osData.CLIENTE.NOME : osData.CLIENTE}
                </div>
              </Link>
            </div>
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Vendedor</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {osData.VENDEDOR.first_name}
              </div>
            </div>
          </div>
        </div>

        {/* Seção Serviço/Laboratório */}
        <div className="space-y-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow">
          <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 border-b pb-2 text-center">
            Detalhes do Serviço
          </h2>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Tipo de Serviço</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {osData.SERVICO}
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Laboratório</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {String(osData.LABORATORIO)}
              </div>
            </div>
          </div>
        </div>

{/* Seção Dados Ópticos */}
<div className="space-y-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow sm:col-span-2">
  <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 border-b pb-2 text-center">
    Dados Ópticos
  </h2>
  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
    {[
      { label: "OD - ESF", name: "OD_ESF", value: osData.OD_ESF },
      { label: "OD - CIL", name: "OD_CIL", value: osData.OD_CIL },
      { label: "OD - EIXO", name: "OD_EIXO", value: osData.OD_EIXO },
      { label: "OE - ESF", name: "OE_ESF", value: osData.OE_ESF },
      { label: "OE - CIL", name: "OE_CIL", value: osData.OE_CIL },
      { label: "OE - EIXO", name: "OE_EIXO", value: osData.OE_EIXO },
      { label: "AD", name: "AD", value: osData.AD },
      { label: "DNP", name: "DNP", value: osData.DNP },
      { label: "P", name: "P", value: osData.P },
      { label: "DPA", name: "DPA", value: osData.DPA },
      { label: "DIAG", name: "DIAG", value: osData.DIAG },
      { label: "V", name: "V", value: osData.V },
      { label: "H", name: "H", value: osData.H },
      { label: "ALT", name: "ALT", value: osData.ALT },
      { label: "ARM", name: "ARM", value: osData.ARM },
    ].map(({ label, name, value }) => (
      <div key={label}>
        <label htmlFor={`input-${label.replace(/\s|\W/g, '').toLowerCase()}`} className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">
          {label}
        </label>
        {editMode ? (
          <input
            id={`input-${label.replace(/\s|\W/g, '').toLowerCase()}`}
            name={name}
            value={value || ""}
            onChange={handleChange}
            maxLength={10}
            className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none text-center"
          />
        ) : (
          <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600 text-center">
            {value || "-"}
          </div>
        )}
      </div>
    ))}
  </div>
</div>


        {/* Seção Pagamento */}
        <div className="space-y-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow sm:col-span-2">
          <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 border-b pb-2 text-center">
            Informações Financeiras
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Forma de Pagamento</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {formaPagLabels[osData.FORMA_PAG] || "-"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor Total</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {osData.VALOR ? `R$ ${parseFloat(osData.VALOR).toFixed(2)}` : "-"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Parcelas</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {osData.QUANTIDADE_PARCELA ? `${osData.QUANTIDADE_PARCELA}x` : "-"}
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor Pago</label>
              <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600">
                {osData.ENTRADA ? `R$ ${parseFloat(osData.ENTRADA).toFixed(2)}` : "-"}
              </div>
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Status</label>
              <div className="flex items-center">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold shadow ${statusLabels[osData.STATUS]?.className || "bg-gray-300 text-gray-800"}`}>
                  {statusLabels[osData.STATUS]?.label || "-"}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Seção Observações */}
        <div className="space-y-4 p-4 bg-white dark:bg-gray-800 rounded-xl shadow sm:col-span-2">
          <h2 className="text-lg font-semibold text-blue-800 dark:text-blue-200 border-b pb-2 text-center">
            Observações
          </h2>
          <div className="w-full bg-blue-50 dark:bg-gray-700 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-600 min-h-[80px]">
            {osData.OBSERVACAO || "Nenhuma observação registrada"}
          </div>
        </div>
      </div>

      {/* Botões de ação */}
      <div className="flex flex-wrap justify-center gap-4 mt-10">
        {!editMode ? (
          <Button type="button" variant="outline" className="px-5 py-2 font-semibold shadow" onClick={() => setEditMode(true)}>
            Editar
          </Button>
        ) : (
          <>
            <Button type="button" variant="primary" className="px-5 py-2 font-semibold shadow" onClick={handleSave}>
              Salvar
            </Button>
            <Button type="button" variant="outline" className="px-5 py-2 font-semibold shadow" onClick={handleCancelEdit}>
              Cancelar
            </Button>
          </>
        )}
        
        <ImprimirOsButton idOs={osData.id} />
        <MoverParaLojaButton idOs={osData.id} />
        <MoverParaLaboratorioButton idOs={osData.id} />
        <MoverParaEntregueButton idOs={osData.id} />
        <MoverParaCanceladoButton idOs={osData.id} />
      </div>
    </div>
  </div>
</section>
    );
};


const PesquisaView: React.FC = () => {
  const [searchParams] = useSearchParams();
  const id = searchParams.get("id");
  const [osData, setOsData] = useState<VisualizarOS | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [messages, setMessages] = useState<{ tags: string; message: string }[]>([]);

  useEffect(() => {
    const fetchOsData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Buscar dados da ordem
        const osResponse = await api.get(`/ordens/${id}/`);
        const os = osResponse.data;
      //  console.log("Ordem:", os); // Depuração

        // Buscar dados relacionados
        const [clienteResponse, vendedorResponse, servicoResponse, laboratorioResponse] = await Promise.all([
          api.get(`/clientes/${os.CLIENTE}/`).catch(() => ({
            data: { id: os.CLIENTE, NOME: "Cliente não encontrado" },
          })),
          api.get(`/usuarios/${os.VENDEDOR}/`).catch(() => ({
            data: { id: os.VENDEDOR, first_name: "Vendedor não encontrado" },
          })),
          api.get(`/servicos/${os.SERVICO}/`).catch(() => ({
            data: { id: os.SERVICO, SERVICO: "Serviço não encontrado" },
          })),
          api.get(`/laboratorios/${os.LABORATORIO}/`).catch(() => ({
            data: { id: os.LABORATORIO, NOME: "Laboratório não encontrado" },
          })),
         
        ]);

     //   console.log("Cliente:", clienteResponse.data); // Depuração
     //   console.log("Laboratório:", laboratorioResponse.data); // Depuração
     //   console.log("Vendedor:", vendedorResponse.data); // Depuração
     //   console.log("Serviço:", servicoResponse.data); // Depuração
        

        // Mapear os dados para o formato esperado por VisualizarOS
        const mappedOs: VisualizarOS = {
          id: os.id,
          DATA_SOLICITACAO: os.DATA_SOLICITACAO,
          PREVISAO_ENTREGA: os.PREVISAO_ENTREGA,
          VENDEDOR: {
            id: vendedorResponse.data.id,
            first_name: vendedorResponse.data.first_name || vendedorResponse.data.username || "Desconhecido",
          },
          CLIENTE: {
            id: clienteResponse.data.id,
            NOME: clienteResponse.data.NOME || "Desconhecido",
          },
          ARMACAO:os.ARMACAO,
          SERVICO: servicoResponse.data.SERVICO || "Desconhecido",
          LABORATORIO: laboratorioResponse.data.LABORATORIO || "Desconhecido",
          OD_ESF: os.OD_ESF || "",
          OD_CIL: os.OD_CIL || "",
          OD_EIXO: os.OD_EIXO || "",
          OE_ESF: os.OE_ESF || "",
          OE_CIL: os.OE_CIL || "",
          OE_EIXO: os.OE_EIXO || "",
          AD: os.AD || "",
          DNP: os.DNP || "",
          P: os.P || "",
          DPA: os.DPA || "",
          DIAG: os.DIAG || "",
          V: os.V || "",
          H: os.H || "",
          ALT: os.ALT || "",
          ARM: os.ARM || "",
          MONTAGEM: os.MONTAGEM || "",
          LENTES: os.LENTES || "",
          OBSERVACAO: os.OBSERVACAO || "",
          FORMA_PAG: os.FORMA_PAG || "",
          VALOR: os.VALOR || "",
          QUANTIDADE_PARCELA: os.QUANTIDADE_PARCELA || 0,
          ENTRADA: os.ENTRADA || "",
          STATUS: os.STATUS || "",
          ANEXO: os.ANEXO || null,
          ASSINATURA: os.ASSINATURA || null,
          solicitar_avaliacao: false, 
        };
        

        setOsData(mappedOs);
        setLoading(false);
      } catch (err) {
        setError("Erro ao carregar os dados da ordem.");
        setLoading(false);
      }
    };

    if (id) {
      fetchOsData();
    } else {
      setError("ID da ordem não fornecido.");
      setLoading(false);
    }
  }, [id]);

  if (loading) {
    return <div className="p-8 text-center text-blue-900 dark:text-blue-100">Carregando...</div>;
  }

  if (error || !osData) {
    return (
      <div className="p-8 text-center text-red-500 dark:text-red-400">
        {error || "Dados da ordem não disponíveis."}
      </div>
    );
  }

  return <OsView unidade="OS - " VISUALIZAR_OS={osData} messages={messages} />;
};
export default PesquisaView;