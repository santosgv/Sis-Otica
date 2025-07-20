// FolhaPagamento.tsx
// Atualizado para consumir dados da API real da folha de pagamento

import React, { useState, useEffect } from "react";
import api from   '../../utils/axiosConfig';


const funcaoLabel = (funcao?: string) => {
    if (funcao === "G") return "Gerente";
    if (funcao === "C") return "Caixa";
    if (funcao === "V") return "Vendedor";
    return "";
};

// Função utilitária para formatar valores monetários
function formatMoney(valor: number) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

const meses = [
    { label: "Janeiro", value: "01" },
    { label: "Fevereiro", value: "02" },
    { label: "Março", value: "03" },
    { label: "Abril", value: "04" },
    { label: "Maio", value: "05" },
    { label: "Junho", value: "06" },
    { label: "Julho", value: "07" },
    { label: "Agosto", value: "08" },
    { label: "Setembro", value: "09" },
    { label: "Outubro", value: "10" },
    { label: "Novembro", value: "11" },
    { label: "Dezembro", value: "12" },
];

const FolhaPagamento: React.FC = () => {
    const [funcionarios, setFuncionarios] = useState<{ id: number, nome: string, funcao: string }[]>([]);
    const [funcionarioSelecionado, setFuncionarioSelecionado] = useState<number | null>(null);
    const [anoSelecionado, setAnoSelecionado] = useState("2025");
    const [mesSelecionado, setMesSelecionado] = useState("07");
    const [folha, setFolha] = useState<any | null>(null);

    useEffect(() => {
        const fetchFuncionarios = async () => {
            try {
                const response = await api.get('/usuarios');
                console.log ('Usuários:', response.data.results);
                const data = response.data.results.map((user: any) => ({ id: user.id, nome: user.first_name, funcao: user.FUNCAO }));
                setFuncionarios(data);
                if (data.length > 0) setFuncionarioSelecionado(data[0].id);
            } catch (error) {
                console.error('Erro ao buscar usuários:', error);
            }
        };
        fetchFuncionarios();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            if (!funcionarioSelecionado) return;
            try {
                const referencia = `${anoSelecionado}-${mesSelecionado}`;
                const response = await api.get(`/folha/${funcionarioSelecionado}/${referencia}/`);
                setFolha(response.data);
            } catch (error) {
                console.error('Erro ao buscar folha:', error);
                setFolha(null);
            }
        };
        fetchData();
    }, [funcionarioSelecionado, anoSelecionado, mesSelecionado]);

    return (
        <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-6 bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors font-inter">
            <div className="flex flex-col md:flex-row gap-2 mb-6 w-full max-w-2xl">
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Funcionário</label>
                    <select
                        className="form-select w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={funcionarioSelecionado || ''}
                        onChange={e => setFuncionarioSelecionado(Number(e.target.value))}
                    >
                        {funcionarios.map(f => (
                            <option key={f.id} value={f.id}>{f.nome}</option>
                        ))}
                    </select>
                </div>
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Ano</label>
                    <input
                        type="number"
                        className="form-input w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={anoSelecionado}
                        onChange={e => setAnoSelecionado(e.target.value)}
                    />
                </div>
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Mês</label>
                    <select
                        className="form-select w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={mesSelecionado}
                        onChange={e => setMesSelecionado(e.target.value)}
                    >
                        {meses.map(m => (
                            <option key={m.value} value={m.value}>{m.label}</option>
                        ))}
                    </select>
                </div>
            </div>

            {!folha && <div className="text-center text-sm text-gray-500 dark:text-gray-300 my-8">Nenhuma folha encontrada para o período.</div>}

            {folha && (
                <div className="max-w-2xl grid gap-6">
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex flex-col gap-2">
                        <h5 className="text-lg font-semibold text-gray-800 dark:text-gray-100 text-center">
                            {folha.nome}- {funcaoLabel(folha.funcao)}
                        </h5>
                        <h6 className="text-lg font-semibold text-gray-800 dark:text-gray-100">Contratado em {folha.data_contratacao}</h6>

                        <div className="font-semibold">Salário Bruto: {formatMoney(folha.salario_bruto)}</div>

                        <div>
                            <h6 className="font-semibold text-sm mt-2">Descontos</h6>
                            {folha.descontos.map((d: any, i: number) => (
                                <div key={i}>{d.tipo}: {d.percentual} — {formatMoney(d.valor)}</div>
                            ))}
                            <div>INSS: {formatMoney(folha.desconto_inss)}</div>
                            <div>FGTS: {formatMoney(folha.desconto_fgts)}</div>
                            <div>IRRF: {formatMoney(folha.desconto_irrf)}</div>
                            <div className="font-bold text-red-500 mt-1">Total: {formatMoney(folha.total_descontos)}</div>
                        </div>

                        <div>
                            <h6 className="font-semibold text-sm mt-2">Proventos</h6>
                            {folha.proventos.map((p: any, i: number) => (
                                <div key={i}>Comissão {formatMoney(p.valor_vendas)} x {p.percentual}% = {formatMoney(p.comissao_gerada)}</div>
                            ))}
                            <div className="font-bold text-green-600 mt-1">Total: {formatMoney(folha.total_comissao)}</div>
                        </div>

                        <div>
                            <h6 className="font-semibold text-sm mt-2">Horas Extras</h6>
                            {folha.proventos.map((p: any, i: number) => (
                                <div key={i}>Horas {p.horas_extras} x {p.valor_hora} + 50% = {formatMoney(p.horas_extras_valor)}</div>
                            ))}
                            <div className="font-bold text-blue-500 mt-1">Total: {formatMoney(folha.total_horas)}</div>
                        </div>

                        <div className="mt-4">
                            <div className="text-lg font-bold text-green-700 dark:text-green-300">Salário Líquido: {formatMoney(folha.salario_liquido)}</div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FolhaPagamento;
