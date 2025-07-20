// RealizaPagamento.tsx
// Tela principal de comissões: lista de colaboradores e pagamentos.
// Permite navegar para detalhes, editar, criar e excluir comissões.
// Responsivo, dark mode, fonte Inter e mock data.
//
// Recursos:
// - Listagem de comissões e ações de CRUD.
// - Integração com rotas de detalhes, edição e exclusão.

import React, { useEffect } from "react";

// Mock de dados para comissões
const comissoesMock = [
    {
        pk: 1,
        colaborador: "João Silva",
        valor_vendas: 10000,
        data_referencia: "2025-06-01",
    },
    {
        pk: 2,
        colaborador: "Maria Souza",
        valor_vendas: 8000,
        data_referencia: "2025-06-01",
    },
    // ...adicione mais mocks se quiser
];

// Tela principal de comissões: lista de colaboradores e pagamentos.
// Permite navegar para detalhes, editar, criar e excluir comissões.
// Responsivo, dark mode, fonte Inter e mock data.
// Responsividade garantida com Tailwind: listas, cards e tabelas usam breakpoints e overflow-x-auto.
// Certifique-se de que botões e ações fiquem acessíveis em telas pequenas.
const ComissaoList: React.FC = () => {
    useEffect(() => {
        // Removido: document.documentElement.classList.add('dark');
    }, []);

    return (
        <div className="w-full min-w-0 min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 p-2 sm:p-4 font-sans">
            <h2 className="text-center text-2xl font-bold mb-4">Comissão de Pagamento</h2>
            <div className="flex flex-col sm:flex-row justify-end mb-4 gap-2">
                <a href="/comissao/create" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow w-full sm:w-auto text-center">Nova Comissão</a>
            </div>
            <div className="overflow-x-auto rounded-lg">
                <table className="w-full text-xs sm:text-sm md:text-base table-auto bg-white dark:bg-gray-800 rounded shadow min-w-[400px]">
                    <thead>
                        <tr>
                            <th className="px-2 sm:px-4 py-2 border-b text-left">Funcionário</th>
                            <th className="px-2 sm:px-4 py-2 border-b text-left">Valor de vendas</th>
                            <th className="px-2 sm:px-4 py-2 border-b text-left">Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        {comissoesMock.map((comissao) => (
                            <tr key={comissao.pk} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                                    <a href={`/comissao/${comissao.pk}`} className="text-blue-600 hover:underline">{comissao.colaborador}</a>
                                </td>
                                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">R$ {comissao.valor_vendas.toLocaleString()}</td>
                                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">{comissao.data_referencia}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ComissaoList;
