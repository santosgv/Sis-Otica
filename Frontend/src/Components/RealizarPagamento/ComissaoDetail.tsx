// ComissaoDetail.tsx
// Tela de detalhes de uma comissão específica.
// Exibe informações do colaborador, valores e histórico.
// Responsivo, dark mode, fonte Inter e mock data.
//
// Recursos:
// - Visualização detalhada de comissão.
// - Exibe histórico e valores pagos.

// Responsividade garantida com Tailwind: detalhes e histórico usam grid/flex e overflow-x-auto para adaptação em telas pequenas.

import React, { useEffect } from "react";

const ComissaoDetail: React.FC = () => {
    useEffect(() => {
        document.documentElement.classList.add('dark');
    }, []);

    // Mock de dados
    const comissao = {
        pk: 1,
        colaborador: "João Silva",
        valor_vendas: 10000,
        data_referencia: "2025-06-01",
    };

    return (
        <div className="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 px-2 py-4 sm:p-4 flex flex-col items-center">
            <div className="w-full max-w-lg bg-white dark:bg-gray-800 rounded-lg shadow px-2 py-6 sm:p-6 overflow-x-auto">
                <h2 className="text-center text-xl sm:text-2xl font-bold mb-3 sm:mb-4">Detalhes da Comissão</h2>
                <div className="mb-2 text-base sm:text-lg">Mês: {comissao.data_referencia}</div>
                <div className="mb-2 text-base sm:text-lg">Venda Mensal: R$ {comissao.valor_vendas.toLocaleString()}</div>
                <div className="flex flex-col sm:flex-row gap-2 mt-4 justify-center">
                    <a href={`/comissao/${comissao.pk}/edit`} className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded w-full sm:w-auto text-sm sm:text-base">Editar</a>
                    <a href={`/comissao/${comissao.pk}/delete`} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded w-full sm:w-auto text-sm sm:text-base">Excluir</a>
                    <button
                        className="block sm:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150 bg-blue-600 text-white hover:bg-blue-700 focus:bg-blue-700"
                        onClick={() => window.history.length > 1 ? window.history.back() : window.location.assign('/comissao')}
                        aria-label="Voltar"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>
                    <a href="/comissao" className="hidden sm:block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded w-full sm:w-auto text-sm sm:text-base" aria-label="Voltar">Voltar</a>
                </div>
            </div>
        </div>
    );
};

export default ComissaoDetail;
