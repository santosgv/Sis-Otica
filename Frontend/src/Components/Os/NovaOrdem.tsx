import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate,Link } from "react-router-dom";
import api from "../../utils/axiosConfig"


interface Cliente {
  id: number;
  NOME: string;
}

interface Vendedor {
  id: number;
  first_name: string;
}

interface Laboratorio {
  id: number;
  LABORATORIO: string;
}

interface Servico {
  id: number;
  SERVICO: string;
}

interface Produto {
  id: number;
  nome: string;
  codigo:string;
  preco_venda: string;
  quantidade: number;
}

interface Errors {
  [key: string]: string;
}


const VisualizarOSForm: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const clienteId = searchParams.get("cliente");
  const userId = localStorage.getItem("user_id");
  const [cliente, setCliente] = useState<Cliente>({ id: 0, NOME: "" });
  const [servicos, setServicos] = useState<Servico[]>([]);
  const [laboratorios, setLaboratorios] = useState<Laboratorio[]>([]);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [osData, setOsData] = useState<any>({ STATUS: "A", VENDEDOR: userId });
  const [errors, setErrors] = useState<Errors>({});
  const [loading, setLoading] = useState(false);
  const [searchArmacao, setSearchArmacao] = useState("");
  const [anexoFile, setAnexoFile] = useState<File | null>(null);
  const [searchTerm, setSearchTerm] = useState("");

  // Format number to 000.000.000.000.000,00
  const formatCurrency = (value: string): string => {
    if (!value) return "";
    const cleanValue = value.replace(/\D/g, "");
    const numberValue = parseFloat((parseInt(cleanValue) / 100).toFixed(2));
    if (isNaN(numberValue)) return "";
    return numberValue.toLocaleString("pt-BR", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  // Parse formatted currency back to number string for API (e.g., "1.234,56" -> "1234.56")
  const parseCurrency = (value: string): string => {
    if (!value) return "";
    const cleanValue = value.replace(/\./g, "").replace(",", ".");
    return cleanValue;
  };

  

  useEffect(() => {
    async function fetchData() {
      if (!clienteId) {
        setErrors({ general: "ID do cliente não fornecido na URL." });
        return;
      }
      setLoading(true);
      try {
        const [clienteRes, servicosRes, labsRes] = await Promise.all([
          api.get(`/clientes/${clienteId}/`),
          api.get("/servicos/"),
          api.get("/laboratorios/"),
        ]);

        setCliente(clienteRes.data);
        setServicos(Array.isArray(servicosRes.data) ? servicosRes.data : servicosRes.data.results || []);
        setLaboratorios(Array.isArray(labsRes.data) ? labsRes.data : labsRes.data.results || []);
      } catch (error) {
        console.error("Erro ao carregar dados:", error);
        setErrors({ general: "Erro ao carregar dados iniciais. Verifique o ID do cliente e tente novamente." });
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [clienteId]);




  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    let newValue = value;

    if ((name === "OD_CIL" || name === "OE_CIL") && value && !value.startsWith("-") && !isNaN(Number(value))) {
      newValue = `-${Math.abs(Number(value))}`;
    } else if (name === "VALOR" || name === "ENTRADA") {
      newValue = formatCurrency(value);
    }

    setOsData((prev: any) => ({ ...prev, [name]: newValue }));
    setErrors((prev) => ({ ...prev, [name]: "" }));

    if (name === "OD_CIL") {
      setErrors((prev) => ({ ...prev, OD_EIXO: newValue ? prev.OD_EIXO : "" }));
    }
    if (name === "OE_CIL") {
      setErrors((prev) => ({ ...prev, OE_EIXO: newValue ? prev.OE_EIXO : "" }));
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    setAnexoFile(file);
    setErrors((prev) => ({ ...prev, ANEXO: "" }));
  }

  function validateForm() {
    const newErrors: Errors = {};

    if (!osData.SERVICO) newErrors.SERVICO = "Serviço é obrigatório";
    if (!osData.LABORATORIO) newErrors.LABORATORIO = "Laboratório é obrigatório";
    if (!osData.VENDEDOR) newErrors.VENDEDOR = "Vendedor é obrigatório";
    if (!osData.PREVISAO_ENTREGA) {
      newErrors.PREVISAO_ENTREGA = "Previsão de entrega é obrigatória";
    } else {
      const selectedDate = new Date(osData.PREVISAO_ENTREGA);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (isNaN(selectedDate.getTime()) || selectedDate < today) {
        newErrors.PREVISAO_ENTREGA = "Data de entrega inválida ou no passado";
      }
    }
    if (!osData.VALOR || isNaN(Number(parseCurrency(osData.VALOR))) || Number(parseCurrency(osData.VALOR)) <= 0) {
      newErrors.VALOR = "Valor é obrigatório e deve ser um número positivo";
    }
    if (!osData.ENTRADA || isNaN(Number(parseCurrency(osData.ENTRADA))) || Number(parseCurrency(osData.ENTRADA)) < 0) {
      newErrors.ENTRADA = "Entrada é obrigatória e deve ser um número não negativo";
    }
    if (!osData.FORMA_PAG) newErrors.FORMA_PAG = "Forma de pagamento é obrigatória";
    if (!osData.QUANTIDADE_PARCELA || Number(osData.QUANTIDADE_PARCELA) < 1) {
      newErrors.QUANTIDADE_PARCELA = "Quantidade de parcelas deve ser entre 1 e 10";
    }
    if (osData.OD_CIL && !osData.OD_EIXO) newErrors.OD_EIXO = "Eixo é obrigatório quando CIL é preenchido";
    if (osData.OE_CIL && !osData.OE_EIXO) newErrors.OE_EIXO = "Eixo é obrigatório quando CIL é preenchido";

    setErrors(newErrors);
    console.log("Validation errors:", newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    console.log("handleSubmit called");
    if (!validateForm()) {
      console.log("Validation failed");
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("CLIENTE", String(Number(clienteId)));
      formData.append("VENDEDOR", String(Number(userId)));
      formData.append("SERVICO", String(Number(osData.SERVICO)));
      formData.append("LABORATORIO", String(Number(osData.LABORATORIO)));
      formData.append("STATUS", osData.STATUS || "A");
      if (anexoFile) formData.append("ANEXO", anexoFile);
      formData.append("ASSINATURA", "");
      [
        "OD_ESF",
        "OD_CIL",
        "OD_EIXO",
        "OE_ESF",
        "OE_CIL",
        "OE_EIXO",
        "AD",
        "DNP",
        "P",
        "DPA",
        "DIAG",
        "V",
        "H",
        "ALT",
        "ARM",
        "MONTAGEM",
        "LENTES",
        "ARMACAO",
        "OBSERVACAO",
        "FORMA_PAG",
      ].forEach((field) => formData.append(field, osData[field] || ""));
      formData.append("VALOR", parseCurrency(osData.VALOR));
      formData.append("QUANTIDADE_PARCELA", String(Number(osData.QUANTIDADE_PARCELA) || 1));
      formData.append("ENTRADA", parseCurrency(osData.ENTRADA));
      formData.append("PREVISAO_ENTREGA", osData.PREVISAO_ENTREGA);

      for (const pair of formData.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`);
      }

      const response = await api.post("/ordens/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (osData.ARMACAO) {
        await realizarSaidaEstoque(osData.ARMACAO);
      }
  
      navigate(`/os?id=${response.data.id}`);
    } catch (err: any) {
      console.error("Erro ao salvar a ordem:", err);
      setErrors({
        general: err.response?.data?.detail || JSON.stringify(err.response?.data) || "Erro ao salvar a ordem. Verifique os dados e tente novamente.",
      });
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
  const fetchProdutos = async () => {
    try {
      if (searchTerm.trim() === "") {
        // Buscar todos os produtos
        const response = await api.get("/produtos/");
        setProdutos(Array.isArray(response.data.results) ? response.data.results : response.data);
      } else {
        // Buscar pelo código exato removendo os hífens
        const response = await api.get("/search_products/", {
          params: { search_products: searchTerm.replace(/-/g, "") },
        });

        if (response.data && Array.isArray(response.data.results) && response.data.results.length > 0) {
        const produto = response.data.results[0];
        setProdutos([produto]);
        setOsData((prev: typeof VisualizarOSForm) => ({ ...prev, ARMACAO: String(produto.id) }));
      } else {
        setProdutos([]);
        setOsData((prev: typeof VisualizarOSForm) => ({ ...prev, ARMACAO: "" }));
}
      }
    } catch (error) {
      console.error("Erro ao buscar produtos:", error);
    }
  };

  const debounce = setTimeout(fetchProdutos, 500); // debounce de 0.5s
  return () => clearTimeout(debounce);
}, [searchTerm]);



    const realizarSaidaEstoque = async (produtoId: number) => {
      try {
        const response = await api.post('/realizar_saida_api/', {
          produto_id: produtoId,
          quantidade: 1,
          motivo: 'Venda por OS',
        });


      } catch (error: any) {
        const message =
          error.response?.data?.error || 'Erro ao realizar saída de estoque';
        console.error('Erro ao dar baixa no estoque:', message);
        alert(message);
      }
    };

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-80px)] flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <p className="text-gray-900 dark:text-white">Carregando...</p>
      </div>
    );
  }

  if (errors.general && !cliente.id) {
    return (
      <div className="min-h-[calc(100vh-80px)] flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="bg-red-100 text-red-800 p-4 rounded-lg dark:bg-red-900 dark:text-red-100">
          {errors.general}
        </div>
      </div>
    );
  }


  return (
    <section className="min-h-[calc(100vh-80px)] flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors duration-300 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto w-full">
        <div className="sticky top-20 z-10 bg-white dark:bg-gray-900 pb-4">
          <nav aria-label="breadcrumb" className="mb-4">
            <ol className="flex flex-wrap gap-2 text-sm text-gray-600 dark:text-gray-300">
              <li>
                <a href="/pesquisa" className="hover:text-blue-600 dark:hover:text-blue-400">
                  O.S
                </a>
              </li>
              <li> / </li>
              <li className="text-gray-900 dark:text-white">Cadastro de O.S</li>
            </ol>
                        <div className="flex flex-wrap gap-2 justify-start mb-4 w-full">
            <Link
            to={"/laboratorio-cadastro"}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center"
            >
            <a>Laborarios</a>
            </Link> 
            <Link
            to={"/servicos-cadastro"}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center">
            <a>Serviços</a>
            </Link>        
          </div>
          </nav>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
              Cadastrar O.S
            </h2>
            <button
              onClick={() => navigate(-1)}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition"
              disabled={loading}
            >
              ← Voltar
            </button>
          </div>
          {errors.general && (
            <div className="bg-red-100 text-red-800 p-4 rounded-lg dark:bg-red-900 dark:text-red-100 mb-6">
              {errors.general}
            </div>
          )}
        </div>
        <form
          onSubmit={handleSubmit}
          className="bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6 sm:p-8 space-y-8"
          encType="multipart/form-data"
        >
          {/* Geral */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Geral</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Cliente
                </label>
                <input
                  readOnly
                  value={cliente.NOME}
                  className="w-full px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-200 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Tipo de Serviço
                </label>
                <select
                  name="SERVICO"
                  value={osData.SERVICO || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                >
                  <option value="">Selecione</option>
                  {servicos.map((serv) => (
                    <option key={serv.id} value={serv.id}>
                      {serv.SERVICO}
                    </option>
                  ))}
                </select>
                {errors.SERVICO && <p className="text-red-500 text-sm mt-1">{errors.SERVICO}</p>}
              </div>
            </div>
          </div>

                  <hr />
          {/* Receita */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">Receita</h3>
            <div className="grid grid-cols-[auto_1fr_1fr_1fr] gap-4 items-center">
              {/* Linha OD */}
              <div className="justify-self-end font-medium text-gray-700 dark:text-gray-200">OD</div>
              <input
                type="text"
                name="OD_ESF"
                maxLength={6}
                value={osData.OD_ESF || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="ESF"
              />
              <input
                type="text"
                name="OD_CIL"
                maxLength={6}
                value={osData.OD_CIL || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="CIL"
              />
              <input
                type="text"
                name="OD_EIXO"
                maxLength={6}
                value={osData.OD_EIXO || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="EIXO"
              />

              {/* Linha OE */}
              <div className="justify-self-end font-medium text-gray-700 dark:text-gray-200">OE</div>
              <input
                type="text"
                name="OE_ESF"
                maxLength={6}
                value={osData.OE_ESF || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="ESF"
              />
              <input
                type="text"
                name="OE_CIL"
                maxLength={6}
                value={osData.OE_CIL || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="CIL"
              />
              <input
                type="text"
                name="OE_EIXO"
                maxLength={6}
                value={osData.OE_EIXO || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="EIXO"
              />

              {/* Linha AD */}
              <div className="justify-self-end font-medium text-gray-700 dark:text-gray-200">AD</div>
              <input
                type="text"
                name="AD"
                maxLength={6}
                value={osData.AD || ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border"
                placeholder="AD"
              />
              <div className="col-span-2">
                <input
                  type="file"
                  name="ANEXO"
                  onChange={handleFileChange}
                  className="w-full px-4 py-2 rounded-lg border"
                />
              </div>
            </div>
          </div>

                  <hr />
          {/* Laboratório */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">Laboratório</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-6 gap-4 sm:gap-6">
              <div className="sm:col-span-2 lg:col-span-3">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Laboratório
                </label>
                <select
                  name="LABORATORIO"
                  value={osData.LABORATORIO || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                >
                  <option value="">Selecione</option>
                  {laboratorios.map((lab) => (
                    <option key={lab.id} value={lab.id}>
                      {lab.LABORATORIO}
                    </option>
                  ))}
                </select>
                {errors.LABORATORIO && <p className="text-red-500 text-sm mt-1">{errors.LABORATORIO}</p>}
              </div>
              {["DNP", "P", "DPA", "DIAG", "V", "H"].map((field) => (
                <div key={field}>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                    {field}
                  </label>
                  <input
                    type="text"
                    name={field}
                    maxLength={field === "DNP" ? 15 : 6}
                    value={osData[field] || ""}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                    placeholder={field}
                  />
                  {errors[field] && <p className="text-red-500 text-sm mt-1">{errors[field]}</p>}
                </div>
              ))}
              {["ALT", "ARM", "MONTAGEM"].map((field) => (
                <div key={field} className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                    {field === "MONTAGEM" ? "Montagem" : field}
                  </label>
                  <input
                    type="text"
                    name={field}
                    maxLength={field === "ALT" ? 6 : 50}
                    value={osData[field] || ""}
                    onChange={handleChange}
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                    placeholder={field === "MONTAGEM" ? "Montagem" : field}
                  />
                  {errors[field] && <p className="text-red-500 text-sm mt-1">{errors[field]}</p>}
                </div>
              ))}
            </div>
          </div>

          {/* Lentes */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">Lentes</h3>
            <div className="grid grid-cols-1">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Lentes</label>
                <input
                  type="text"
                  name="LENTES"
                  maxLength={150}
                  value={osData.LENTES || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                />
                {errors.LENTES && <p className="text-red-500 text-sm mt-1">{errors.LENTES}</p>}
              </div>
            </div>
          </div>

          {/* Armação */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Armação</h3>
            <div className="grid grid-cols-1">
              <div className="flex items-center gap-2">
                <div className="relative flex-1">
                  <input
                    type="text"
                    placeholder="Buscar produto..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="border p-2 rounded"
                />
                  <svg
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
              <select
                name="ARMACAO"
                key={osData.ARMACAO}
                value={osData.ARMACAO ?? ""}
                onChange={handleChange}
                className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              >
                <option value="" disabled>
                  Selecione uma armação
                </option>
                {produtos.map((produto) => (
                  <option key={produto.id} value={String(produto.codigo)}>
                  {produto.codigo} - {produto.nome} ({produto.quantidade} un.) - R$ {produto.preco_venda}
                </option>
                ))}
              </select>
              </div>
              {errors.ARMACAO && <p className="text-red-500 text-sm mt-1">{errors.ARMACAO}</p>}
            </div>
          </div>

          {/* Observação */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Observação</h3>
            <div className="grid grid-cols-1">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Observação ({osData.OBSERVACAO?.length || 0}/80)
                </label>
                <textarea
                  name="OBSERVACAO"
                  value={osData.OBSERVACAO || ""}
                  onChange={handleChange}
                  maxLength={80}
                  rows={2}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                />
                {errors.OBSERVACAO && <p className="text-red-500 text-sm mt-1">{errors.OBSERVACAO}</p>}
              </div>
            </div>
          </div>
                <hr />
          {/* Financeiro */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">Financeiro</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 sm:gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Pagamento
                </label>
                <select
                  name="FORMA_PAG"
                  value={osData.FORMA_PAG || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                >
                  <option value="">Selecione</option>
                  <option value="A">PIX</option>
                  <option value="B">Dinheiro</option>
                  <option value="C">Débito</option>
                  <option value="D">Crédito</option>
                  <option value="E">Carnê</option>
                  <option value="F">Permuta</option>
                </select>
                {errors.FORMA_PAG && <p className="text-red-500 text-sm mt-1">{errors.FORMA_PAG}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Valor</label>
                <input
                  type="text"
                  maxLength={10}
                  name="VALOR"
                  value={osData.VALOR || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  placeholder="0,00"
                />
                {errors.VALOR && <p className="text-red-500 text-sm mt-1">{errors.VALOR}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Parcelas
                </label>
                <select
                  name="QUANTIDADE_PARCELA"
                  value={osData.QUANTIDADE_PARCELA || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                >
                  <option value="">Escolha...</option>
                  {Array.from({ length: 10 }, (_, i) => i + 1).map((num) => (
                    <option key={num} value={num}>
                      {num}x
                    </option>
                  ))}
                </select>
                {errors.QUANTIDADE_PARCELA && (
                  <p className="text-red-500 text-sm mt-1">{errors.QUANTIDADE_PARCELA}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Valor Pago
                </label>
                <input
                  type="text"
                  name="ENTRADA"
                  maxLength={10}
                  value={osData.ENTRADA || ""}
                  onChange={handleChange}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  placeholder="0,00"
                />
                {errors.ENTRADA && <p className="text-red-500 text-sm mt-1">{errors.ENTRADA}</p>}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
                  Previsão de Entrega
                </label>
                <input
                  type="date"
                  name="PREVISAO_ENTREGA"
                  value={osData.PREVISAO_ENTREGA || ""}
                  onChange={handleChange}
                  min={new Date().toISOString().split("T")[0]}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                  required
                />
                {errors.PREVISAO_ENTREGA && (
                  <p className="text-red-500 text-sm mt-1">{errors.PREVISAO_ENTREGA}</p>
                )}
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row justify-center gap-4 mt-8">
            <button
              type="submit"
              className="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? "Salvando..." : "Finalizar Pedido"}
            </button>
            <button
              type="button"
              onClick={() => navigate("/clientes")}
              className="px-6 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
              disabled={loading}
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default VisualizarOSForm;