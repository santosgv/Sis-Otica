import React from "react";

interface PesquisaPaginationProps {
    currentPage: number;
    setCurrentPage: (v: number) => void;
    totalPages: number;
    pageSize: number;
    setPageSize: (v: number) => void;
    PAGE_SIZE_OPTIONS: number[];
}

const PesquisaPagination: React.FC<PesquisaPaginationProps> = ({
    currentPage, setCurrentPage, totalPages, pageSize, setPageSize, PAGE_SIZE_OPTIONS
}) => (
    <div className="flex flex-col md:flex-row justify-center items-center gap-2 sm:gap-4 mt-4 sm:mt-6 px-1 sm:px-2 w-full">
        <div className="flex items-center gap-1 sm:gap-2">
            <span className="text-[11px] sm:text-xs text-gray-600 dark:text-gray-300 font-medium">Itens por página:</span>
            <select
                value={pageSize}
                onChange={e => setPageSize(Number(e.target.value))}
                className="rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-2 sm:px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 transition text-xs sm:text-sm"
            >
                {PAGE_SIZE_OPTIONS.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                ))}
            </select>
        </div>
        <div className="flex items-center gap-1 sm:gap-2">
            <button
                className="px-2 sm:px-3 py-1 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 disabled:opacity-50 shadow-sm transition text-xs sm:text-sm"
                onClick={() => setCurrentPage(currentPage - 1)}
                disabled={currentPage === 1}
                aria-label="Página anterior"
            >
                &lt;
            </button>
            <span className="px-2 sm:px-3 py-1 text-gray-700 dark:text-gray-200 font-semibold rounded-lg bg-gray-100 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-sm text-xs sm:text-sm">
                Página {currentPage} de {totalPages}
            </span>
            <button
                className="px-2 sm:px-3 py-1 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 disabled:opacity-50 shadow-sm transition text-xs sm:text-sm"
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={currentPage === totalPages}
                aria-label="Próxima página"
            >
                &gt;
            </button>
        </div>
    </div>
);

export default PesquisaPagination;
