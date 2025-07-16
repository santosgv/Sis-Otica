import React from "react";

interface MinhasVendasFiltersProps {
    search: string;
    setSearch: (v: string) => void;
    dataInicio: string;
    setDataInicio: (v: string) => void;
    dataFim: string;
    setDataFim: (v: string) => void;
}

const MinhasVendasFilters: React.FC<MinhasVendasFiltersProps> = ({
    search, setSearch, dataInicio, setDataInicio, dataFim, setDataFim
}) => (
    <div className="mb-4 flex flex-wrap gap-2 items-center w-full">
        <input
            type="text"
            className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full sm:w-1/3 md:w-1/4 min-w-[140px] focus:ring-2 focus:ring-blue-500"
            placeholder="Pesquisar por descrição, OS ou forma..."
            value={search}
            onChange={e => setSearch(e.target.value)}
        />
        <input
            type="date"
            className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full sm:w-auto min-w-[120px] focus:ring-2 focus:ring-blue-500"
            value={dataInicio}
            onChange={e => setDataInicio(e.target.value)}
        />
        <span className="self-center text-xs text-gray-500 dark:text-gray-400">até</span>
        <input
            type="date"
            className="form-input px-2 py-2 sm:px-3 sm:py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white text-xs sm:text-sm w-full sm:w-auto min-w-[120px] focus:ring-2 focus:ring-blue-500"
            value={dataFim}
            onChange={e => setDataFim(e.target.value)}
        />
    </div>
);

export default MinhasVendasFilters;
