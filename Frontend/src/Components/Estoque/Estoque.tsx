import React, { useState, useEffect } from "react";
import { useNavigate,Link } from "react-router-dom";

import { Input } from "../ui/Input";
import { Select } from "../ui/Select";
import { Button } from "../ui/Button";
import api from "../../utils/axiosConfig"

interface Fornecedor {
  id: number;
  nome: string;
}

interface Tipo {
  id: number;
  nome: string;
}

interface Estilo {
  id: number;
  nome: string;
}

interface TipoUnitario {
  id: number;
  nome: string;
}

interface Produto {
  id: number;
  importado: boolean;
  conferido: boolean;
  chavenfe: string | null;
  codigo: string;
  nome: string;
  preco_unitario: string;
  preco_venda: string;
  quantidade: number;
  quantidade_minima: number;
  valor_total: string;
  fornecedor: number;
  Tipo: number;
  Estilo: number;
  tipo_unitario: number;
}

const Estoque: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    chavenfe: "",
    nome: "",
    fornecedor: "",
    tipo: "",
    estilo: "",
    preco_unitario: "",
    preco_venda: "",
    quantidade: "",
    quantidade_minima: "",
    tipo_unitario: "",
    importado: false,
    conferido: false,
  });
  const [fornecedores, setFornecedores] = useState<Fornecedor[]>([]);
  const [tipos, setTipos] = useState<Tipo[]>([]);
  const [estilos, setEstilos] = useState<Estilo[]>([]);
  const [unitarios, setUnitarios] = useState<TipoUnitario[]>([]);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [itensPorPagina] = useState(5);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [mensagem, setMensagem] = useState<string>("");
  const [mensagemTipo, setMensagemTipo] = useState<"sucesso" | "erro" | "">("");
  const [loading, setLoading] = useState(false);
  const [entradaId, setEntradaId] = useState<number | null>(null);
  const [retiradaId, setRetiradaId] = useState<number | null>(null);
  const [quantidadeMovimento, setQuantidadeMovimento] = useState("");
  const userFuncao = "G"; // Placeholder para função do usuário

  // Funções para buscar dados dos endpoints
  const fetchFornecedores = async () => {
    try {
      const response = await api.get("/fornecedor/");
      setFornecedores(response.data.results);
    } catch (error) {
      setMensagem("Erro ao carregar fornecedores!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const fetchTipos = async () => {
    try {
      const response = await api.get("/tipo/");
      setTipos(response.data.results);
    } catch (error) {
      setMensagem("Erro ao carregar tipos!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const fetchEstilos = async () => {
    try {
      const response = await api.get("/estilo/");
      setEstilos(response.data.results);
    } catch (error) {
      setMensagem("Erro ao carregar estilos!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const fetchTiposUnitarios = async () => {
    try {
      const response = await api.get("/tipounitario/");
      setUnitarios(response.data.results);
    } catch (error) {
      setMensagem("Erro ao carregar tipos unitários!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const fetchProdutos = async () => {
    setLoading(true);
    try {
      const response = await api.get("/produtos/", {
        params: {
          page: paginaAtual,
          page_size: itensPorPagina,
        },
      });
      setProdutos(response.data.results);
      setTotalPaginas(Math.ceil(response.data.count / itensPorPagina));
    } catch (error) {
      setMensagem("Erro ao carregar produtos!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    } finally {
      setLoading(false);
    }
  };

  // Carregar dados iniciais
  useEffect(() => {
    fetchFornecedores();
    fetchTipos();
    fetchEstilos();
    fetchTiposUnitarios();
    fetchProdutos();
  }, [paginaAtual]);

  // Manipulação do formulário
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setForm((prev) => ({
        ...prev,
        [name]: checked,
      }));
    } else {
      setForm((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.nome.trim()) {
      setMensagem("O nome do produto não pode estar vazio!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    if (!form.fornecedor || !form.tipo || !form.estilo || !form.tipo_unitario) {
      setMensagem("Selecione fornecedor, tipo, estilo e tipo unitário!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      const response = await api.post("/produtos/", {
        ...form,
        fornecedor: Number(form.fornecedor),
        Tipo: Number(form.tipo),
        Estilo: Number(form.estilo),
        tipo_unitario: Number(form.tipo_unitario),
        preco_unitario: Number(form.preco_unitario) || 0,
        preco_venda: Number(form.preco_venda) || 0,
        quantidade: Number(form.quantidade) || 0,
        quantidade_minima: Number(form.quantidade_minima) || 0,
        chavenfe: form.chavenfe || null,
      });
      setProdutos((prev) => [...prev, response.data]);
      setForm({
        chavenfe: "",
        nome: "",
        fornecedor: "",
        tipo: "",
        estilo: "",
        preco_unitario: "",
        preco_venda: "",
        quantidade: "",
        quantidade_minima: "",
        tipo_unitario: "",
        importado: false,
        conferido: false,
      });
      setMensagem("Produto cadastrado com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      fetchProdutos();
    } catch (error) {
      setMensagem("Erro ao cadastrar produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  // Funções para entrada e retirada
  const handleEntrada = (id: number) => {
    setEntradaId(id);
    setQuantidadeMovimento("");
  };

  const handleRetirada = (id: number) => {
    setRetiradaId(id);
    setQuantidadeMovimento("");
  };

  const confirmEntrada = async () => {
    if (!quantidadeMovimento || Number(quantidadeMovimento) <= 0) {
      setMensagem("Quantidade deve ser maior que zero!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      const produto = produtos.find((p) => p.id === entradaId);
      if (produto) {
        const novaQuantidade = produto.quantidade + Number(quantidadeMovimento);
        await api.put(`/produtos/${entradaId}/`, {
          ...produto,
          quantidade: novaQuantidade,
        });
        setProdutos((prev) =>
          prev.map((p) =>
            p.id === entradaId ? { ...p, quantidade: novaQuantidade } : p
          )
        );
        setMensagem("Entrada de produto realizada com sucesso!");
        setMensagemTipo("sucesso");
        setTimeout(() => {
          setMensagem("");
          setMensagemTipo("");
        }, 2500);
      }
      setEntradaId(null);
      setQuantidadeMovimento("");
    } catch (error) {
      setMensagem("Erro ao realizar entrada de produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const confirmRetirada = async () => {
    if (!quantidadeMovimento || Number(quantidadeMovimento) <= 0) {
      setMensagem("Quantidade deve ser maior que zero!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      const produto = produtos.find((p) => p.id === retiradaId);
      if (produto) {
        const novaQuantidade = produto.quantidade - Number(quantidadeMovimento);
        if (novaQuantidade < 0) {
          setMensagem("Quantidade insuficiente em estoque!");
          setMensagemTipo("erro");
          setTimeout(() => {
            setMensagem("");
            setMensagemTipo("");
          }, 2500);
          return;
        }
        await api.put(`/produtos/${retiradaId}/`, {
          ...produto,
          quantidade: novaQuantidade,
        });
        setProdutos((prev) =>
          prev.map((p) =>
            p.id === retiradaId ? { ...p, quantidade: novaQuantidade } : p
          )
        );
        setMensagem("Retirada de produto realizada com sucesso!");
        setMensagemTipo("sucesso");
        setTimeout(() => {
          setMensagem("");
          setMensagemTipo("");
        }, 2500);
      }
      setRetiradaId(null);
      setQuantidadeMovimento("");
    } catch (error) {
      setMensagem("Erro ao realizar retirada de produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const cancelMovimento = () => {
    setEntradaId(null);
    setRetiradaId(null);
    setQuantidadeMovimento("");
  };

  const handleGerarRelatorio = async () => {
    try {
      setLoading(true);
      setMensagem("");

      // Faz a requisição para o endpoint com responseType: 'blob'
      const response = await api.get("/gerar_relatorio_estoque_conferido", {
        responseType: "blob", // Para receber dados binários (PDF)
      });

      // Cria um objeto Blob a partir da resposta
      const blob = new Blob([response.data], { type: "application/pdf" });

      // Cria um URL temporário para o Blob
      const url = window.URL.createObjectURL(blob);

      // Cria um link temporário para download
      const link = document.createElement("a");
      link.href = url;
      link.download = "relatorio_estoque_conferido.pdf"; // Nome do arquivo
      document.body.appendChild(link);
      link.click();

      // Remove o link e libera o URL
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setMensagem("Relatório baixado com sucesso!");
      setTimeout(() => setMensagem(""), 2500);
    } catch (e) {
      console.error("Erro ao baixar relatório:", e);
      setMensagem("Erro ao baixar o relatório. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };



  
  return (
   <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-4 bg-white dark:bg-gray-900 min-h-screen transition-colors duration-300 flex justify-start">
  <div className="w-full max-w-full md:w-[1200px] lg:w-[1100px] xl:w-[1000px] 2xl:w-[900px] mx-auto min-w-0">

        {/* Mensagem fixa */}
        {mensagem && (
          <div
            className={`fixed z-50 px-3 py-1 rounded shadow text-sm font-medium text-left transition-opacity duration-300 ${
              mensagemTipo === "sucesso" ? "bg-green-500 text-white" : "bg-red-500 text-white"
            }`}
            style={{ left: 278, top: 104 }}
          >
            {mensagem}
          </div>
        )}
        {/* Botões de ação (apenas gerente) */}
        {userFuncao === "G" && (
          <div className="flex flex-wrap gap-2 justify-start mb-4 w-full">
            <Link
            to={"/fornecedores"}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center"
            >
            <a>Fornecedores</a>
            </Link> 
            <Link
            to={"/tipos"}
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center">
            <a>Tipos</a>
            </Link>        
             <Link
            to={"/estilos"}
            className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center"
            >
            <a>Estilos</a>
            </Link>
            <Link
            to={"/tipos-unitarios"}
            className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center"
            >
            <a>Tipos Und</a>
            </Link>
            <button
              onClick={handleGerarRelatorio}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-1.5 sm:py-2 px-3 sm:px-4 rounded text-xs sm:text-base min-w-[90px] text-center"
            >
              Baixar Relatório Conferência
            </button>
          </div>
        )}
        {/* Formulário de cadastro */}
        {userFuncao === "G" && (
          <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded shadow p-4 mb-4">
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Chave NF</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="chavenfe"
                  value={form.chavenfe}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Nome</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="nome"
                  value={form.nome}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Fornecedor</label>
                <Select
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="fornecedor"
                  value={form.fornecedor}
                  onChange={handleChange}
                >
                  <option value="">Selecione um fornecedor...</option>
                  {fornecedores.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.nome}
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Tipo</label>
                <Select
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="tipo"
                  value={form.tipo}
                  onChange={handleChange}
                >
                  <option value="">Selecione um tipo...</option>
                  {tipos.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.nome}
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Estilo</label>
                <Select
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="estilo"
                  value={form.estilo}
                  onChange={handleChange}
                >
                  <option value="">Selecione um estilo...</option>
                  {estilos.map((e) => (
                    <option key={e.id} value={e.id}>
                      {e.nome}
                    </option>
                  ))}
                </Select>
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Preço unitário</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="preco_unitario"
                  value={form.preco_unitario}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Preço venda</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="preco_venda"
                  value={form.preco_venda}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Quantidade</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="quantidade"
                  value={form.quantidade}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Quantidade mínima</label>
                <Input
                  type="text"
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="quantidade_minima"
                  value={form.quantidade_minima}
                  onChange={handleChange}
                />
              </div>
              <div>
                <label className="block text-gray-700 dark:text-gray-300">Tipo Unitário</label>
                <Select
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                  name="tipo_unitario"
                  value={form.tipo_unitario}
                  onChange={handleChange}
                >
                  <option value="">Selecione um tipo unitário...</option>
                  {unitarios.map((u) => (
                    <option key={u.id} value={u.id}>
                      {u.nome}
                    </option>
                  ))}
                </Select>
              </div>
            </div>
            <div className="mt-4 flex flex-col md:flex-row gap-4">
              <label className="inline-flex items-center cursor-pointer select-none">
                <input
                  className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:checked:bg-blue-600 dark:checked:border-blue-600 focus:ring-blue-500"
                  type="checkbox"
                  name="importado"
                  checked={form.importado}
                  onChange={handleChange}
                />
                <span className="ml-2 text-gray-700 dark:text-gray-300">Importado</span>
              </label>
              <label className="inline-flex items-center cursor-pointer select-none">
                <input
                  className="form-checkbox h-5 w-5 text-blue-600 transition duration-150 ease-in-out border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:checked:bg-blue-600 dark:checked:border-blue-600 focus:ring-blue-500"
                  type="checkbox"
                  name="conferido"
                  checked={form.conferido}
                  onChange={handleChange}
                />
                <span className="ml-2 text-gray-700 dark:text-gray-300">Conferido</span>
              </label>
            </div>
            <Button
              type="submit"
              className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Cadastrar
            </Button>
          </form>
        )}
        <hr className="my-4" />
        {/* Lista de produtos */}
        <div id="list-products" className="mb-3">
          <div className="mb-2 text-gray-700 dark:text-gray-300">
            Quantidade <span className="bg-green-500 text-white px-2 py-1 rounded">{produtos.length}</span>
          </div>
          {loading ? (
            <div className="bg-gray-100 dark:bg-gray-800 rounded p-3 text-center text-gray-500 dark:text-gray-400">
              Carregando...
            </div>
          ) : produtos.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full md:min-w-[700px] bg-gray-100 dark:bg-gray-800 rounded text-gray-900 dark:text-gray-200">
                <thead>
                  <tr>
                    <th className="px-4 py-2 border-b text-left">Importado</th>
                    <th className="px-4 py-2 border-b text-left">Conferido</th>
                    <th className="px-4 py-2 border-b text-left">Código</th>
                    <th className="px-4 py-2 border-b text-left">Nome</th>
                    <th className="px-4 py-2 border-b text-center">Fornecedor</th>
                    <th className="px-4 py-2 border-b text-center">Preço Unitário</th>
                    <th className="px-4 py-2 border-b text-center">Preço Venda</th>
                    <th className="px-4 py-2 border-b text-center">Qtd</th>
                    <th className="px-4 py-2 border-b text-center">Qtd Mínima</th>
                    <th className="px-4 py-2 border-b text-center">Tipo</th>
                    <th className="px-4 py-2 border-b text-center">R$</th>
                    <th className="px-4 py-2 border-b text-center">Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {produtos.map((p) => (
                    <tr
                      key={p.id}
                      className="border-b border-gray-200 dark:border-gray-700 last:border-b-0 hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      <td className="px-4 py-2 border-b">
                        <input
                          type="checkbox"
                          checked={p.importado}
                          
                          className="form-checkbox h-5 w-5 text-blue-600"
                        />
                      </td>
                      <td className="px-4 py-2 border-b">
                        <input
                          type="checkbox"
                          checked={p.conferido}
                          
                          className="form-checkbox h-5 w-5 text-blue-600"
                        />
                      </td>
                      <td className="px-4 py-2 border-b">{p.codigo}</td>
                      <td className="px-4 py-2 border-b">

                      <Link
                        to={`/produtos/${p.id}`}
                        className="text-blue-600 hover:text-blue-800">
                        <a>{p.nome}</a>
                        </Link>
                      </td>
                      <td className="px-4 py-2 border-b text-center">
                        {fornecedores.find((f) => f.id === p.fornecedor)?.nome || "N/A"}
                      </td>
                      <td className="px-4 py-2 border-b text-center">{p.preco_unitario}</td>
                      <td className="px-4 py-2 border-b text-center">{p.preco_venda}</td>
                      <td className="px-4 py-2 border-b text-center">{p.quantidade}</td>
                      <td className="px-4 py-2 border-b text-center">{p.quantidade_minima}</td>
                      <td className="px-4 py-2 border-b text-center">
                        {tipos.find((t) => t.id === p.Tipo)?.nome || "N/A"}
                      </td>
                      <td className="px-4 py-2 border-b text-center">{p.valor_total}</td>
                      <td className="px-4 py-2 border-b text-center">
                        <button
                          className="text-green-600 hover:text-green-800 mr-2"
                          onClick={() => handleEntrada(p.id)}
                          title="Entrada"
                          aria-label="Registrar entrada de produto"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-5 w-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 4v16m8-8H4"
                            />
                          </svg>
                        </button>
                        <button
                          className="text-red-600 hover:text-red-800"
                          onClick={() => handleRetirada(p.id)}
                          title="Retirada"
                          aria-label="Registrar retirada de produto"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-5 w-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M20 12H4"
                            />
                          </svg>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="bg-gray-100 dark:bg-gray-800 rounded p-3 text-center text-gray-500 dark:text-gray-400">
              Nenhum produto cadastrado.
            </div>
          )}
        </div>
        {/* Paginação */}
        <div className="flex justify-center items-center gap-2 mt-4">
          <Button
            className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded"
            disabled={paginaAtual === 1}
            onClick={() => setPaginaAtual(paginaAtual - 1)}
            aria-label="Página anterior"
          >
            {"<"}
          </Button>
          <span className="text-gray-700 dark:text-gray-300">
            {paginaAtual} de {totalPaginas}
          </span>
          <Button
            className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-bold py-2 px-4 rounded"
            disabled={paginaAtual === totalPaginas || totalPaginas === 0}
            onClick={() => setPaginaAtual(paginaAtual + 1)}
            aria-label="Próxima página"
          >
            {">"}
          </Button>
        </div>
        {/* Modal de entrada */}
        {entradaId !== null && (
          <div
            className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50"
            role="dialog"
            aria-labelledby="modal-entrada-title"
          >
            <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
              <h3
                id="modal-entrada-title"
                className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100"
              >
                Entrada de Produto
              </h3>
              <p className="mb-4 text-gray-700 dark:text-gray-300">
                Informe a quantidade a ser adicionada:
              </p>
              <Input
                type="number"
                className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                value={quantidadeMovimento}
                onChange={(e) => setQuantidadeMovimento(e.target.value)}
                placeholder="Quantidade"
                min="1"
              />
              <div className="flex justify-end gap-2 mt-4">
                <Button
                  className="bg-green-500 hover:bg-green-700 text-white px-4 py-2 rounded"
                  onClick={confirmEntrada}
                  aria-label="Confirmar entrada"
                >
                  Confirmar
                </Button>
                <Button
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                  onClick={cancelMovimento}
                  aria-label="Cancelar entrada"
                >
                  Cancelar
                </Button>
              </div>
            </div>
          </div>
        )}
        {/* Modal de retirada */}
        {retiradaId !== null && (
          <div
            className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50"
            role="dialog"
            aria-labelledby="modal-retirada-title"
          >
            <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
              <h3
                id="modal-retirada-title"
                className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100"
              >
                Retirada de Produto
              </h3>
              <p className="mb-4 text-gray-700 dark:text-gray-300">
                Informe a quantidade a ser retirada:
              </p>
              <Input
                type="number"
                className="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                value={quantidadeMovimento}
                onChange={(e) => setQuantidadeMovimento(e.target.value)}
                placeholder="Quantidade"
                min="1"
              />
              <div className="flex justify-end gap-2 mt-4">
                <Button
                  className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded"
                  onClick={confirmRetirada}
                  aria-label="Confirmar retirada"
                >
                  Confirmar
                </Button>
                <Button
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                  onClick={cancelMovimento}
                  aria-label="Cancelar retirada"
                >
                  Cancelar
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Estoque;