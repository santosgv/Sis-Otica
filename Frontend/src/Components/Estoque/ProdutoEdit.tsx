import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
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

const ProdutoEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    chavenfe: "",
    codigo: '',
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
  const [mensagem, setMensagem] = useState<string>("");
  const [mensagemTipo, setMensagemTipo] = useState<"sucesso" | "erro" | "">("");
  const [loading, setLoading] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);


  // Funções para buscar dados
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

  const fetchProduto = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/produtos/${id}/`);
      const produto = response.data;
      setForm({
        chavenfe: produto.chavenfe || "",
        codigo: produto.codigo || "",
        nome: produto.nome,
        fornecedor: produto.fornecedor.toString(),
        tipo: produto.Tipo.toString(),
        estilo: produto.Estilo.toString(),
        preco_unitario: produto.preco_unitario,
        preco_venda: produto.preco_venda,
        quantidade: produto.quantidade.toString(),
        quantidade_minima: produto.quantidade_minima.toString(),
        tipo_unitario: produto.tipo_unitario.toString(),
        importado: produto.importado,
        conferido: produto.conferido,
      });
      console.log(produto)
    } catch (error) {
      setMensagem("Erro ao carregar produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFornecedores();
    fetchTipos();
    fetchEstilos();
    fetchTiposUnitarios();
    fetchProduto();
  }, [id]);

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
    if (Number(form.preco_unitario) < 0 || Number(form.preco_venda) < 0) {
      setMensagem("Preços não podem ser negativos!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    if (Number(form.quantidade) < 0 || Number(form.quantidade_minima) < 0) {
      setMensagem("Quantidades não podem ser negativas!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
      return;
    }
    try {
      await api.put(`/produtos/${id}/`, {
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
      setMensagem("Produto atualizado com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    } catch (error) {
      setMensagem("Erro ao atualizar produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const handleDelete = () => {
    setDeleteId(Number(id));
  };

  const confirmDelete = async () => {
    try {
      await api.delete(`/produtos/${deleteId}/`);
      setMensagem("Produto excluído com sucesso!");
      setMensagemTipo("sucesso");
      setTimeout(() => {
        navigate("/estoque");
      }, 2500);
    } catch (error) {
      setMensagem("Erro ao excluir produto!");
      setMensagemTipo("erro");
      setTimeout(() => {
        setMensagem("");
        setMensagemTipo("");
      }, 2500);
    }
  };

  const cancelDelete = () => {
    setDeleteId(null);
  };


const handleGerarEtiquetas = async (codigo: string, quantidade: number = 1) => {
  try {
    setLoading(true);
    setMensagem("");
  

    // Faz a requisição para o endpoint de geração de etiquetas
    const response = await api.get(`/etiquetas/${codigo}/${quantidade}/`, {
      responseType: "blob", // PDF é binário
    });

    // Cria o blob para PDF
    const blob = new Blob([response.data], { type: "application/pdf" });

    // Cria a URL e faz o download
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `etiquetas_${codigo}.pdf`;
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    setMensagem("Etiquetas geradas com sucesso!");
    setTimeout(() => setMensagem(""), 2500);
  } catch (error) {
    console.error("Erro ao gerar etiquetas:", error);
    setMensagem("Erro ao gerar etiquetas. Tente novamente.");
  } finally {
    setLoading(false);
  }
};




  if (loading) {
    return (
      <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-4 bg-white dark:bg-gray-900 min-h-screen transition-colors duration-300 flex justify-center">
        <div className="text-gray-500 dark:text-gray-400">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="w-full min-w-0 px-2 sm:px-4 md:px-8 py-4 bg-white dark:bg-gray-900 min-h-screen transition-colors duration-300 flex justify-start">
      <div className="w-full max-w-full md:w-[1200px] lg:w-[1100px] xl:w-[1000px] 2xl:w-[900px] mr-auto min-w-0">
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
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">
          Editar Produto
        </h2>
        <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 rounded shadow p-4 mb-4">
          <h1 className="text-center">Codigo</h1>
          <h1 className="text-center">{form.codigo}</h1>
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
          <div className="mt-4 flex gap-4">
            <Button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Salvar
            </Button>
            <Button
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              onClick={handleDelete}
            >
              Excluir
            </Button>
            <Button
              className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
              onClick={() => navigate("/estoque")}
            >
              Voltar
            </Button>
            <Button className="bg-green-500 hover:bg-green-400  font-bold py-2 px-4 rounded" onClick={() => handleGerarEtiquetas(String(form.codigo), Number(form.quantidade))}>Imprimir Etiqueta</Button>
          </div>
        </form>
        {/* Modal de confirmação de exclusão */}
        {deleteId !== null && (
          <div
            className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50"
            role="dialog"
            aria-labelledby="modal-title"
          >
            <div className="bg-white dark:bg-gray-800 rounded shadow-lg p-6 w-full max-w-sm">
              <h3
                id="modal-title"
                className="text-lg font-bold mb-2 text-gray-800 dark:text-gray-100"
              >
                Confirmar exclusão
              </h3>
              <p className="mb-4 text-gray-700 dark:text-gray-300">
                Deseja realmente excluir este produto?
              </p>
              <div className="flex justify-end gap-2">
                <Button
                  className="bg-red-500 hover:bg-red-700 text-white px-4 py-2 rounded"
                  onClick={confirmDelete}
                  aria-label="Confirmar exclusão"
                >
                  Excluir
                </Button>
                <Button
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                  onClick={cancelDelete}
                  aria-label="Cancelar exclusão"
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

export default ProdutoEdit;