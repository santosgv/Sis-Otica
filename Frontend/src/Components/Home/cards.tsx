import React, { useEffect, useState } from 'react';
import api from "../../utils/axiosConfig"


interface Aniversariante {
  id: number;
  nome: string;
  telefone: string;
  data_nascimento: string;
  email: string;
  mensagem: string;
}

const LOCAL_STORAGE_KEY = 'cardsFechadosAniversariantes';

const AniversariantesMes: React.FC = () => {
  const [aniversariantes, setAniversariantes] = useState<Aniversariante[]>([]);
  const [cardsFechados, setCardsFechados] = useState<Set<number>>(new Set());

  // Carrega fechados do localStorage
  useEffect(() => {
    const fechadosJSON = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (fechadosJSON) {
      try {
        const fechadosArray = JSON.parse(fechadosJSON);
        setCardsFechados(new Set(fechadosArray));
      } catch {
        setCardsFechados(new Set());
      }
    }
  }, []);

  // Busca aniversariantes
  useEffect(() => {
    const fetchAniversariantes = async () => {
      try {
        const res = await api.get('/aniversariantes_mes/');
        setAniversariantes(res.data);
      } catch (err) {
        console.error('Erro ao carregar aniversariantes:', err);
      }
    };

    fetchAniversariantes();
  }, []);

  const enviarMensagemWhatsApp = (telefone: string, mensagem: string) => {
    const telefoneFormatado = telefone.replace(/\D/g, '');
    const link = `https://wa.me/55${telefoneFormatado}?text=${(mensagem)}`;
    window.open(link, '_blank');
  };

  const fecharCard = (id: number) => {
    const novoSet = new Set(cardsFechados).add(id);
    setCardsFechados(novoSet);
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify([...novoSet]));
  };

  return (
    <div className="flex flex-wrap gap-4 justify-start">
      {aniversariantes
        .filter((cliente) => !cardsFechados.has(cliente.id))
        .map((cliente) => (
          <div
            key={cliente.id}
            className="relative bg-white shadow-lg rounded-xl p-6 w-full max-w-xs hover:shadow-xl transition-shadow duration-300 border"
          >
            {/* Botão de fechar */}
            <button
              onClick={() => fecharCard(cliente.id)}
              className="absolute top-2 right-2 text-gray-400 hover:text-red-500 text-lg font-bold"
              title="Fechar"
            >
              ✖
            </button>

            {/* Conteúdo */}
            <div className="text-center">
              <h3 className="text-lg font-semibold text-gray-800">{cliente.nome}</h3>
              <p className="text-sm text-gray-500 mb-1">
                <span className="font-medium text-gray-700">Dia:</span> {cliente.data_nascimento}
              </p>
              <p className="text-sm text-gray-500 mb-1">
                <span className="font-medium text-gray-700">Telefone:</span> {cliente.telefone}
                   <button
              onClick={() => enviarMensagemWhatsApp(cliente.telefone, cliente.mensagem)}
            >
            <img width="30" height="30" src="https://img.icons8.com/color/48/whatsapp--v1.png" alt="whatsapp--v1"/>
            </button>
              </p>
              <p className="text-sm text-gray-500 mb-4">
                <span className="font-medium text-gray-700">Email:</span> {cliente.email}
              </p>
            </div>
         
          </div>
        ))}
    </div>
  );
};

export default AniversariantesMes;