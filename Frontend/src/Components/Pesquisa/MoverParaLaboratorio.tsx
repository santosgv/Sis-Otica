import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { ThemeContext } from "../../ThemeContext/themecontext";
import api from "../../utils/axiosConfig";

interface MoverParaLaboratorioButtonProps {
  idOs: number;
  onStatusChange?: () => void; // Callback para atualizar a lista após mudança
}

const MoverParaLaboratorioButton: React.FC<MoverParaLaboratorioButtonProps> = ({ idOs, onStatusChange }) => {
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

      const response = await api.post(`/laboratorio_os/${idOs}/`);
      setMensagem(response.data.message);
      navigate(-1)

      setTimeout(() => setMensagem(""), 2500);
    } catch (e: any) {
      console.error("Erro ao mover OS para a Entregue:", e);
      setErro(e.response?.data?.error || "Erro ao mover OS para a Entregue.");
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
            ? "bg-blue-700 hover:bg-blue-800 text-white"
            : "bg-blue-500 hover:bg-blue-600 text-white"
        } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
        onClick={handleMoverParaLoja}
        disabled={loading}
        title="Mover para Loja"
      >
        {loading ? "Movendo..." : "Mover para Laboratorio"}
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

export default MoverParaLaboratorioButton;