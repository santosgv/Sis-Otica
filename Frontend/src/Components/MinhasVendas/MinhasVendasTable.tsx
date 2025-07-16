import React from "react";

interface Venda {
    data: string;
    descricao: string;
    os: string | number;
    valor: string | number;
    forma: string;
}

interface MinhasVendasTableProps {
    paginated: Venda[];
}

const MinhasVendasTable: React.FC<MinhasVendasTableProps> = ({ paginated }) => (
    <div className="hidden md:block pr-2 xl:pr-8">
        <div className="overflow-auto rounded-xl shadow bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
            <table className="min-w-full w-full text-xs sm:text-sm text-left text-gray-900 dark:text-white">
                <thead>
                    <tr>
                        <th className="px-2 sm:px-4 py-2">Data</th>
                        <th className="px-2 sm:px-4 py-2">Descrição</th>
                        <th className="px-2 sm:px-4 py-2">OS</th>
                        <th className="px-2 sm:px-4 py-2">Valor</th>
                        <th className="px-2 sm:px-4 py-2">Forma</th>
                    </tr>
                </thead>
                <tbody>
                    {paginated.map((v, idx) => (
                        <tr key={idx} className="hover:bg-gray-100 dark:hover:bg-gray-700 transition block md:table-row">
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Data:'] md:before:content-none border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">{v.data}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Descrição:'] md:before:content-none border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">{v.descricao}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['OS:'] md:before:content-none border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">{v.os}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Valor:'] md:before:content-none border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">{v.valor}</td>
                            <td className="px-2 sm:px-4 py-2 block md:table-cell before:content-['Forma:'] md:before:content-none border-b border-gray-200 dark:border-gray-700 whitespace-nowrap">{v.forma}</td>
                        </tr>
                    ))}
                    {paginated.length === 0 && (
                        <tr>
                            <td colSpan={5} className="px-2 sm:px-4 py-8 text-center text-gray-500 dark:text-gray-400 text-xs sm:text-sm">
                                Nenhuma venda encontrada.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    </div>
);

export default MinhasVendasTable;
