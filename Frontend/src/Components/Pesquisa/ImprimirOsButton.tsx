import React, { useState, useContext } from "react";
import { ThemeContext } from "../../ThemeContext/themecontext";
import api from "../../utils/axiosConfig";

interface ImprimirOsButtonProps {
  idOs: number;
}

const ImprimirOsButton: React.FC<ImprimirOsButtonProps> = ({ idOs }) => {
  const { theme } = useContext(ThemeContext);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");
  const isDark = theme === "dark";

  const handleImprimirOs = async () => {
    try {
      setLoading(true);
      setErro("");
      setMensagem("");

      // Faz a requisição para o endpoint com responseType: 'blob'
      const response = await api.get(`imprimir_os/${idOs}`, {
        responseType: "blob", // Para receber dados binários (PDF)
      });

      // Cria um objeto Blob a partir da resposta
      const blob = new Blob([response.data], { type: "application/pdf" });

      // Cria um URL temporário para o Blob
      const url = window.URL.createObjectURL(blob);

      // Cria um link temporário para download
      const link = document.createElement("a");
      link.href = url;
      link.download = `OS-${idOs}.pdf`; // Nome do arquivo, ajustado com idOs
      document.body.appendChild(link);
      link.click();

      // Remove o link e libera o URL
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setMensagem("PDF gerado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
    } catch (e) {
      console.error("Erro ao gerar PDF:", e);
      setErro("Erro ao gerar o PDF da OS. Tente novamente.");
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
            ? "bg-yellow-700 hover:bg-yellow-800 text-white"
            : "bg-yellow-500 hover:bg-yellow-600 text-white"
        } ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
        onClick={handleImprimirOs}
        disabled={loading}
        title="Imprimir OS"
      >
        {loading ? "Imorimindo..." : "Imprimir OS"}
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

export default ImprimirOsButton;