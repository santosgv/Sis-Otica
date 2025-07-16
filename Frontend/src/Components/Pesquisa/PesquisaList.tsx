import React from "react";
import PesquisaFilters from "./PesquisaFilters";
import PesquisaTable from "./PesquisaTable";
import PesquisaCardList from "./PesquisaCardList";
import PesquisaPagination from "./PesquisaPagination";
import { usePesquisaList } from "./hooks/usePesquisaList";

const Pesquisa: React.FC = () => {
    const {
        loading, error,
        clientesMap, vendedoresMap, servicosMap,
        searchCliente, setSearchCliente,
        searchOS, setSearchOS,
        status, setStatus,
        dataInicio, setDataInicio,
        dataFim, setDataFim,
        currentPage, setCurrentPage,
        pageSize, setPageSize,
        PAGE_SIZE_OPTIONS,
        totalPages,
        paginated
    } = usePesquisaList();

    if (loading) return <div className="p-8 text-center">Carregando...</div>;
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

    return (
        <section className="w-full min-w-0 min-h-[calc(100vh-80px)] bg-gray-50 dark:bg-gray-900 transition-colors py-3 sm:py-6 font-inter">
            {/* Título centralizado no topo */}
            <h1 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-white">Pesquisa de Ordens de Serviço</h1>
            <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 flex flex-col flex-1">
                <div className="w-full flex flex-col flex-1 md:pr-8 md:pl-2 xl:pr-16 xl:pl-6">
                    <PesquisaFilters
                        searchCliente={searchCliente} setSearchCliente={setSearchCliente}
                        searchOS={searchOS} setSearchOS={setSearchOS}
                        status={status} setStatus={setStatus}
                        dataInicio={dataInicio} setDataInicio={setDataInicio}
                        dataFim={dataFim} setDataFim={setDataFim}
                    />
                    <div className="overflow-x-auto">
                        <PesquisaCardList paginated={paginated} servicosMap={servicosMap} clientesMap={clientesMap} vendedoresMap={vendedoresMap} />
                        <PesquisaTable paginated={paginated} servicosMap={servicosMap} clientesMap={clientesMap} vendedoresMap={vendedoresMap} />
                    </div>
                    <PesquisaPagination
                        currentPage={currentPage}
                        setCurrentPage={setCurrentPage}
                        totalPages={totalPages}
                        pageSize={pageSize}
                        setPageSize={setPageSize}
                        PAGE_SIZE_OPTIONS={PAGE_SIZE_OPTIONS}
                    />
                </div>
            </div>
        </section>
    );
};

export default Pesquisa;