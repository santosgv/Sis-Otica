import React, { useState, useEffect } from "react";
import api from "../../utils/axiosConfig";

interface AdicionarCaixaProps {
  onClose: () => void;
  onSuccess?: () => void;
}

interface OsOption {
  id: number;
  numero: string; // Usaremos `OS ${id}` para exibição
}

const formasPagamento = [
  { value: "A", label: "Pix" },
  { value: "B", label: "Dinheiro" },
  { value: "C", label: "Débito" },
  { value: "D", label: "Crédito" },
  { value: "E", label: "Carnê" },
  { value: "F", label: "Permuta" },
];

const tipos = [
  { value: "E", label: "Entrada" },
  { value: "S", label: "Saída" },
];

const AdicionarCaixa: React.FC<AdicionarCaixaProps> = ({ onClose, onSuccess }) => {
  const [data] = useState(() => new Date().toISOString().split("T")[0]); // Formato YYYY-MM-DD
  const [valor, setValor] = useState("");
  const [forma, setForma] = useState("A");
  const [tipo, setTipo] = useState("E");
  const [descricao, setDescricao] = useState("");
  const [searchOs, setSearchOs] = useState("");
  const [referencia, setReferencia] = useState("");
  const [osOptions, setOsOptions] = useState<OsOption[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [osLoading, setOsLoading] = useState(true);


   function formatLocalDate(dateStr: string | undefined): string {
  if (!dateStr) return "";
  const [year, month, day] = dateStr.slice(0, 10).split("-");
  return `${day}/${month}/${year}`;
}

  // Buscar ordens de serviço do endpoint /os
  const fetchOsOptions = async () => {
    setOsLoading(true);
    try {
      const response = await api.get("/ordens/");
      const options = response.data.results
        .filter((os: any) => os.id) // Garante que o id existe
        .map((os: any) => ({
          id: os.id,
          numero: `OS ${os.id}`, // Usa o id como número da OS
        }));
      setOsOptions([{ id: 0, numero: "Nenhuma OS" }, ...options]);
    } catch (err) {
      setError("Erro ao carregar ordens de serviço.");
    } finally {
      setOsLoading(false);
    }
  };

  useEffect(() => {
    fetchOsOptions();
  }, []);

  // Temporizador para mensagens de erro
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Máscara para valor (R$)
  function handleValorChange(e: React.ChangeEvent<HTMLInputElement>) {
    let v = e.target.value.replace(/[^\d]/g, "");
    v = (Number(v) / 100).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
    setValor(v);
  }

  // Filtrar opções de OS com verificação de undefined
  const filteredOsOptions = osOptions.filter((opt) =>
    opt.numero?.toLowerCase().includes(searchOs.toLowerCase())
  );

  // Submissão do formulário
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    // Validações
    if (!valor || Number(valor.replace(/[^\d,.-]/g, "").replace(",", ".")) <= 0) {
      setError("O valor deve ser maior que zero.");
      return;
    }
    if (!descricao.trim()) {
      setError("A descrição é obrigatória.");
      return;
    }

    setLoading(true);
    try {
      const valorNumerico = String(valor.replace(/[R$\s]/g, "").replace(/\./g, "").replace(",", ".")) ;
      console.log(valorNumerico)
      await api.post("/dados-caixa/", {
        DATA: data,
        DESCRICAO: descricao,
        TIPO: tipo,
        VALOR: valorNumerico,
        FORMA: forma,
        FECHADO: false,
        REFERENCIA: referencia && Number(referencia) !== 0 ? Number(referencia) : null,
      });
      if (onSuccess) onSuccess();
      if (onClose) onClose();
    } catch (err) {
      console.log(err)
      setError("Erro ao adicionar lançamento.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full flex justify-center items-start py-8">
      <div className="w-full max-w-sm sm:max-w-md md:max-w-lg mx-auto">
        {/* Mensagem de erro */}
        {error && (
          <div
            className="fixed left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-2 rounded shadow-lg z-50 text-sm font-medium"
            style={{ top: 88 }}
          >
            {error}
          </div>
        )}
        <div className="text-center mb-4">
          <label className="block text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">
            Cadastro Caixa
          </label>
        </div>
        <form className="space-y-3" onSubmit={handleSubmit}>
          <div className="flex flex-wrap gap-2">
            <div className="flex-1 min-w-[90px]">
              <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">Data</label>
              <input
                className="form-input w-full bg-gray-100 dark:bg-gray-800 dark:text-white dark:border-gray-700 rounded px-2 py-1 text-sm border border-gray-300 dark:border-gray-700"
                type="text"
                value={formatLocalDate(data)}
                readOnly
              />
            </div>
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">
                Pesquisa OS
              </label>
              <div className="flex gap-1">
                <input
                  type="text"
                  id="search_os"
                  name="search_os"
                  className="form-input w-1/2 rounded-l px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
                  placeholder="Buscar OS"
                  value={searchOs}
                  onChange={(e) => setSearchOs(e.target.value)}
                  disabled={osLoading}
                />
                <select
                  id="os-select"
                  name="REFERENCIA"
                  className="form-input w-1/2 rounded-r px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
                  value={referencia}
                  onChange={(e) => setReferencia(e.target.value)}
                  disabled={osLoading}
                >
                  {osLoading ? (
                    <option value="">Carregando OS...</option>
                  ) : filteredOsOptions.length === 0 ? (
                    <option value="">Nenhuma OS encontrada</option>
                  ) : (
                    filteredOsOptions.map((opt) => (
                      <option key={opt.id} value={opt.id}>
                        {opt.numero}
                      </option>
                    ))
                  )}
                </select>
              </div>
            </div>
            <div className="flex-1 min-w-[100px]">
              <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">Valor</label>
              <input
                required
                className="form-input w-full rounded px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
                maxLength={15}
                value={valor}
                onChange={handleValorChange}
                id="VALOR"
                name="VALOR"
                placeholder="R$ 0,00"
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">
                Forma Pagamento
              </label>
              <select
                name="FORMA"
                id="FORMA"
                className="form-input w-full rounded px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
                value={forma}
                onChange={(e) => setForma(e.target.value)}
                required
              >
                {formasPagamento.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex-1 min-w-[90px]">
              <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">Tipo</label>
              <select
                id="TIPO"
                name="TIPO"
                className="form-input w-full rounded px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
                value={tipo}
                onChange={(e) => setTipo(e.target.value)}
                required
              >
                {tipos.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1 text-gray-700 dark:text-gray-200">Descrição</label>
            <textarea
              className="form-input w-full rounded px-2 py-1 text-sm border border-gray-300 dark:bg-gray-800 dark:text-white dark:border-gray-700"
              id="DESCRICAO"
              name="DESCRICAO"
              rows={3}
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              required
            ></textarea>
          </div>
          <div className="flex flex-col sm:flex-row justify-between gap-2 mt-4">
            <button
              type="button"
              className="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-100 rounded px-4 py-2 flex-1"
              onClick={onClose}
              disabled={loading || osLoading}
            >
              Fechar
            </button>
            <button
              type="submit"
              className="bg-blue-600 dark:bg-blue-700 hover:bg-blue-700 dark:hover:bg-blue-800 text-white rounded px-4 py-2 flex-1"
              disabled={loading || osLoading}
            >
              {loading ? "Salvando..." : "Finalizar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdicionarCaixa;