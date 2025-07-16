// ComissaoDelete.tsx
// Tela de confirmação para exclusão de comissão.
// Exibe detalhes da comissão e solicita confirmação do usuário.
// Responsivo, dark mode, fonte Inter e mock data.
//
// Recursos:
// - Confirmação de exclusão de comissão.
// - Exibe detalhes antes de excluir.
// - Botões de ação para confirmar ou cancelar a exclusão.
// Responsividade garantida com Tailwind: modal de confirmação centralizado, largura máxima (max-w) e padding adaptativo.

import React, { useEffect } from "react";
import { Button } from '../ui/Button';

const ComissaoDelete: React.FC = () => {
    useEffect(() => {
        document.documentElement.classList.add('dark');
    }, []);

    return (
        <div className="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 px-2 py-4 sm:p-4 flex flex-col items-center justify-center">
            <div className="w-full max-w-lg bg-white dark:bg-gray-800 rounded-lg shadow px-2 py-6 sm:p-6">
                <h2 className="text-center text-xl sm:text-2xl font-bold mb-3 sm:mb-4">Excluir Comissão</h2>
                <p className="text-center mb-4 text-base sm:text-lg">Tem certeza de que deseja excluir "João Silva"?</p>
                <form className="text-center mb-4">
                    <Button type="submit" variant="danger" className="w-full sm:w-auto text-sm sm:text-base mr-0 sm:mr-2">Confirmar</Button>
                </form>
                <a href="/comissao" className="inline-flex items-center justify-center font-semibold rounded transition focus:outline-none focus:ring-2 focus:ring-offset-2 bg-blue-600 hover:bg-blue-700 text-white w-full sm:w-auto text-sm sm:text-base px-4 py-2">Cancelar</a>
            </div>
        </div>
    );
};

export default ComissaoDelete;
