import React from "react";

interface PesquisaFiltersProps {
    searchCliente: string;
    setSearchCliente: (v: string) => void;
    searchOS: string;
    setSearchOS: (v: string) => void;
    status: string;
    setStatus: (v: string) => void;
    dataInicio: string;
    setDataInicio: (v: string) => void;
    dataFim: string;
    setDataFim: (v: string) => void;
}

const PesquisaFilters: React.FC<PesquisaFiltersProps> = ({
    searchCliente, setSearchCliente,
    searchOS, setSearchOS,
    status, setStatus,
    dataInicio, setDataInicio,
    dataFim, setDataFim
}) => (
    <div className="flex flex-col md:flex-row md:items-end gap-2 md:gap-4 bg-white dark:bg-gray-800 p-2 sm:p-4 rounded-lg shadow mb-4 sm:mb-6 w-full">
        <div className="flex flex-col gap-1 sm:gap-2 w-full md:w-auto min-w-0">
            <label className="text-[11px] sm:text-xs font-semibold text-gray-700 dark:text-gray-200">Cliente</label>
            <input
                type="search"
                placeholder="Cliente"
                value={searchCliente}
                onChange={e => setSearchCliente(e.target.value)}
                className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full min-w-0 focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <div className="flex flex-col gap-1 sm:gap-2 w-full md:w-auto min-w-0">
            <label className="text-[11px] sm:text-xs font-semibold text-gray-700 dark:text-gray-200">OS</label>
            <input
                type="search"
                placeholder="OS"
                value={searchOS}
                onChange={e => setSearchOS(e.target.value)}
                className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full min-w-0 focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <div className="flex flex-col gap-1 sm:gap-2 w-full md:w-auto min-w-0">
            <label className="text-[11px] sm:text-xs font-semibold text-gray-700 dark:text-gray-200">Status</label>
            <select
                value={status}
                onChange={e => setStatus(e.target.value)}
                className="form-select px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full min-w-0 focus:ring-2 focus:ring-blue-500"
            >
                <option value="">Status</option>
                <option value="A">SOLICITADO</option>
                <option value="E">ENTREGUE</option>
                <option value="C">CANCELADO</option>
                <option value="L">LABORATÓRIO</option>
                <option value="F">FINALIZADO</option>
                <option value="J">LOJA</option>
            </select>
        </div>
        <div className="flex flex-col gap-1 sm:gap-2 w-full md:w-auto min-w-0">
            <label className="text-[11px] sm:text-xs font-semibold text-gray-700 dark:text-gray-200">Data Início</label>
            <input
                type="date"
                value={dataInicio}
                onChange={e => setDataInicio(e.target.value)}
                className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full min-w-0 focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <div className="flex flex-col gap-1 sm:gap-2 w-full md:w-auto min-w-0">
            <label className="text-[11px] sm:text-xs font-semibold text-gray-700 dark:text-gray-200">Data Fim</label>
            <input
                type="date"
                value={dataFim}
                onChange={e => setDataFim(e.target.value)}
                className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full min-w-0 focus:ring-2 focus:ring-blue-500"
            />
        </div>
    </div>
);

export default PesquisaFilters;
