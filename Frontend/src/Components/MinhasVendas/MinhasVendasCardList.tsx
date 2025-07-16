import React from "react";

interface Venda {
    os: number | string;
    tipo: string;
    descricao: string;
    valor: number | string;
    forma: string;
    data: string;
}

interface MinhasVendasCardListProps {
    paginated: Venda[];
}

const MinhasVendasCardList: React.FC<MinhasVendasCardListProps> = ({ paginated }) => (
    <div className="md:hidden">
        {paginated.map((v, idx) => (
            <div key={idx} className="bg-white dark:bg-gray-800 rounded-lg shadow p-3 mb-3 text-xs sm:text-sm">
                <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-blue-700 dark:text-blue-300">OS #{v.os}</span>
                    <span className="bg-green-600 text-white px-2 py-1 rounded text-xs">{v.tipo}</span>
                </div>
                <div className="mb-0.5"><span className="font-semibold">Descrição:</span> {v.descricao}</div>
                <div className="mb-0.5"><span className="font-semibold">Valor:</span> {v.valor}</div>
                <div className="mb-0.5"><span className="font-semibold">Forma:</span> {v.forma}</div>
                <div className="mb-0.5"><span className="font-semibold">Data:</span> {v.data}</div>
            </div>
        ))}
        {paginated.length === 0 && (
            <div className="px-2 py-6 text-center text-gray-500 dark:text-gray-300 bg-white dark:bg-gray-800 rounded-lg shadow text-xs">
                Nenhuma venda encontrada.
            </div>
        )}
    </div>
);

export default MinhasVendasCardList;
