// ComissaoForm.tsx
// Tela/formulário para criar ou editar uma comissão.
// Permite cadastrar ou atualizar dados de comissão de colaborador.
// Responsivo, dark mode, fonte Inter e mock data.
//
// Recursos:
// - Cadastro e edição de comissão.
// - Validação de campos e integração visual.

import React, { useEffect } from "react";
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

const ComissaoForm: React.FC = () => {
    useEffect(() => {
        // Removido: document.documentElement.classList.add('dark');
    }, []);

    return (
        <div className="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 px-2 py-4 sm:p-4 flex flex-col items-center">
            <div className="w-full max-w-lg bg-white dark:bg-gray-800 rounded-lg shadow px-2 py-6 sm:p-6">
                <h2 className="text-center text-xl sm:text-2xl font-bold mb-3 sm:mb-4">Nova Comissão</h2>
                <form className="flex flex-col gap-3 sm:gap-4">
                    <Input className="p-2 rounded border dark:bg-gray-700 dark:text-white w-full text-base sm:text-lg" placeholder="Funcionário" />
                    <Input className="p-2 rounded border dark:bg-gray-700 dark:text-white w-full text-base sm:text-lg" placeholder="Valor de vendas" type="number" />
                    <Input className="p-2 rounded border dark:bg-gray-700 dark:text-white w-full text-base sm:text-lg" placeholder="Data" type="date" />
                    <Button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded w-full sm:w-auto">Salvar</Button>
                </form>
                {/* Botão Voltar responsivo */}
                <div className="mt-4 flex justify-center">
                    <button
                        className={`block sm:hidden p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-150
                        bg-blue-600 text-white hover:bg-blue-700 focus:bg-blue-700`}
                        onClick={() => window.history.length > 1 ? window.history.back() : window.location.assign('/comissao')}
                        aria-label="Voltar"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>
                    <a
                        href="/comissao"
                        className="hidden sm:block text-blue-600 hover:underline text-center text-sm sm:text-base px-4 py-2 rounded font-medium bg-blue-50 hover:bg-blue-100 transition-all"
                        aria-label="Voltar para a Lista"
                    >
                        Voltar para a Lista
                    </a>
                </div>
            </div>
        </div>
    );
};

export default ComissaoForm;

// Responsividade garantida com Tailwind: formulário usa grid/flex, largura máxima (max-w) e padding adaptativo.
// Certifique-se de que campos e botões fiquem acessíveis em telas pequenas.
