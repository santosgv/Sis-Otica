import { useState, useEffect } from "react";
import api from "../../../utils/axiosConfig";

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

  const [ordensPagina, setOrdensPagina] = useState<Ordem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [clientesMap, setClientesMap] = useState<Record<number, string>>({});
  const [clientesTelefoneMap, setClientesTelefoneMap] = useState<Record<number, string>>({});
  const [vendedoresMap, setVendedoresMap] = useState<Record<number, string>>({});
  const [servicosMap, setServicosMap] = useState<Record<number, string>>({});
  const [searchCliente, setSearchCliente] = useState("");
  const [searchOS, setSearchOS] = useState("");
  const [status, setStatus] = useState("");
  const [dataInicio, setDataInicio] = useState("");
  const [dataFim, setDataFim] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(PAGE_SIZE_OPTIONS[0]);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    setLoading(true);
    setError(null);

    const params = {
      page: currentPage,
      page_size: pageSize,
    };

    Promise.all([
      api.get("/ordens/", { params }),
      api.get("/clientes/"),
      api.get("/usuarios/"),
      api.get("/servicos/"),
    ])
      .then(([ordensRes, clientesRes, usuariosRes, servicosRes]) => {
        interface Cliente {
          id: number;
          NOME?: string;
          TELEFONE: string;
        }

        const clientesArr = Array.isArray(clientesRes.data.results)
          ? (clientesRes.data.results as Cliente[])
          : [];

        const localClientesMap: Record<number, string> = {};
        const localClientesTelefoneMap: Record<number, string> = {};

        clientesArr.forEach((c: Cliente) => {
          localClientesMap[c.id] = c.NOME ?? c.TELEFONE ?? "";
          localClientesTelefoneMap[c.id] = c.TELEFONE ?? "";
        });

        setClientesMap(localClientesMap);
        setClientesTelefoneMap(localClientesTelefoneMap);

        interface Usuario {
          id: number;
          username?: string;
          first_name?: string;
        }

        const usuariosArr = Array.isArray(usuariosRes.data.results)
          ? (usuariosRes.data.results as Usuario[])
          : [];

        const localVendedoresMap: Record<number, string> = {};
        usuariosArr.forEach((u: Usuario) => {
          localVendedoresMap[Number(u.id)] = u.first_name ?? u.username ?? "";
        });
        setVendedoresMap(localVendedoresMap);

        interface Servico {
          id: number;
          SERVICO?: string;
        }

        const servicosArr = Array.isArray(servicosRes.data.results)
          ? (servicosRes.data.results as Servico[])
          : [];

        const localServicosMap: Record<number, string> = {};
        servicosArr.forEach((s: Servico) => {
          localServicosMap[s.id] = s.SERVICO ?? "";
        });
        setServicosMap(localServicosMap);

        const results = Array.isArray(ordensRes.data.results)
          ? ordensRes.data.results
          : [];

        const mapped = results.map((item: Record<string, any>) => ({
          id: item.id,
          servico: item.SERVICO ?? "",
          cliente: item.CLIENTE ?? "",
          vendedor: item.VENDEDOR ?? "",
          lentes: item.LENTES ?? "",
          dataPedido: item.DATA_SOLICITACAO ?? "",
          status: item.STATUS ?? "",
          telefone: localClientesTelefoneMap[Number(item.CLIENTE)] ?? "",
          previsaoEntrega: item.PREVISAO_ENTREGA ?? "",
        }));

        setOrdensPagina(mapped);
        setTotalCount(ordensRes.data.count || 0);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao buscar dados da API");
        setLoading(false);
      });
  }, [currentPage, pageSize]);

  // Filtros apenas na página atual
  const filtered = ordensPagina.filter((os) => {
    const clienteNome = clientesMap[Number(os.cliente)]?.toLowerCase() ?? "";
    return (
      (searchCliente === "" || clienteNome.includes(searchCliente.toLowerCase())) &&
      (searchOS === "" || os.id.toString().includes(searchOS)) &&
      (status === "" || os.status === status) &&
      (dataInicio === "" || os.dataPedido >= dataInicio) &&
      (dataFim === "" || os.dataPedido <= dataFim)
    );
  });

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));

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
    paginated: filtered, // dados filtrados apenas da página atual
    filtered, // alias, se você usa em outro lugar
  };
}
