// FolhaPagamento.tsx
// Tela de folha de pagamento (RH).
// Exibe lista de colaboradores, salários, descontos e totais.
// Responsivo, dark mode, fonte Inter e mock data.
//
// Recursos:
// - Listagem de colaboradores e totais de folha.
// - Visualização de descontos e salários.
// - Cálculo automático de comissões e horas extras.
// - Download do holerite em PDF.
//
// Integrações Visuais:
// - Tema escuro e claro.
// - Estilo responsivo para diferentes tamanhos de tela.
// - Uso da fonte Inter.
//
// Responsividade garantida com Tailwind: tabelas usam overflow-x-auto, cards e grids se adaptam com breakpoints (sm, md, lg).
// Certifique-se de que a visualização de totais e descontos seja clara em telas pequenas.

import React, { useState, useEffect } from "react";
import { Input } from '../ui/Input';

// Mock de dados para folha de pagamento
const folhaPagamentoMock = [
    {
        id: 1,
        mes: "2025-06",
        ano: "2025",
        colaborador: {
            first_name: "João",
            FUNCAO: "G",
            data_contratacao: "2022-01-10",
            comissao_percentual: 5,
            valor_hora: 20,
        },
        salario_bruto: 3500,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
            { tipo: "Vale Alimentação", percentual: 3 },
        ],
        desconto_inss: 300,
        desconto_fgts: 200,
        desconto_irrf: 150,
        total_descontos: 650,
        comissoes: [
            { valor_vendas: 10000, horas_extras: 10 },
        ],
        total_comissao: 500,
        total_horas: 300,
        salario_liquido: 3650,
    },
    {
        id: 2,
        mes: "2025-06",
        ano: "2025",
        colaborador: {
            first_name: "Ana",
            FUNCAO: "V",
            data_contratacao: "2023-03-15",
            comissao_percentual: 7,
            valor_hora: 18,
        },
        salario_bruto: 2800,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
        ],
        desconto_inss: 250,
        desconto_fgts: 160,
        desconto_irrf: 100,
        total_descontos: 510,
        comissoes: [
            { valor_vendas: 8000, horas_extras: 5 },
        ],
        total_comissao: 560,
        total_horas: 90,
        salario_liquido: 2850,
    },
    {
        id: 3,
        mes: "2025-07",
        ano: "2025",
        colaborador: {
            first_name: "João",
            FUNCAO: "G",
            data_contratacao: "2022-01-10",
            comissao_percentual: 5,
            valor_hora: 20,
        },
        salario_bruto: 3500,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
            { tipo: "Vale Alimentação", percentual: 3 },
        ],
        desconto_inss: 310,
        desconto_fgts: 210,
        desconto_irrf: 160,
        total_descontos: 680,
        comissoes: [
            { valor_vendas: 12000, horas_extras: 12 },
        ],
        total_comissao: 600,
        total_horas: 350,
        salario_liquido: 3770,
    },
    {
        id: 4,
        mes: "2025-07",
        ano: "2025",
        colaborador: {
            first_name: "Carlos",
            FUNCAO: "C",
            data_contratacao: "2024-02-01",
            comissao_percentual: 0,
            valor_hora: 16,
        },
        salario_bruto: 2200,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
        ],
        desconto_inss: 180,
        desconto_fgts: 120,
        desconto_irrf: 80,
        total_descontos: 380,
        comissoes: [
            { valor_vendas: 0, horas_extras: 2 },
        ],
        total_comissao: 0,
        total_horas: 32,
        salario_liquido: 1852,
    },
    {
        id: 5,
        mes: "2025-05",
        ano: "2025",
        colaborador: {
            first_name: "Ana",
            FUNCAO: "V",
            data_contratacao: "2023-03-15",
            comissao_percentual: 7,
            valor_hora: 18,
        },
        salario_bruto: 2800,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
        ],
        desconto_inss: 240,
        desconto_fgts: 150,
        desconto_irrf: 90,
        total_descontos: 480,
        comissoes: [
            { valor_vendas: 7000, horas_extras: 3 },
        ],
        total_comissao: 490,
        total_horas: 54,
        salario_liquido: 2810,
    },
    // Exemplo de outro ano
    {
        id: 6,
        mes: "2024-06",
        ano: "2024",
        colaborador: {
            first_name: "João",
            FUNCAO: "G",
            data_contratacao: "2022-01-10",
            comissao_percentual: 5,
            valor_hora: 20,
        },
        salario_bruto: 3400,
        descontos: [
            { tipo: "Vale Transporte", percentual: 6 },
            { tipo: "Vale Alimentação", percentual: 3 },
        ],
        desconto_inss: 290,
        desconto_fgts: 190,
        desconto_irrf: 140,
        total_descontos: 620,
        comissoes: [
            { valor_vendas: 9500, horas_extras: 8 },
        ],
        total_comissao: 480,
        total_horas: 220,
        salario_liquido: 3260,
    },
];


// Função utilitária para formatar valores monetários
function formatMoney(valor: number) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

