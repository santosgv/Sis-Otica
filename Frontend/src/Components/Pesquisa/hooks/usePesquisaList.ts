import { useState, useEffect } from "react";
import api from "../../../utils/axiosConfig"


const PAGE_SIZE_OPTIONS = [25, 50, 100];

export function usePesquisaList() {
  interface Ordem {
    id: number;
    servico: string | number;
    cliente: string | number;
    vendedor: string | number;
    lentes: string;
    dataPedido: string;
    status: string;
    telefone: string;
    previsaoEntrega: string;
  }
  const [ordens, setOrdens] = useState<Ordem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [clientesMap, setClientesMap] = useState<Record<number, string>>({});
  const [clientesTelefoneMap, setClientesTelefoneMap] = useState<Record<number, string>>({});
  const [vendedoresMap, setVendedoresMap] = useState<Record<number, string>>(
    {}
  );
  const [servicosMap, setServicosMap] = useState<Record<number, string>>({});
  const [searchCliente, setSearchCliente] = useState("");
  const [searchOS, setSearchOS] = useState("");
  const [status, setStatus] = useState("");
  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZE_OPTIONS[0]);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      api.get("http://localhost:8000/api/v1/ordens/"),
      api.get("http://localhost:8000/api/v1/clientes/"),
      api.get("http://localhost:8000/api/v1/usuarios/"),
      api.get("http://localhost:8000/api/v1/servicos/"),
    ])
      .then(([ordensRes, clientesRes, usuariosRes, servicosRes]) => {
        // ...mapeamento igual ao componente original...
        interface Cliente {
          id: number;
          NOME?: string;
          TELEFONE: string;
        }
        const clientesArr = Array.isArray(clientesRes.data.results)
          ? (clientesRes.data.results as Cliente[])
          : [];
        const clientesMap: Record<number, string> = {};
        const clientesTelefoneMap: Record<number, string> = {}; // Novo mapeamento
                clientesArr.forEach((c: Cliente) => {
                  clientesMap[c.id] = c.NOME ?? c.TELEFONE ?? "";
                  clientesTelefoneMap[c.id] = c.TELEFONE ?? ""; // Mapeia o telefone
                });
                setClientesMap(clientesMap);
                setClientesTelefoneMap(clientesTelefoneMap);

        interface Usuario {
          id: number;
          username?: string;
          first_name?: string;
          FUNCAO?: string;
        }
        const usuariosArr = Array.isArray(usuariosRes.data.results)
          ? (usuariosRes.data.results as Usuario[])
          : [];
        const vendedoresMap: Record<number, string> = {};
        usuariosArr.forEach((u: Usuario) => {
          vendedoresMap[Number(u.id)] = u.first_name ?? u.username ?? "";
        });
        setVendedoresMap(vendedoresMap);

        interface Servico {
          id: number;
          SERVICO?: string;
        }
        const servicosArr = Array.isArray(servicosRes.data.results)
          ? (servicosRes.data.results as Servico[])
          : [];
        const servicosMap: Record<number, string> = {};
        servicosArr.forEach((s: Servico) => {
          servicosMap[s.id] = s.SERVICO ?? "";
        });
        setServicosMap(servicosMap);

        const results = Array.isArray(ordensRes.data.results)
          ? ordensRes.data.results
          : [];
        const mapped = results.map((item: Record<string, unknown>) => ({
          id: item.id as number,
          servico: (item.SERVICO ?? "") as string | number,
          cliente: (item.CLIENTE ?? "") as string | number,
          vendedor: (item.VENDEDOR ?? "") as string | number,
          lentes: (item.LENTES ?? "") as string,
          dataPedido: (item.DATA_SOLICITACAO ?? "") as string,
          status: (item.STATUS ?? "") as string,
          telefone: clientesTelefoneMap[Number(item.CLIENTE)] ?? "",
          previsaoEntrega: (item.PREVISAO_ENTREGA ?? "") as string,
        }));
        setOrdens(mapped);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao buscar dados da API");
        setLoading(false);
      });
  }, []);

  // Filtro
  const filtered = ordens.filter(
    (os) =>
      (searchCliente === "" ||
        (clientesMap[Number(os.cliente)] &&
          clientesMap[Number(os.cliente)]
            .toLowerCase()
            .includes(searchCliente.toLowerCase()))) &&
      (searchOS === "" || os.id?.toString().includes(searchOS)) &&
      (status === "" || os.status === status) &&
      (dataInicio === "" || os.dataPedido >= dataInicio) &&
      (dataFim === "" || os.dataPedido <= dataFim)
  );

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const paginated = filtered.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  return {
    loading,
    error,
    clientesMap,
    vendedoresMap,
    servicosMap,
    searchCliente,
    setSearchCliente,
    searchOS,
    setSearchOS,
    status,
    setStatus,
    dataInicio,
    setDataInicio,
    dataFim,
    setDataFim,
    currentPage,
    setCurrentPage,
    pageSize,
    setPageSize,
    PAGE_SIZE_OPTIONS,
    totalPages,
    paginated,
    filtered,
  };
}
