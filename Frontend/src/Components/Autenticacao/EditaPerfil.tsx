import React, { useState, useEffect } from 'react';
import api from '../../utils/axiosConfig';

interface User {
  id: number;
  username: string;
  first_name: string;
  FUNCAO: string;
}



const EditUser: React.FC = ({ }) => {
  const [user, setUser] = useState<User | null>(null);
  const [username, setUsername] = useState('');
  const [firstName, setFirstName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Carrega o userId do localStorage e os dados do usuário
  useEffect(() => {
    const fetchUser = async () => {
      const userId = localStorage.getItem('user_id');
      
      if (!userId) {
        setError('ID do usuário não encontrado no localStorage');
        return;
      }

      try {
        setLoading(true);
        const response = await api.get(`/usuarios/${userId}/`);
        setUser(response.data);
        setUsername(response.data.username);
        setFirstName(response.data.first_name);
      } catch (err) {
        const error = err as Error;
        setError('Erro ao carregar usuário: ' + (error.message || 'Tente novamente'));
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Função para enviar a requisição PUT
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const userId = localStorage.getItem('user_id');

    if (!userId) {
      setError('ID do usuário não encontrado no localStorage');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await api.put(`/usuarios/${userId}/`, {
        username,
        first_name: firstName,
      });
      window.location.assign("editar-perfil");
    } catch (err) {
      const error = err as Error;
      setError('Erro ao atualizar usuário: ' + (error.message || 'Tente novamente'));
    } finally {
      setLoading(false);
    }
  };

  if (loading && !user) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  );

  if (error && !user) return (
    <div className="text-center text-red-500 p-4 bg-red-100 rounded-lg">
      {error}
    </div>
  );

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">Editar Usuário</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700">
            Username
          </label>
          <input
            id="username"
            type="text"
            disabled={true}
            readOnly
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite o username"
          />
        </div>
        <div>
          <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">
            Primeiro Nome
          </label>
          <input
            id="firstName"
            type="text"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
            className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite o primeiro nome"
          />
        </div>
        {error && (
          <p className="text-red-500 text-sm text-center">{error}</p>
        )}
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 rounded-md text-white font-medium ${
            loading ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          } transition-colors duration-200`}
        >
          {loading ? 'Salvando...' : 'Salvar'}
        </button>
      </form>
    </div>
  );
};

export default EditUser;