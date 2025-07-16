import React, { useState, useContext, useEffect, useRef } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import type { DropResult } from "@hello-pangea/dnd";
import { motion } from "framer-motion";
import { ThemeContext } from "../../ThemeContext/themecontext";
import { Link } from "react-router-dom";
import api from "../../utils/axiosConfig"


// Status do Kanban
const KANBAN_STATUS = [
  { key: "A", label: "SOLICITADO" },
  { key: "L", label: "LABORATÓRIO" },
  { key: "J", label: "LOJA" },
  { key: "E", label: "ENTREGUE" },
];

// Interface da ordem
interface Ordem {
  id: number;
  status: string;
  cliente: string;
  servico: string;
  vendedor: string;
  lentes: string;
  dataPedido: string;
  observacao: string;
  previsaoEntrega: string;
}

const Kanban: React.FC = () => {
  const [ordens, setOrdens] = useState<Ordem[]>([]);
  const [clientesMap, setClientesMap] = useState<Record<string, string>>({});
  const [usuariosMap, setUsuariosMap] = useState<Record<string, string>>({});
  const { theme } = useContext(ThemeContext);
  const boardRef = useRef<HTMLDivElement>(null);
  const columnRefs = useRef<(HTMLDivElement | null)[]>([]);
  const [boardMinHeight, setBoardMinHeight] = useState<number | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  // Carrega dados auxiliares (clientes, usuários/vendedores)
  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const response = await api.get("/clientes/");
        const lista = Array.isArray(response.data) ? response.data : response.data.results || [];
        const map: Record<string, string> = {};
        lista.forEach((c: { id: number; nome?: string; NOME?: string; razao_social?: string; RAZAO_SOCIAL?: string }) => {
          map[String(c.id)] = c.nome || c.NOME || c.razao_social || c.RAZAO_SOCIAL || String(c.id);
        });
        setClientesMap(map);
      } catch (err) {
        console.error("Erro ao carregar clientes:", err);
        setError("Erro ao carregar clientes. Tente novamente.");
      }
    };

    const fetchUsuarios = async () => {
      try {
        const response = await api.get("/usuarios/");
        const lista = Array.isArray(response.data) ? response.data : response.data.results || [];
        const map: Record<string, string> = {};
        lista.forEach((u: { id: number; nome?: string; NOME?: string; username?: string }) => {
          map[String(u.id)] = u.nome || u.NOME || u.username || String(u.id);
        });
        setUsuariosMap(map);
      } catch (err) {
        console.error("Erro ao carregar usuários:", err);
        setError("Erro ao carregar usuários. Tente novamente.");
      }
    };

    fetchClientes();
    fetchUsuarios();
  }, []);

  // Carrega ordens da API
  useEffect(() => {
    const fetchOrdens = async () => {
      try {
        const response = await api.get("/kanban/");
        const data = response.data;
        const statusMap = {
          solicitado: "A",
          laboratorio: "L",
          loja: "J",
          entregue: "E",
        };
        let ordens: Ordem[] = [];
        Object.entries(statusMap).forEach(([apiKey, statusKey]) => {
          if (data[apiKey]) {
            ordens = ordens.concat(
              data[apiKey].map((item: Record<string, unknown>) => ({
                id: Number(item.id),
                status: String(item.STATUS || statusKey),
                cliente: String(item.CLIENTE ?? ""),
                vendedor: String(item.VENDEDOR ?? ""),
                lentes: String(item.LENTES ?? ""),
                dataPedido: String(item.DATA_SOLICITACAO || ""),
                observacao: String(item.OBSERVACAO || ""),
                previsaoEntrega: String(item.PREVISAO_ENTREGA || ""),
              }))
            );
          }
        });
        setOrdens(ordens);
      } catch (err) {
        console.error("Erro ao carregar ordens:", err);
        setError("Não foi possível carregar as ordens. Tente novamente.");
      }
    };

    fetchOrdens();
  }, []);

  // Atualiza a altura do board
  useEffect(() => {
    if (columnRefs.current.length > 0) {
      const max = Math.max(...columnRefs.current.map((col) => (col ? col.offsetHeight : 0)), 0);
      setBoardMinHeight(max);
    }
  }, [ordens]);

  // Função de drag and drop
  const onDragEnd = async (result: DropResult) => {
    const { source, destination } = result;
    if (!destination) return;
    if (source.droppableId === destination.droppableId && source.index === destination.index) return;

    const ordensByStatus = KANBAN_STATUS.reduce((acc, s) => {
      acc[s.key] = ordens.filter((o) => o.status === s.key);
      return acc;
    }, {} as Record<string, Ordem[]>);

    const sourceStatus = KANBAN_STATUS[Number(source.droppableId)].key;
    const destStatus = KANBAN_STATUS[Number(destination.droppableId)].key;
    const sourceList = Array.from(ordensByStatus[sourceStatus]);
    const destList = Array.from(ordensByStatus[destStatus]);

    const [movedOrder] = sourceList.splice(source.index, 1);
    movedOrder.status = destStatus;
    destList.splice(destination.index, 0, movedOrder);

    ordensByStatus[sourceStatus] = sourceList;
    ordensByStatus[destStatus] = destList;

    const newOrdens = KANBAN_STATUS.flatMap((s) => ordensByStatus[s.key]);
    setOrdens(newOrdens); // Atualiza localmente primeiro para melhor UX

    try {
      await api.post(`/cards/${movedOrder.id}/update-status/`, { status: destStatus });
    } catch (err) {
      console.error("Erro ao atualizar status:", err);
      alert("Erro ao atualizar status no servidor. O card será revertido.");
      setOrdens(ordens); // Reverte em caso de erro
    }
  };

  function getNomeCliente(id: string) {
    return clientesMap[id] || id;
  }

  function getNomeVendedor(id: string) {
    return usuariosMap[id] || id;
  }

  const ordensByStatus = KANBAN_STATUS.reduce((acc, s) => {
    acc[s.key] = ordens.filter((o) => o.status === s.key);
    return acc;
  }, {} as Record<string, Ordem[]>);

  return (
    <section className="w-full min-h-[94vh] py-6 bg-white dark:bg-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4">
        <div className="sticky top-20 left-0 w-full z-10 bg-white dark:bg-gray-900">
          <h3 className="text-center text-lg md:text-2xl font-bold mb-4 md:mb-6 text-gray-900 dark:text-gray-100">
            Kanban - Últimos 10 Dias
          </h3>
          {error && (
            <div className="bg-red-100 text-red-800 p-4 rounded-lg dark:bg-red-900 dark:text-red-100 mb-4">
              {error}
            </div>
          )}
        </div>
        <DragDropContext onDragEnd={onDragEnd}>
          <div
            className="kanban-board grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 2xl:grid-cols-4 gap-6 pb-2 min-w-0 w-full mx-auto items-start overflow-x-auto"
            ref={boardRef}
            style={boardMinHeight ? { minHeight: boardMinHeight } : {}}
          >
            {KANBAN_STATUS.map((col, index) => (
              <Droppable droppableId={index.toString()} key={col.key}>
                {(provided) => (
                  <div
                    ref={(el) => {
                      provided.innerRef(el);
                      columnRefs.current[index] = el;
                    }}
                    {...provided.droppableProps}
                    className="kanban-column relative w-full bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md p-4 flex-shrink-0 h-auto z-10 max-h-[calc(100vh-180px)] overflow-y-auto"
                  >
                    <h6 className="text-center font-semibold text-base xl:text-lg mb-2 text-black-600 dark:text-black-400 sticky top-0 bg-gray-100 dark:bg-gray-800 z-20 pb-2">
                      {col.label}
                    </h6>
                    <div className="flex flex-col gap-3 items-center">
                      {ordensByStatus[col.key]?.map((os, idx) => (
                        <Draggable key={os.id} draggableId={os.id.toString()} index={idx}>
                          {(provided) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              className="w-full"
                            >
                              <motion.div
                                className="kanban-card w-full max-w-[420px] bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-md p-3 mb-0 shadow-md hover:shadow-lg transition-shadow duration-200 text-sm xl:text-base mx-auto"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                              >
                                <Link to={`/os?id=${os.id}`} className="block">
                                  <div className="font-bold text-blue-600 dark:text-blue-400 mb-1 text-base">
                                    OS #{os.id}
                                  </div>
                                  </Link>
                                  <div {...provided.dragHandleProps}
                                  className=" cursor-move">
                                  <div>
                                    <b className="text-gray-700 dark:text-white">Cliente:</b>{" "}
                                    <span className="dark:text-white">{getNomeCliente(os.cliente)}</span>
                                  </div>
                                  <div>
                                    <b className="text-gray-700 dark:text-white">Vendedor:</b>{" "}
                                    <span className="dark:text-white">{getNomeVendedor(os.vendedor)}</span>
                                  </div>
                                  <div>
                                    <b className="text-gray-700 dark:text-white">Lentes:</b>{" "}
                                    <span className="dark:text-white">{os.lentes}</span>
                                  </div>
                                  <div>
                                    <b className="text-gray-700 dark:text-white">Data Pedido:</b>{" "}
                                    <span className="dark:text-white">{os.dataPedido}</span>
                                  </div>
                                  <div>
                                    <b className="text-gray-700 dark:text-white">Previsão Entrega:</b>{" "}
                                    <span className="dark:text-white">{os.previsaoEntrega}</span>
                                  </div>
                                
                                <div
                                
                                >
                                  <span className="text-gray-700 dark:text-white">
                                    <b>Obs:</b> <span className="dark:text-white">{os.observacao}</span>
                                  </span>
                                </div>
                                </div>
                              </motion.div>
                            </div>
                          )}
                        </Draggable>
                      ))}
                    </div>
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            ))}
          </div>
        </DragDropContext>
      </div>
    </section>
  );
};

export default Kanban;