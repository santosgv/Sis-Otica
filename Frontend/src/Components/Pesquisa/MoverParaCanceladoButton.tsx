import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { ThemeContext } from "../../ThemeContext/themecontext";
import api from "../../utils/axiosConfig";

interface MoverParaCanceladoButtonProps {
  idOs: number;
  onStatusChange?: () => void; // Callback para atualizar a lista após mudança
}

const MoverParaCanceladoButton: React.FC<MoverParaCanceladoButtonProps> = ({ idOs, onStatusChange }) => {
  const { theme } = useContext(ThemeContext);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");
  const isDark = theme === "dark";
  const navigate = useNavigate();

  const handleMoverParaLoja = async () => {
    try {
      setLoading(true);
      setErro("");
      setMensagem("");

      const response = await api.post(`/cancelar_os/${idOs}/`);
      setMensagem(response.data.message);
      navigate(-1)
      setTimeout(() => setMensagem(""), 2500);
    } catch (e: any) {
      console.error("Erro ao mover OS para a Cancelado:", e);
      setErro(e.response?.data?.error || "Erro ao mover OS para a Cancelado.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative">
      {/* Botão */}
      <button
        className={`text-sm px-3 py-1 rounded ${
          isDark
            ? "bg-red-700 hover:bg-red-800 text-white"
            : "bg-red-500 hover:bg-red-600 text-white"
        } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
        onClick={handleMoverParaLoja}
        disabled={loading}
        title="Mover para Cancelado"
      >
        {loading ? "Movendo..." : "Mover para Cancelado"}
      </button>
      {/* Mensagem de feedback */}
      {mensagem && (
        <div
          className={`absolute top-0 left-1/2 transform -translate-x-1/2 mt-12 bg-green-500 text-white px-4 py-2 rounded shadow-lg z-50`}
        >
          {mensagem}
        </div>
      )}
      {erro && (
        <div
          className={`absolute top-0 left-1/2 transform -translate-x-1/2 mt-12 bg-red-500 text-white px-4 py-2 rounded shadow-lg z-50`}
        >
          {erro}
        </div>
      )}
    </div>
  );
};

export default MoverParaCanceladoButton;