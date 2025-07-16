import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import api from "../../utils/axiosConfig"

interface FormData {
  nome: string;
  email: string;
  telefone: string;
  cpf: string;
  dataNascimento: string;
  cep: string;
  logradouro: string;
  numero: string;
  bairro: string;
  cidade: string;
}

interface Errors {
  nome?: string;
  email?: string;
  telefone?: string;
  cpf?: string;
  dataNascimento?: string;
  cep?: string;
  logradouro?: string;
  numero?: string;
  bairro?: string;
  cidade?: string;
}

const ClienteCadastro: React.FC = () => {
  const [form, setForm] = useState<FormData>({
    nome: "",
    email: "",
    telefone: "",
    cpf: "",
    dataNascimento: "",
    cep: "",
    logradouro: "",
    numero: "",
    bairro: "",
    cidade: "",
  });
  const [errors, setErrors] = useState<Errors>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Função para consultar o ViaCEP
  const handleCepBlur = async () => {
    const cepRegex = /^\d{5}-\d{3}$/;
    if (!form.cep || !cepRegex.test(form.cep)) {
      setErrors((prev) => ({ ...prev, cep: "CEP deve seguir o formato XXXXX-XXX" }));
      return;
    }

    try {
      const response = await axios.get(`https://viacep.com.br/ws/${form.cep.replace(/\D/g, "")}/json/`);
      if (response.data.erro) {
        setErrors((prev) => ({ ...prev, cep: "CEP não encontrado" }));
        return;
      }

      setForm((prev) => ({
        ...prev,
        logradouro: response.data.logradouro || prev.logradouro,
        bairro: response.data.bairro || prev.bairro,
        cidade: response.data.localidade || prev.cidade,
      }));
      setErrors((prev) => ({ ...prev, cep: undefined, logradouro: undefined, bairro: undefined, cidade: undefined }));
    } catch (error) {
      console.error("Erro ao consultar ViaCEP:", error);
      setErrors((prev) => ({ ...prev, cep: "Erro ao consultar CEP. Verifique e tente novamente." }));
    }
  };

  // Funções de validação
  const validateForm = () => {
    const newErrors: Errors = {};

    // Nome: limite de 100 caracteres
    if (!form.nome) {
      newErrors.nome = "Nome é obrigatório";
    } else if (form.nome.length > 100) {
      newErrors.nome = "Nome deve ter no máximo 100 caracteres";
    }

    // Email: validação de formato e limite de 255 caracteres
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!form.email) {
      newErrors.email = "Email é obrigatório";
    } else if (!emailRegex.test(form.email)) {
      newErrors.email = "Email inválido";
    } else if (form.email.length > 255) {
      newErrors.email = "Email deve ter no máximo 255 caracteres";
    }

    // Telefone: formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX, limite de 15 caracteres
    const telefoneRegex = /^\(\d{2}\)\s?\d{4,5}-\d{4}$/;
    if (!form.telefone) {
      newErrors.telefone = "Telefone é obrigatório";
    } else if (!telefoneRegex.test(form.telefone)) {
      newErrors.telefone = "Telefone deve seguir o formato (XX) XXXXX-XXXX";
    } else if (form.telefone.length > 15) {
      newErrors.telefone = "Telefone deve ter no máximo 15 caracteres";
    }

    // CPF: formato XXX.XXX.XXX-XX, limite de 14 caracteres
    const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/;
    if (!form.cpf) {
      newErrors.cpf = "CPF é obrigatório";
    } else if (!cpfRegex.test(form.cpf)) {
      newErrors.cpf = "CPF deve seguir o formato XXX.XXX.XXX-XX";
    } else if (form.cpf.length > 14) {
      newErrors.cpf = "CPF deve ter no máximo 14 caracteres";
    }

    // Data de Nascimento: obrigatória e no formato AAAA-MM-DD
    if (!form.dataNascimento) {
      newErrors.dataNascimento = "Data de nascimento é obrigatória";
    } else {
      const date = new Date(form.dataNascimento);
      if (isNaN(date.getTime()) || date > new Date()) {
        newErrors.dataNascimento = "Data de nascimento inválida ou futura";
      }
    }

    // CEP: formato XXXXX-XXX, limite de 9 caracteres
    const cepRegex = /^\d{5}-\d{3}$/;
    if (!form.cep) {
      newErrors.cep = "CEP é obrigatório";
    } else if (!cepRegex.test(form.cep)) {
      newErrors.cep = "CEP deve seguir o formato XXXXX-XXX";
    } else if (form.cep.length > 9) {
      newErrors.cep = "CEP deve ter no máximo 9 caracteres";
    }

    // Logradouro: limite de 200 caracteres
    if (!form.logradouro) {
      newErrors.logradouro = "Logradouro é obrigatório";
    } else if (form.logradouro.length > 200) {
      newErrors.logradouro = "Logradouro deve ter no máximo 200 caracteres";
    }

    // Número: limite de 10 caracteres
    if (!form.numero) {
      newErrors.numero = "Número é obrigatório";
    } else if (form.numero.length > 10) {
      newErrors.numero = "Número deve ter no máximo 10 caracteres";
    }

    // Bairro: limite de 100 caracteres
    if (!form.bairro) {
      newErrors.bairro = "Bairro é obrigatório";
    } else if (form.bairro.length > 100) {
      newErrors.bairro = "Bairro deve ter no máximo 100 caracteres";
    }

    // Cidade: limite de 100 caracteres
    if (!form.cidade) {
      newErrors.cidade = "Cidade é obrigatória";
    } else if (form.cidade.length > 100) {
      newErrors.cidade = "Cidade deve ter no máximo 100 caracteres";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Máscaras para entrada
  const applyMask = (name: string, value: string) => {
    let maskedValue = value;

    if (name === "telefone") {
      maskedValue = value
        .replace(/\D/g, "")
        .replace(/(\d{2})(\d)/, "($1) $2")
        .replace(/(\d{4,5})(\d{4})$/, "$1-$2")
        .slice(0, 15);
    } else if (name === "cpf") {
      maskedValue = value
        .replace(/\D/g, "")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d)/, "$1.$2")
        .replace(/(\d{3})(\d{2})$/, "$1-$2")
        .slice(0, 14);
    } else if (name === "cep") {
      maskedValue = value
        .replace(/\D/g, "")
        .replace(/(\d{5})(\d)/, "$1-$2")
        .slice(0, 9);
    }

    return maskedValue;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const maskedValue = ["telefone", "cpf", "cep"].includes(name)
      ? applyMask(name, value)
      : value;

    setForm({ ...form, [name]: maskedValue });
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setSubmitError(null);

    // Remove caracteres de formatação para a API
    const cleanPayload = {
      NOME: form.nome,
      LOGRADOURO: form.logradouro,
      CEP: form.cep.replace(/\D/g, ""), // Apenas números
      NUMERO: form.numero,
      BAIRRO: form.bairro,
      CIDADE: form.cidade,
      TELEFONE: form.telefone.replace(/\D/g, ""), // Apenas números
      CPF: form.cpf.replace(/\D/g, ""), // Apenas números
      DATA_NASCIMENTO: form.dataNascimento.split("T")[0], // Garante apenas YYYY-MM-DD
      EMAIL: form.email,
      STATUS: 1, // Valor fixo conforme o exemplo
    };

    try {
      await api.post("/clientes/", cleanPayload);
      alert("Cliente cadastrado com sucesso!");
      navigate("/clientes");
    } catch (error) {
      console.error("Erro ao cadastrar cliente:", error);
      setSubmitError("Erro ao cadastrar cliente. Verifique os dados e tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="w-full h-full min-h-[calc(100vh-80px)] flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors px-2 sm:px-4">
      <form
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 shadow-lg rounded-xl py-6 px-2 sm:py-8 sm:px-4 md:px-8 w-full mx-auto space-y-6 text-gray-900 dark:text-white mt-4 sm:mt-8"
        autoComplete="off"
      >
        <h2 className="text-xl sm:text-2xl font-bold mb-2 sm:mb-4 text-gray-900 dark:text-white text-left">
          Cadastro de Cliente
        </h2>

        {/* Mensagem de erro geral */}
        {submitError && (
          <div className="bg-red-100 text-red-800 p-4 rounded-lg dark:bg-red-900 dark:text-red-100">
            {submitError}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 w-full">
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="nome">
              Nome
            </label>
            <input
              type="text"
              id="nome"
              name="nome"
              value={form.nome}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.nome ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Ex: João"
              required
              maxLength={100}
            />
            {errors.nome && <p className="text-red-500 text-sm mt-1">{errors.nome}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.email ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Email"
              required
              maxLength={255}
            />
            {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="telefone">
              Telefone
            </label>
            <input
              type="text"
              id="telefone"
              name="telefone"
              value={form.telefone}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.telefone ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="(XX) XXXXX-XXXX"
              required
              maxLength={15}
            />
            {errors.telefone && <p className="text-red-500 text-sm mt-1">{errors.telefone}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="cpf">
              CPF
            </label>
            <input
              type="text"
              id="cpf"
              name="cpf"
              value={form.cpf}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.cpf ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="000.000.000-00"
              required
              maxLength={14}
            />
            {errors.cpf && <p className="text-red-500 text-sm mt-1">{errors.cpf}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="dataNascimento">
              Data Nascimento
            </label>
            <input
              type="date"
              id="dataNascimento"
              name="dataNascimento"
              value={form.dataNascimento}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.dataNascimento ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              required
            />
            {errors.dataNascimento && (
              <p className="text-red-500 text-sm mt-1">{errors.dataNascimento}</p>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="cep">
              CEP
            </label>
            <input
              type="text"
              id="cep"
              name="cep"
              value={form.cep}
              onChange={handleChange}
              onBlur={handleCepBlur} // Adiciona o evento onBlur para consultar o ViaCEP
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.cep ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="XXXXX-XXX"
              required
              maxLength={9}
            />
            {errors.cep && <p className="text-red-500 text-sm mt-1">{errors.cep}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="logradouro">
              Logradouro
            </label>
            <input
              type="text"
              id="logradouro"
              name="logradouro"
              value={form.logradouro}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.logradouro ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Rua"
              required
              maxLength={200}
            />
            {errors.logradouro && <p className="text-red-500 text-sm mt-1">{errors.logradouro}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="numero">
              Número
            </label>
            <input
              type="text"
              id="numero"
              name="numero"
              value={form.numero}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.numero ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Número"
              required
              maxLength={10}
            />
            {errors.numero && <p className="text-red-500 text-sm mt-1">{errors.numero}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="bairro">
              Bairro
            </label>
            <input
              type="text"
              id="bairro"
              name="bairro"
              value={form.bairro}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.bairro ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Bairro"
              required
              maxLength={100}
            />
            {errors.bairro && <p className="text-red-500 text-sm mt-1">{errors.bairro}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700 dark:text-white" htmlFor="cidade">
              Cidade
            </label>
            <input
              type="text"
              id="cidade"
              name="cidade"
              value={form.cidade}
              onChange={handleChange}
              className={`w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-900 text-gray-900 dark:text-white ${
                errors.cidade ? "border-red-500" : "border-gray-300 dark:border-gray-700"
              }`}
              placeholder="Cidade"
              required
              maxLength={100}
            />
            {errors.cidade && <p className="text-red-500 text-sm mt-1">{errors.cidade}</p>}
          </div>
        </div>
        <div className="flex flex-col sm:flex-row justify-start gap-3 sm:gap-4 mt-4 sm:mt-6">
          <button
            type="submit"
            className={`px-4 sm:px-6 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition w-full sm:w-auto ${
              loading ? "opacity-50 cursor-not-allowed" : ""
            }`}
            disabled={loading}
          >
            {loading ? "Cadastrando..." : "Cadastrar"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/clientes")}
            className="px-4 sm:px-6 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition w-full sm:w-auto"
            disabled={loading}
          >
            Cancelar
          </button>
        </div>
      </form>
    </section>
  );
};

export default ClienteCadastro;