import React from "react";
import { Link } from "react-router-dom";

interface OrdemServico {
    id: number;
    servico: number | string;
    cliente: number | string;
    vendedor: number | string;
    lentes: string;
    dataPedido: string;
    status: string;
    telefone: string;
    previsaoEntrega: string;
}

interface PesquisaTableProps {
    paginated: OrdemServico[];
    servicosMap: Record<number, string>;
    clientesMap: Record<number, string>;
    vendedoresMap: Record<number, string>;
}

const statusLabel = (status: string) => {
    switch (status) {
        case "A": return <span className="bg-gray-500 text-white px-2 py-1 rounded text-xs">SOLICITADO</span>;
        case "E": return <span className="bg-green-600 text-white px-2 py-1 rounded text-xs">ENTREGUE</span>;
        case "C": return <span className="bg-red-600 text-white px-2 py-1 rounded text-xs">CANCELADO</span>;
        case "L": return <span className="bg-blue-600 text-white px-2 py-1 rounded text-xs">LABORATÓRIO</span>;
        case "F": return <span className="bg-gray-900 text-white px-2 py-1 rounded text-xs">FINALIZADO</span>;
        case "J": return <span className="bg-yellow-400 text-gray-900 px-2 py-1 rounded text-xs">LOJA</span>;
        default: return null;
    }
};

const PesquisaTable: React.FC<PesquisaTableProps> = ({ paginated, servicosMap, clientesMap, vendedoresMap }) => (
    <div className="hidden md:block pr-2 xl:pr-8">
        <div className="overflow-auto rounded-xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <table className="min-w-full w-full text-xs sm:text-sm text-left text-gray-900 dark:text-white">
                <thead>
                    <tr>
                        <th className="px-2 sm:px-4 py-2">OS</th>
                        <th className="px-2 sm:px-4 py-2">SERVIÇO</th>
                        <th className="px-2 sm:px-4 py-2">CLIENTE</th>
                        <th className="px-2 sm:px-4 py-2">VENDEDOR</th>
                        <th className="px-2 sm:px-4 py-2">LENTES</th>
                        <th className="px-2 sm:px-4 py-2">DATA PEDIDO</th>
                        <th className="px-2 sm:px-4 py-2">STATUS</th>
                        <th className="px-2 sm:px-4 py-2">N° Contato</th>
                        <th className="px-2 sm:px-4 py-2">PREVISÃO ENTREGA</th>
                        <th className="px-2 sm:px-4 py-2">AÇÃO</th>
                    </tr>
                </thead>
                <tbody>
                    {paginated.map(os => (
                        <tr key={os.id} className="hover:bg-gray-100 dark:hover:bg-gray-700 transition block md:table-row">
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['ID:'] md:before:content-none">{os.id}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Serviço:'] md:before:content-none">{servicosMap[Number(os.servico)] || os.servico}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Cliente:'] md:before:content-none">{clientesMap[Number(os.cliente)] || os.cliente}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Vendedor:'] md:before:content-none">{vendedoresMap[Number(os.vendedor)] || os.vendedor}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Lentes:'] md:before:content-none">{os.lentes}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Data Pedido:'] md:before:content-none">{os.dataPedido}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Status:'] md:before:content-none">{statusLabel(os.status)}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['N° Contato:'] md:before:content-none">
                                <div className="flex items-center gap-1 sm:gap-2">
                                    {os.telefone}
                                    <a
                                        href={`https://wa.me/55${os.telefone.replace(/\D/g, "")}?text=Olá! ${clientesMap[Number(os.cliente)] || os.cliente}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <img
                                            width="18"
                                            height="18"
                                            src="https://img.icons8.com/color/48/whatsapp--v1.png"
                                            alt="WhatsApp"
                                        />
                                    </a>
                                </div>
                            </td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Previsão Entrega:'] md:before:content-none">{os.previsaoEntrega}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Ação:'] md:before:content-none">
                                <Link
                                    to={`/os?id=${os.id}`}
                                    className="text-blue-600 dark:text-blue-400 hover:underline text-xs sm:text-sm"
                                >
                                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12s3.75-7.5 9.75-7.5 9.75 7.5 9.75 7.5-3.75 7.5-9.75 7.5S2.25 12 2.25 12z" />
                                            <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="1.5" fill="none" />
                                        </svg>
                                </Link>
                            </td>
                        </tr>
                    ))}
                    {paginated.length === 0 && (
                        <tr>
                            <td colSpan={10} className="px-2 sm:px-4 py-8 text-center text-gray-500 dark:text-gray-300 text-xs sm:text-sm">
                                Nenhuma O.S encontrada.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    </div>
);

export default PesquisaTable;
