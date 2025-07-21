import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';
import api from '../../utils/axiosConfig';

interface User {
  id: number;
  first_name: string;
}

interface Desconto {
  id: number;
  tipo: string;
  percentual: number;
  colaborador: number;
}


const DescontoList: React.FC = () => {
  const [descontos, setDescontos] = useState<Desconto[]>([]);
  const [colaboradores, setColaboradores] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();

  // Carrega os descontos e colaboradores
  useEffect(() => {
    const fetchDescontos = async () => {
      try {
        setLoading(true);
        const response = await api.get('/descontos');
        setDescontos(response.data.results);
      } catch (err) {
        const error = err as Error;
        setError('Erro ao carregar descontos: ' + (error.message || 'Tente novamente'));
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

    fetchDescontos();
    fetchColaboradores();
  }, []);

  if (loading && descontos.length === 0 && colaboradores.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error && descontos.length === 0) {
    return (
      <div className="text-center text-red-500 p-4 bg-red-100 rounded-lg">
        {error}
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 p-2 sm:p-4 font-sans">
      <div className="mb-4 flex justify-start">
        <Button
          type="button"
          variant="outline"
          className="px-4 py-2 font-semibold shadow"
          onClick={() => navigate(-1)}
        >
          ← Voltar
        </Button>
      </div>

      <h2 className="text-center text-2xl font-bold mb-4">Lista de Descontos</h2>
      <div className="flex flex-col sm:flex-row justify-end mb-4 gap-2">
        <Link
          to="/desconto/create"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow w-full sm:w-auto text-center"
        >
          Novo Desconto
        </Link>
      </div>
      <div className="overflow-x-auto rounded-lg">
        <table className="w-full text-xs sm:text-sm md:text-base table-auto bg-white dark:bg-gray-800 rounded shadow min-w-[500px]">
          <thead>
            <tr>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Colaborador</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Tipo</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Percentual</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            {descontos.map((desconto) => (
              <tr key={desconto.id} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                  <Link to={`/desconto/edit/${desconto.id}`} className="text-blue-600 hover:underline">
                    {colaboradores.find((col) => col.id === desconto.colaborador)?.first_name || 'Desconhecido'}
                  </Link>
                </td>
                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                  {desconto.tipo}
                </td>
                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                  {desconto.percentual.toLocaleString('pt-BR', { minimumFractionDigits: 1 })}%
                </td>
                <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                  <Button
                    type="button"
                    variant="outline"
                    className="px-3 py-1 text-sm"
                    onClick={() => navigate(`/desconto/edit/${desconto.id}`)}
                  >
                    Editar
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {error && (
          <p className="text-red-500 text-sm text-center mt-4">{error}</p>
        )}
      </div>
    </div>
  );
};

export default DescontoList;