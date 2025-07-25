import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import api from '../../utils/axiosConfig';

interface User {
  id: number;
  first_name: string;
}

interface Comissao {
  id?: number;
  valor_vendas: number;
  data_referencia: string;
  horas_extras: number;
  colaborador: number;
}

function formatLocalDate(dateStr: string | undefined): string {
  if (!dateStr) return '';
  const [year, month, day] = dateStr.slice(0, 10).split('-');
  return `${day}/${month}/${year}`;
}

const ComissaoForm: React.FC = () => {
  const [comissoes, setComissoes] = useState<Comissao[]>([]);
  const [colaboradores, setColaboradores] = useState<User[]>([]);
  const [form, setForm] = useState<Comissao>({
    valor_vendas: 0,
    data_referencia: '',
    horas_extras: 0,
    colaborador: 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>(); // ID para edição, undefined para criação

  // Carrega comissões e colaboradores
  useEffect(() => {
    const fetchComissoes = async () => {
      try {
        setLoading(true);
        const response = await api.get('/comissoesapi');
        setComissoes(response.data.results);
      } catch (err) {
        const error = err as Error;
        setError('Erro ao carregar comissões: ' + (error.message || 'Tente novamente'));
      } finally {
        setLoading(false);
      }
    };

    const fetchColaboradores = async () => {
      try {
        setLoading(true);
        const response = await api.get('/usuarios');
        setColaboradores(response.data.results);
      } catch (err) {
        const error = err as Error;
        setError('Erro ao carregar colaboradores: ' + (error.message || 'Tente novamente'));
      } finally {
        setLoading(false);
      }
    };

    const fetchComissao = async () => {
      if (id) {
        try {
          setLoading(true);
          const response = await api.get(`/comissoesapi/${id}/`);
          setForm(response.data);
        } catch (err) {
          const error = err as Error;
          setError('Erro ao carregar comissão: ' + (error.message || 'Tente novamente'));
        } finally {
          setLoading(false);
        }
      }
    };

    fetchComissoes();
    fetchColaboradores();
    fetchComissao();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validações
    if (form.valor_vendas <= 0) {
      setError('Valor das vendas deve ser maior que 0');
      return;
    }
    if (!form.data_referencia) {
      setError('Data de referência é obrigatória');
      return;
    }
    if (form.horas_extras < 0) {
      setError('Horas extras não podem ser negativas');
      return;
    }
    if (!form.colaborador) {
      setError('Selecione um colaborador');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      if (id) {
        // Edição (PUT)
        await api.put(`/comissoesapi/${id}/`, form);
        setComissoes((prev) =>
          prev.map((comissao) =>
            comissao.id === Number(id) ? { ...comissao, ...form } : comissao
          )
        );
        alert('Comissão atualizada com sucesso!');
      } else {
        // Criação (POST)
        const response = await api.post('/comissoesapi/', form);
        setComissoes((prev) => [...prev, response.data]);
        alert('Comissão criada com sucesso!');
      }
      setForm({
        valor_vendas: 0,
        data_referencia: '',
        horas_extras: 0,
        colaborador: 0,
      });
      navigate('/comissao');
    } catch (err: any) {
      console.error('Erro na requisição:', err.response?.data);
      const errorMessage =
        err.response?.data?.detail ||
        Object.values(err.response?.data || {}).join(', ') ||
        err.message ||
        'Tente novamente';
      setError('Erro: ' + errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (comissao: Comissao) => {
    navigate(`/comissao/edit/${comissao.id}`);
  };

  if (loading && comissoes.length === 0 && colaboradores.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error && comissoes.length === 0 && colaboradores.length === 0) {
    return (
      <div className="text-center text-red-500 p-4 bg-red-100 rounded-lg">
        {error}
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 p-2 sm:p-4 font-sans">

      {/* Formulário de Criação/Edição */}
      <div className="max-w-lg mx-auto bg-white dark:bg-gray-800 rounded-lg shadow px-2 py-6 sm:p-6">
        <div className="mb-4 flex justify-start">
          <Button
            type="button"
            variant="outline"
            className="px-4 py-2 font-semibold shadow"
            onClick={() => navigate('/realizar-pagamento')}
          >
            ← Voltar
          </Button>
        </div>
        <h2 className="text-center text-xl sm:text-2xl font-bold mb-3 sm:mb-4">
          {id ? 'Editar Comissão' : 'Nova Comissão'}
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:gap-4">
          <div>
            <label htmlFor="colaborador" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Colaborador
            </label>
            <select
              id="colaborador"
              value={form.colaborador || ''}
              onChange={(e) => setForm({ ...form, colaborador: Number(e.target.value) })}
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
            >
              <option value="">Selecione um colaborador</option>
              {colaboradores.map((colaborador) => (
                <option key={colaborador.id} value={colaborador.id}>
                  {colaborador.first_name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="valor_vendas" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Valor das Vendas (R$)
            </label>
            <Input
              id="valor_vendas"
              type="number"
              value={form.valor_vendas || ''}
              onChange={(e) => setForm({ ...form, valor_vendas: Number(e.target.value) })}
              min="0"
              step="0.01"
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
              placeholder="Digite o valor das vendas"
            />
          </div>
          <div>
            <label htmlFor="data_referencia" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Data de Referência
            </label>
            <Input
              id="data_referencia"
              type="date"
              value={formatLocalDate(form.data_referencia)}
              onChange={(e) => setForm({ ...form, data_referencia: e.target.value })}
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
            />
          </div>
          <div>
            <label htmlFor="horas_extras" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Horas Extras
            </label>
            <Input
              id="horas_extras"
              type="number"
              value={form.horas_extras || ''}
              onChange={(e) => setForm({ ...form, horas_extras: Number(e.target.value) })}
              min="0"
              step="1"
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
              placeholder="Digite as horas extras"
            />
          </div>
          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}
          <Button
            type="submit"
            disabled={loading}
            className={`w-full py-2 px-4 rounded-md text-white font-medium ${
              loading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
            } transition-colors duration-200`}
          >
            {loading ? 'Salvando...' : id ? 'Salvar' : 'Criar'}
          </Button>
        </form>
      </div>

      {/* Lista de Comissões */}
      <div className="max-w-4xl mx-auto mb-8">
        <h2 className="text-center text-xl sm:text-2xl font-bold mb-4">Lista de Comissões</h2>
        <div className="overflow-x-auto rounded-lg">
          <table className="w-full text-xs sm:text-sm md:text-base table-auto bg-white dark:bg-gray-800 rounded shadow min-w-[500px]">
            <thead>
              <tr>
                <th className="px-2 sm:px-4 py-2 border-b text-left">Colaborador</th>
                <th className="px-2 sm:px-4 py-2 border-b text-left">Valor Vendas</th>
                <th className="px-2 sm:px-4 py-2 border-b text-left">Horas Extras</th>
                <th className="px-2 sm:px-4 py-2 border-b text-left">Data Referência</th>
                <th className="px-2 sm:px-4 py-2 border-b text-left">Ações</th>
              </tr>
            </thead>
            <tbody>
              {comissoes.map((comissao) => (
                <tr key={comissao.id} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                  <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                    {colaboradores.find((col) => col.id === comissao.colaborador)?.first_name || 'Desconhecido'}
                  </td>
                  <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                    R$ {comissao.valor_vendas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </td>
                  <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                    {comissao.horas_extras}
                  </td>
                  <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                    {formatLocalDate(comissao.data_referencia)}
                  </td>
                  <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                    <Button
                      type="button"
                      variant="outline"
                      className="px-3 py-1 text-sm"
                      onClick={() => handleEdit(comissao)}
                    >
                      Editar
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>


    </div>
  );
};

export default ComissaoForm;