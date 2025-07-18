
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
      ARMACAO: osData.ARMACAO,
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
        <section className="min-h-screen w-full min-w-0 bg-gradient-to-br from-blue-50 via-white to-blue-100 dark:from-gray-900 dark:via-gray-950 dark:to-gray-900 flex flex-col items-center py-10 px-2 sm:px-4 md:px-8">
            <div className="w-full px-2 md:px-10">
                {/* Botão Voltar */}
                <div className="mb-4 flex justify-start">
                    <Button type="button" variant="outline" className="px-4 py-2 font-semibold shadow" onClick={() => navigate(-1)}>
                        ← Voltar
                    </Button>
                </div>

                {/* Toast de sucesso fixo, nunca empurra o layout */}
                {showMsg && (
                    <div className="fixed top-6 left-1/2 -translate-x-1/2 z-50 p-4 rounded-xl border bg-green-100 text-green-800 border-green-200 dark:bg-green-900 dark:text-green-100 dark:border-green-700 text-center font-semibold shadow-lg min-w-[220px] max-w-[90vw]">
                        Dados salvos com sucesso!
                    </div>
                )}
                {/* Mensagens do backend (mantém no fluxo, pois podem ser múltiplas e não são toast) */}
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
                    <h1 className="text-4xl font-extrabold text-center text-blue-800 dark:text-white tracking-tight drop-shadow mb-8">
                        {unidade}{osData.id}
                    </h1>

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

                    {/* Grid responsivo, sem card, ocupando toda a largura */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 w-full">
                        {/* Data Pedido */}
                        <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Data Pedido</label>
                           
                                <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                                    {formatLocalDate(osData.DATA_SOLICITACAO)}
                                </div>
                            
                        </div>
                        {/* Previsão Entrega */}
                        <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Previsão Entrega</label>
                            {editMode ? (
                                <input
                                type="date"
                                name="PREVISAO_ENTREGA"
                                value={osData.PREVISAO_ENTREGA?.slice(0, 10) || ""}
                                onChange={handleChange}
                                min={new Date().toISOString().split("T")[0]}
                                className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                                required
                                />
                            ) : (
                                <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                                   {formatLocalDate(osData.PREVISAO_ENTREGA)}
                                </div>
                            )}
                        </div>
                        {/* Vendedor */}
                        <div>
                            <label htmlFor="vendedor-input" className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Vendedor</label>
                            <input
                                id="vendedor-input"
                                name="VENDEDOR"
                                readOnly
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={osData.VENDEDOR.first_name}
                            />
                        </div>
                        {/* Cliente */}
                        <div>
                            <label htmlFor="cliente-input" className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Cliente</label>
                            <Link
                                to={`/cliente?id=${typeof osData.CLIENTE === 'object' ? osData.CLIENTE.id : ''}`}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                <input
                                    id="cliente-input"
                                    name="CLIENTE"
                                    readOnly
                                    className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 hover:bg-blue-100 dark:hover:bg-gray-700 transition-colors cursor-pointer"
                                    value={typeof osData.CLIENTE === 'object' ? osData.CLIENTE.NOME : osData.CLIENTE}
                                />
                            </Link>
                        </div>
                        {/* Tipo de Serviço */}
                        <div>
                            <label htmlFor="servico-input" className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Tipo de Serviço</label>
                            <input
                                id="servico-input"
                                name="SERVICO"
                                readOnly
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={osData.SERVICO}
                                onChange={handleChange}
                            />
                        </div>
                        {/* Laboratório */}
                        <div>
                            <label htmlFor="laboratorio-input" className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Laboratório</label>
                            <input
                                id="laboratorio-input"
                                name="LABORATORIO"
                                readOnly
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={String(osData.LABORATORIO)}
                                onChange={handleChange}
                            />
                        </div>
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
                                className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none"
                                value={value}
                                onChange={handleChange}
                                maxLength={10}
                            />
                            ) : (
                            <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                                {value}
                            </div>
                            )}
                        </div>
                        ))}

                        {/* Montagem */}
                        <div>
                        <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Montagem</label>
                        {editMode ? (
                            <input
                            name="MONTAGEM"
                            className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none"
                            value={osData.MONTAGEM}
                            onChange={handleChange}
                            maxLength={20}
                            />
                        ) : (
                            <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                            {osData.MONTAGEM}
                            </div>
                        )}
                        </div>
                    {/* Lentes */}
                    <div>
                    <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Lentes</label>
                    {editMode ? (
                        <input
                        name="LENTES"
                        className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none"
                        value={osData.LENTES}
                        onChange={handleChange}
                        maxLength={150}
                        />
                    ) : (
                        <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                        {osData.LENTES}
                        </div>
                    )}
                    </div>
                    {/* Armação */}
                    <div>
                    <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Armação</label>
                    {editMode ? (
                        <input
                        name="ARMACAO"
                        className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none"
                        value={osData.ARMACAO}
                        onChange={handleChange}
                        maxLength={20}
                        />
                    ) : (
                        <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                        {osData.ARMACAO}
                        </div>
                    )}
                    </div>
               {/* Observação */}
                <div className="sm:col-span-2 md:col-span-4">
                <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Observação</label>
                {editMode ? (
                    <textarea
                    name="OBSERVACAO"
                    maxLength={80}
                    className="w-full bg-white dark:bg-gray-900 rounded-lg px-3 py-2 text-blue-900 dark:text-white border border-blue-300 dark:border-gray-600 focus:outline-none resize-none"
                    rows={2}
                    value={osData.OBSERVACAO}
                    onChange={handleChange}
                    />
                ) : (
                    <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                    {osData.OBSERVACAO}
                    </div>
                )}
                </div>
                        {/* Pagamento */}
                        <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Pagamento</label>
                           {editMode ? (
                            <select
                                name="FORMA_PAG"
                                className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                                value={osData.FORMA_PAG}
                                onChange={handleChange}
                            >
                                <option value="">Selecione</option>
                                {Object.entries(formaPagLabels).map(([key, label]) => (
                                <option key={key} value={key}>
                                    {label}
                                </option>
                                ))}
                            </select>
                            ) : (
                            <div className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700">
                                {formaPagLabels[osData.FORMA_PAG] || "-"}
                            </div>
                            )}

                        </div>
                        {/* Valor */}
                        { editMode ? (
                        <div>
                        <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor</label>
                        <input
                        type="text"
                        name="VALOR"
                        maxLength={10}
                        value={osData.VALOR || ""}
                        onChange={handleChange}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                        placeholder="0,00"
                        />
                        </div>):(
                            <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor</label>
                            <input
                                name="VALOR"
                                readOnly={!editMode}
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={osData.VALOR}
                                onChange={handleChange}
                            />
                        </div>
                        )}

                        {/* Parcelas */}
                        
                        <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Parcelas</label>
                        {editMode ? (
                            
                               <select
                            name="QUANTIDADE_PARCELA"
                            value={osData.QUANTIDADE_PARCELA || ""}
                            onChange={handleChange}
                            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                            required
                >
                  <option value="">Escolha...</option>
                  {Array.from({ length: 10 }, (_, i) => i + 1).map((num) => (
                    <option key={num} value={num}>
                      {num}x
                    </option>
                  ))}
                </select>
                        ): (   
                            <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Parcelas</label>
                            <input
                                name="QUANTIDADE_PARCELA"
                                readOnly={!editMode}
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={osData.QUANTIDADE_PARCELA + "x"}
                                onChange={handleChange}
                            />
                        </div>)
                    }
                     </div>
                        {/* Valor Pago */}
                        {editMode ? (                        
                            <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor Pago</label>
                            <input
                            type="text"
                            name="ENTRADA"
                            value={osData.ENTRADA || ""}
                            onChange={handleChange}
                            maxLength={10}
                            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                            placeholder="0,00"
                            />
                        </div>):(                       
                            <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Valor Pago</label>
                            <input
                                name="ENTRADA"
                                readOnly={!editMode}
                                className="w-full bg-blue-50 dark:bg-gray-800 rounded-lg px-3 py-2 text-blue-900 dark:text-blue-100 border border-blue-100 dark:border-gray-700 focus:outline-none"
                                value={osData.ENTRADA}
                                onChange={handleChange}
                            />
                        </div>)}

                        {/* Status */}
                        <div>
                            <label className="block text-sm font-semibold text-blue-900 dark:text-blue-100 mb-1">Status</label>
                            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold shadow ${statusLabels[osData.STATUS]?.className || "bg-gray-300 text-gray-800"}`}>
                                {statusLabels[osData.STATUS]?.label || "-"}
                            </span>
                        </div>
                    </div>
                    <div className="flex flex-wrap justify-center gap-4 mt-10">
                        {!editMode ? (
                            <Button type="button" variant="outline" className="px-5 py-2 font-semibold shadow" onClick={() => setEditMode(true)}>Editar</Button>
                        ) : (
                            <>
                                <Button type="button" variant="primary" className="px-5 py-2 font-semibold shadow" onClick={handleSave}>Salvar</Button>
                                <Button type="button" variant="outline" className="px-5 py-2 font-semibold shadow" onClick={handleCancelEdit}>Cancelar</Button>
                            </>
                        )}
                        
                                <ImprimirOsButton idOs={osData.id} />
                                <MoverParaLojaButton idOs={osData.id}  />
                                <MoverParaLaboratorioButton idOs={osData.id}  />
                                <MoverParaEntregueButton idOs={osData.id}  />
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
        console.log("Ordem:", os); // Depuração

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

        console.log("Cliente:", clienteResponse.data); // Depuração
        console.log("Laboratório:", laboratorioResponse.data); // Depuração
        console.log("Vendedor:", vendedorResponse.data); // Depuração
        console.log("Serviço:", servicoResponse.data); // Depuração

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
          SERVICO: servicoResponse.data.SERVICO || "Desconhecido",
          LABORATORIO: laboratorioResponse.data.LABORATORIO || "Desconhecido", // Ajuste conforme o campo retornado
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
          ARMACAO: os.ARMACAO || "",
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