// Mock de funcionários para o select
const funcionariosMock = [
    { id: 1, nome: "João" },
    { id: 2, nome: "Ana" },
    { id: 3, nome: "Carlos" },
];

const meses = [
    { label: "Janeiro", value: "2025-01" },
    { label: "Fevereiro", value: "2025-02" },
    { label: "Março", value: "2025-03" },
    { label: "Abril", value: "2025-04" },
    { label: "Maio", value: "2025-05" },
    { label: "Junho", value: "2025-06" },
    { label: "Julho", value: "2025-07" },
    { label: "Agosto", value: "2025-08" },
    { label: "Setembro", value: "2025-09" },
    { label: "Outubro", value: "2025-10" },
    { label: "Novembro", value: "2025-11" },
    { label: "Dezembro", value: "2025-12" },
];

const FolhaPagamento: React.FC = () => {
    const [funcionarioSelecionado, setFuncionarioSelecionado] = useState(funcionariosMock[0].id);
    // Filtra os holerites do funcionário selecionado
    const holeritesFuncionario = folhaPagamentoMock.filter(item => item.colaborador.first_name === funcionariosMock.find(f => f.id === funcionarioSelecionado)?.nome);
    // Opções de ano e mês disponíveis para o funcionário
    const anosDisponiveis = Array.from(new Set(holeritesFuncionario.map(h => h.ano))).map(ano => ({ label: ano, value: ano }));
    const [anoSelecionado, setAnoSelecionado] = useState(anosDisponiveis[0]?.value || "");
    const mesesDisponiveis = Array.from(new Set(holeritesFuncionario.filter(h => h.ano === anoSelecionado).map(h => h.mes)))
        .map(mes => ({ label: meses.find(m => m.value === mes)?.label || mes, value: mes }));
    const [mesSelecionado, setMesSelecionado] = useState(mesesDisponiveis[0]?.value || "");

    // Atualiza ano e mês quando funcionário muda
    React.useEffect(() => {
        setAnoSelecionado(anosDisponiveis[0]?.value || "");
    }, [funcionarioSelecionado, anosDisponiveis]);
    React.useEffect(() => {
        setMesSelecionado(mesesDisponiveis[0]?.value || "");
    }, [anoSelecionado, funcionarioSelecionado, mesesDisponiveis]);

    React.useEffect(() => {
        document.documentElement.classList.add('dark');
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/sua-api-aqui');
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Erro ao buscar dados:', error);
            }
        };
        fetchData();
    }, []);

    // Filtra o holerite conforme mês, ano e funcionário selecionados
    const colaboradorSelecionado = funcionariosMock.find(f => f.id === funcionarioSelecionado);
    const holeritesFiltrados = folhaPagamentoMock.filter(item =>
        item.colaborador.first_name === colaboradorSelecionado?.nome &&
        item.mes === mesSelecionado &&
        item.ano === anoSelecionado
    );

    return (
        <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-6 bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors font-inter">
            {/* Filtros de funcionário, ano e mês */}
            <h1 className="text-center">Dados Fake.... a tela esta em desenvolvimento</h1>
            <div className="flex flex-col md:flex-row gap-2 mb-6 w-full max-w-2xl">
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Funcionário</label>
                    <select
                        className="form-select w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={funcionarioSelecionado}
                        onChange={e => setFuncionarioSelecionado(Number(e.target.value))}
                    >
                        {funcionariosMock.map(f => (
                            <option key={f.id} value={f.id}>{f.nome}</option>
                        ))}
                    </select>
                </div>
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Ano</label>
                    <select
                        className="form-select w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={anoSelecionado}
                        onChange={e => setAnoSelecionado(e.target.value)}
                    >
                        {anosDisponiveis.map(a => (
                            <option key={a.value} value={a.value}>{a.label}</option>
                        ))}
                    </select>
                </div>
                <div className="w-full md:w-1/4">
                    <label className="block text-xs font-semibold text-gray-700 dark:text-gray-200 mb-1">Mês</label>
                    <select
                        className="form-select w-full rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-3 py-2 text-sm"
                        value={mesSelecionado}
                        onChange={e => setMesSelecionado(e.target.value)}
                    >
                        {mesesDisponiveis.map(m => (
                            <option key={m.value} value={m.value}>{m.label}</option>
                        ))}
                    </select>
                </div>
            </div>
            {holeritesFiltrados.length === 0 && (
                <div className="text-center text-sm text-gray-500 dark:text-gray-300 my-8">Nenhum holerite encontrado para o filtro selecionado.</div>
            )}
            {holeritesFiltrados.map((item) => (
                <div key={item.id} className="mb-10">
                    {/* Título principal do holerite */}
                    <h2 className="text-left text-2xl font-bold mb-4 border-b border-gray-200 dark:border-gray-700 pb-2 flex items-center gap-4">
                        Holerite <span className="text-lg font-normal text-gray-500">({meses.find(m => m.value === item.mes)?.label}/{item.ano})</span>
                        <a
                            href={`#baixar_pdf_${item.id}`}
                            className="ml-auto text-blue-600 hover:underline text-base font-normal flex items-center gap-1"
                            download
                        >
                            <svg className="w-5 h-5 inline-block" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M7 10l5 5m0 0l5-5m-5 5V4" /></svg>
                            Baixar
                        </a>
                    </h2>
                    <div className="max-w-2xl grid gap-6">
                        {/* Card do colaborador */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex flex-col gap-2">
                            <div className="flex flex-col sm:flex-row sm:items-center gap-2 border-b border-gray-100 dark:border-gray-700 pb-2 mb-2">
                                <h5 className="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2">
                                    {item.colaborador.first_name}
                                    {item.colaborador.FUNCAO === "G" && (
                                        <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs">Gerente</span>
                                    )}
                                    {item.colaborador.FUNCAO === "C" && (
                                        <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs">Caixa</span>
                                    )}
                                    {item.colaborador.FUNCAO === "V" && (
                                        <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs">Vendedor</span>
                                    )}
                                </h5>
                                <span className="text-xs text-gray-500 dark:text-gray-300 ml-1">Data Contratação: {item.colaborador.data_contratacao || "Sem Data"}</span>
                            </div>
                            {/* Salário Bruto */}
                            <div className="flex flex-col md:flex-row md:items-center gap-2 mb-1">
                                <label className="w-full md:w-1/3 font-semibold text-gray-700 dark:text-gray-200">Salário Bruto</label>
                                <Input type="text" readOnly className="form-input w-full md:w-2/3 bg-gray-100 dark:bg-gray-700 text-black dark:text-white rounded px-3 py-2 font-bold" value={formatMoney(item.salario_bruto)} />
                            </div>
                            {/* Descontos */}
                            <div className="flex flex-col md:flex-row md:items-start gap-2 mb-1">
                                <label className="w-full md:w-1/3 font-semibold text-gray-700 dark:text-gray-200">Descontos</label>
                                <div className="w-full md:w-2/3 bg-gray-100 dark:bg-gray-700 rounded px-3 py-2 text-black dark:text-white text-sm flex flex-col gap-1">
                                    {item.descontos.map((d, i) => (
                                        <div key={i}>{d.tipo}: <span className="font-semibold">{d.percentual}%</span></div>
                                    ))}
                                    <div>Desconto INSS: <span className="font-semibold">{formatMoney(item.desconto_inss)}</span></div>
                                    <div>Desconto FGTS: <span className="font-semibold">{formatMoney(item.desconto_fgts)}</span></div>
                                    <div>Desconto IRRF: <span className="font-semibold">{formatMoney(item.desconto_irrf)}</span></div>
                                    <hr className="my-2 border-gray-300 dark:border-gray-600" />
                                    <div className="text-right font-bold text-red-600 dark:text-red-400">Total: {formatMoney(item.total_descontos)}</div>
                                </div>
                            </div>
                            {/* Proventos */}
                            <div className="flex flex-col md:flex-row md:items-start gap-2 mb-1">
                                <label className="w-full md:w-1/3 font-semibold text-gray-700 dark:text-gray-200">Proventos</label>
                                <div className="w-full md:w-2/3 bg-gray-100 dark:bg-gray-700 rounded px-3 py-2 text-black dark:text-white text-sm flex flex-col gap-1">
                                    {item.comissoes.map((c, i) => (
                                        <div key={i}>Comissão <span className="font-semibold">{formatMoney(c.valor_vendas)}</span> x {item.colaborador.comissao_percentual}%</div>
                                    ))}
                                    <hr className="my-2 border-gray-300 dark:border-gray-600" />
                                    <div className="text-right font-bold text-green-700 dark:text-green-400">Total: {formatMoney(item.total_comissao)}</div>
                                </div>
                            </div>
                            {/* Horas Extras */}
                            <div className="flex flex-col md:flex-row md:items-start gap-2 mb-1">
                                <label className="w-full md:w-1/3 font-semibold text-gray-700 dark:text-gray-200">Horas Extras</label>
                                <div className="w-full md:w-2/3 bg-gray-100 dark:bg-gray-700 rounded px-3 py-2 text-black dark:text-white text-sm flex flex-col gap-1">
                                    {item.comissoes.map((h, i) => (
                                        <div key={i}>Horas Trabalhadas <span className="font-semibold">{h.horas_extras}</span> x {item.colaborador.valor_hora} + 50%</div>
                                    ))}
                                    <hr className="my-2 border-gray-300 dark:border-gray-600" />
                                    <div className="text-right font-bold text-blue-700 dark:text-blue-400">Total: {formatMoney(item.total_horas)}</div>
                                </div>
                            </div>
                            {/* Salário Líquido */}
                            <div className="flex flex-col md:flex-row md:items-center gap-2 mt-2">
                                <label className="w-full md:w-1/3 font-semibold text-gray-700 dark:text-gray-200 text-lg">Salário Líquido</label>
                                <Input type="text" readOnly className="form-input w-full md:w-2/3 bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-200 rounded px-3 py-2 font-bold text-lg border-2 border-green-300 dark:border-green-700" value={formatMoney(item.salario_liquido)} />
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default FolhaPagamento;
