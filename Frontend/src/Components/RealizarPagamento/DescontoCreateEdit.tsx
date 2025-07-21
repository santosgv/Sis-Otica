import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/Button';
import api from '../../utils/axiosConfig';

interface User {
  id: number;
  first_name: string;
}

interface Desconto {
  id?: number;
  tipo: string;
  percentual: number;
  colaborador: number;
}

const DescontoCreateEdit: React.FC = () => {
  const [form, setForm] = useState<Desconto>({
    tipo: '',
    percentual: 0,
    colaborador: 0,
  });
  const [colaboradores, setColaboradores] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>(); // ID para edição, undefined para criação

  // Carrega colaboradores e, se for edição, os dados do desconto
  useEffect(() => {
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

    const fetchDesconto = async () => {
      if (id) {
        try {
          setLoading(true);
          const response = await api.get(`/descontos/${id}/`);
          setForm(response.data);
        } catch (err) {
          const error = err as Error;
          setError('Erro ao carregar desconto: ' + (error.message || 'Tente novamente'));
        } finally {
          setLoading(false);
        }
      }
    };

    fetchColaboradores();
    fetchDesconto();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validações
    if (!form.tipo.trim()) {
      setError('Tipo é obrigatório');
      return;
    }
    if (isNaN(form.percentual) || form.percentual < 0 || form.percentual > 100) {
      setError('Percentual deve ser um número entre 0 e 100');
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
        await api.put(`/descontos/${id}/`, form);
        alert('Desconto atualizado com sucesso!');
      } else {
        // Criação (POST)
        await api.post('/descontos/', form);
        alert('Desconto criado com sucesso!');
      }
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

  if (loading && colaboradores.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error && colaboradores.length === 0) {
    return (
      <div className="text-center text-red-500 p-4 bg-red-100 rounded-lg">
        {error}
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 p-2 sm:p-4 font-sans">
      <div className="max-w-md mx-auto mt-10 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
        <div className="mb-4 flex justify-start">
          <Button
            type="button"
            variant="outline"
            className="px-4 py-2 font-semibold shadow"
            onClick={() => navigate('/desconto')}
          >
            ← Voltar
          </Button>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-6 text-center">
          {id ? 'Editar Desconto' : 'Novo Desconto'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="tipo" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Tipo
            </label>
            <input
              id="tipo"
              type="text"
              value={form.tipo}
              onChange={(e) => setForm({ ...form, tipo: e.target.value })}
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
              placeholder="Digite o tipo (ex.: pensão, vale transporte)"
            />
          </div>
          <div>
            <label htmlFor="percentual" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Percentual (%)
            </label>
            <input
              id="percentual"
              type="number"
              value={form.percentual || ''}
              onChange={(e) => setForm({ ...form, percentual: Number(e.target.value) })}
              min="0"
              max="100"
              step="0.1"
              className="mt-1 w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200"
              placeholder="Digite o percentual"
            />
          </div>
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
    </div>
  );
};

export default DescontoCreateEdit;