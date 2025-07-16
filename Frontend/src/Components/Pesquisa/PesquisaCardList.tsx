import React from "react";
import { Link } from "react-router-dom";

interface OS {
    id: number;
    status: string;
    servico: number | string;
    cliente: number | string;
    vendedor: number | string;
    lentes: string;
    dataPedido: string;
    telefone: string;
    previsaoEntrega: string;
}

interface PesquisaCardListProps {
    paginated: OS[];
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

const PesquisaCardList: React.FC<PesquisaCardListProps> = ({ paginated, servicosMap, clientesMap, vendedoresMap }) => (
    <div className="md:hidden">
        {paginated.map(os => (
            <div key={os.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-3 mb-3 text-xs sm:text-sm">
                <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-blue-700 dark:text-blue-300">OS #{os.id}</span>
                    <span>{statusLabel(os.status)}</span>
                </div>
                <div className="mb-0.5"><span className="font-semibold">Serviço:</span> {servicosMap[Number(os.servico)] || os.servico}</div>
                <div className="mb-0.5"><span className="font-semibold">Cliente:</span> {clientesMap[Number(os.cliente)] || os.cliente}</div>
                <div className="mb-0.5"><span className="font-semibold">Vendedor:</span> {vendedoresMap[Number(os.vendedor)] || os.vendedor}</div>
                <div className="mb-0.5"><span className="font-semibold">Lentes:</span> {os.lentes}</div>
                <div className="mb-0.5"><span className="font-semibold">Data Pedido:</span> {os.dataPedido}</div>
                <div className="mb-0.5 flex items-center gap-1"><span className="font-semibold">Contato:</span> {os.telefone}
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
                <div className="mb-0.5"><span className="font-semibold">Previsão Entrega:</span> {os.previsaoEntrega}</div>
                <div className="mt-1">
                    <Link
                        to={`/cadastro-os?id=${os.id}`}
                        className="text-blue-600 dark:text-blue-400 hover:underline text-xs"
                    >
                        Visualizar
                    </Link>
                </div>
            </div>
        ))}
        {paginated.length === 0 && (
            <div className="px-2 py-6 text-center text-gray-500 dark:text-gray-300 bg-white dark:bg-gray-800 rounded-lg shadow text-xs">
                Nenhuma O.S encontrada.
            </div>
        )}
    </div>
);

export default PesquisaCardList;
