import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/Button';
import api from '../../utils/axiosConfig';

interface User {
  id: number;
  username: string;
  first_name: string;
  FUNCAO: string;
  salario_bruto: number;
  comissao_percentual: number;
  valor_hora: number;
  data_contratacao: string;
}

function formatLocalDate(dateStr: string | undefined): string {
  if (!dateStr) return '';
  const [year, month, day] = dateStr.slice(0, 10).split('-');
  return `${day}/${month}/${year}`;
}

const ComissaoList: React.FC = () => {
  const [comissoes, setComissoes] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState<{
    first_name: string;
    username: string;
    FUNCAO: string;
    salario_bruto: string;
    valor_hora: string;
    comissao_percentual: string;
    data_contratacao: string;
  }>({
    first_name: '',
    username: '',
    FUNCAO: '',
    salario_bruto: '',
    valor_hora: '',
    comissao_percentual: '',
    data_contratacao: '',
  });

  const navigate = useNavigate();

  // Carrega os dados do endpoint /usuarios
  useEffect(() => {
    const fetchComissoes = async () => {
      try {
        setLoading(true);
        const response = await api.get('/usuarios');
        setComissoes(response.data.results);
      } catch (err) {
        const error = err as Error;
        setError('Erro ao carregar comissões: ' + (error.message || 'Tente novamente'));
      } finally {
        setLoading(false);
      }
    };

    fetchComissoes();
  }, []);

  // Inicia a edição de um usuário
  const handleEdit = (user: User) => {
    setEditingId(user.id);
    setEditForm({
      first_name: user.first_name,
      username: user.username,
      FUNCAO: user.FUNCAO,
      salario_bruto: user.salario_bruto.toString(),
      valor_hora: user.valor_hora.toString(),
      comissao_percentual: user.comissao_percentual.toString(),
      data_contratacao: user.data_contratacao,
    });
  };

  // Cancela a edição
  const handleCancel = () => {
    setEditingId(null);
    setEditForm({
      first_name: '',
      username: '',
      FUNCAO: '',
      salario_bruto: '',
      valor_hora: '',
      comissao_percentual: '',
      data_contratacao: '',
    });
    setError(null);
  };

  // Salva as alterações
  const handleSave = async (id: number) => {
    // Validações
    if (!editForm.first_name.trim()) {
      setError('Nome é obrigatório');
      return;
    }
    if (!editForm.username.trim()) {
      setError('Username é obrigatório');
      return;
    }
    if (!editForm.FUNCAO.trim()) {
      setError('Função é obrigatória');
      return;
    }
    if (isNaN(Number(editForm.salario_bruto)) || Number(editForm.salario_bruto) < 0) {
      setError('Salário bruto deve ser um número válido');
      return;
    }
    if (isNaN(Number(editForm.valor_hora)) || Number(editForm.valor_hora) < 0) {
      setError('Valor da hora extra deve ser um número válido');
      return;
    }
    if (
      isNaN(Number(editForm.comissao_percentual)) ||
      Number(editForm.comissao_percentual) < 0 ||
      Number(editForm.comissao_percentual) > 100
    ) {
      setError('Comissão deve ser um número entre 0 e 100');
      return;
    }
    if (!editForm.data_contratacao) {
      setError('Data de contratação é obrigatória');
      return;
    }

    try {
      setLoading(true);
      await api.put(`/usuarios/${id}/`, {
        username: editForm.username,
        first_name: editForm.first_name,
        FUNCAO: editForm.FUNCAO,
        salario_bruto: Number(editForm.salario_bruto),
        valor_hora: Number(editForm.valor_hora),
        comissao_percentual: Number(editForm.comissao_percentual),
        data_contratacao: editForm.data_contratacao,
      });
      setComissoes((prev) =>
        prev.map((user) =>
          user.id === id
            ? {
                ...user,
                username: editForm.username,
                first_name: editForm.first_name,
                FUNCAO: editForm.FUNCAO,
                salario_bruto: Number(editForm.salario_bruto),
                valor_hora: Number(editForm.valor_hora),
                comissao_percentual: Number(editForm.comissao_percentual),
                data_contratacao: editForm.data_contratacao,
              }
            : user
        )
      );
      setEditingId(null);
      setEditForm({
        first_name: '',
        username: '',
        FUNCAO: '',
        salario_bruto: '',
        valor_hora: '',
        comissao_percentual: '',
        data_contratacao: '',
      });
      setError(null);
      alert('Usuário atualizado com sucesso!');
    } catch (err: any) {
      console.error('Erro na requisição PUT:', err.response?.data);
      const errorMessage =
        err.response?.data?.detail ||
        Object.values(err.response?.data || {}).join(', ') ||
        err.message ||
        'Tente novamente';
      setError('Erro ao atualizar usuário: ' + errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (loading && comissoes.length === 0) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );

  if (error && comissoes.length === 0) return (
    <div className="text-center text-red-500 p-4 bg-red-100 rounded-lg">
      {error}
    </div>
  );

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

      <h2 className="text-center text-2xl font-bold mb-4">Folha de Pagamento Funcionários</h2>
      <div className="flex flex-col sm:flex-row justify-end mb-4 gap-2">
        <Link
          to="/comissao"
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded shadow w-full sm:w-auto text-center"
        >
          Nova Comissão
        </Link>
        <Link
          to="/desconto"
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded shadow w-full sm:w-auto text-center"
        >
          Novo Descontos
        </Link>
      </div>
      <div className="overflow-x-auto rounded-lg">
        <table className="w-full text-xs sm:text-sm md:text-base table-auto bg-white dark:bg-gray-800 rounded shadow min-w-[600px]">
          <thead>
            <tr>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Funcionário</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Salário Base</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Valor Hora Extra</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">% Comissão</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Contratação</th>
              <th className="px-2 sm:px-4 py-2 border-b text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            {comissoes.map((comissao) => (
              <tr key={comissao.id} className="hover:bg-gray-100 dark:hover:bg-gray-700">
                {editingId === comissao.id ? (
                  <>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <input
                        type="text"
                        value={editForm.first_name}
                        onChange={(e) => setEditForm({ ...editForm, first_name: e.target.value })}
                        className="w-full p-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Nome"
                      />
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <input
                        type="number"
                        value={editForm.salario_bruto}
                        onChange={(e) => setEditForm({ ...editForm, salario_bruto: e.target.value })}
                        min="0"
                        step="0.01"
                        className="w-full p-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Salário Bruto"
                      />
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <input
                        type="number"
                        value={editForm.valor_hora}
                        onChange={(e) => setEditForm({ ...editForm, valor_hora: e.target.value })}
                        min="0"
                        step="0.01"
                        className="w-full p-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Valor Hora Extra"
                      />
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <input
                        type="number"
                        value={editForm.comissao_percentual}
                        onChange={(e) => setEditForm({ ...editForm, comissao_percentual: e.target.value })}
                        min="0"
                        max="100"
                        step="0.1"
                        className="w-full p-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Comissão (%)"
                      />
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <input
                        type="date"
                        value={editForm.data_contratacao}
                        onChange={(e) => setEditForm({ ...editForm, data_contratacao: e.target.value })}
                        className="w-full p-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap flex gap-2">
                      <Button
                        type="button"
                        className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded"
                        onClick={() => handleSave(comissao.id)}
                        disabled={loading}
                      >
                        Salvar
                      </Button>
                      <Button
                        type="button"
                        variant="outline"
                        className="px-3 py-1 text-sm"
                        onClick={handleCancel}
                        disabled={loading}
                      >
                        Cancelar
                      </Button>
                    </td>
                  </>
                ) : (
                  <>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      <Link to={`/comissoesapi/${comissao.id}`} className="text-blue-600 hover:underline">
                        {comissao.first_name}
                      </Link>
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      R$ {comissao.salario_bruto.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      R$ {comissao.valor_hora.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      {comissao.comissao_percentual.toLocaleString('pt-BR', { minimumFractionDigits: 1 })}%
                    </td>
                    <td className="px-2 sm:px-4 py-2 border-b whitespace-nowrap">
                      {formatLocalDate(comissao.data_contratacao)}
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
                  </>
                )}
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

export default ComissaoList;