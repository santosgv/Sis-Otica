import React, { useState, useEffect } from "react"
import { AuthProvider } from "./Components/Autenticacao/AuthContext";
import { Routes, Route } from "react-router-dom"
import ProtectedRoute from './Components/ProtectedRoute';
import Unauthorized from "./Components/pages/Unauthorized";
import Sidebar from "./Components/Sidebar/Sidebar"
import Home from "./Components/Home/Home"
import Login from "./Components/Autenticacao/Login";
import Logoff from "./Components/Autenticacao/Logoff";
import Clientes from "./Components/Cliente/ClienteList"
import ClienteEdicao from "./Components/Cliente/ClienteEdit"
import ClienteCadastro from "./Components/Cliente/ClienteCadastro"
import ServicosCadastro from "./Components/Cliente/ServicosCadastro";
import LaboratorioCadastro from "./Components/Cliente/LaboratorioCadastro";
import NovaOrdem from "./Components/Os/NovaOrdem";
import Navbar from "./Components/Navbar/Navbar"
import Pesquisa from "./Components/Pesquisa/PesquisaList";
import PesquisaView from "./Components/Pesquisa/PesquisaView";
import Kanban from "./Components/Kanban/Kanban";
import Relatorios from "./Components/Relatorios/Relatorios";
import useIsKanbanRoute from "./hooks/useIsKanbanRoute";
import Estoque from "./Components/Estoque/Estoque";
import ProdutoEdit from "./Components/Estoque/ProdutoEdit";
import FornecedorList from "./Components/Estoque/FornecedorList";
import TipoList from "./Components/Estoque/TipoList";
import EstiloList from "./Components/Estoque/EstiloList";
import TipoUnitarioList from "./Components/Estoque/TipoUnitarioList";
import Caixa from "./Components/Caixa/CaixaList";
import VisualizarMesAnterior from "./Components/Caixa/VisualizarMesAnterior";
import AdicionarCaixa from "./Components/Caixa/AdicionarCaixa";
import { ThemeProvider } from "./ThemeContext/ThemeProvider";
import MinhasVendas from "./Components/MinhasVendas/MinhasVendas";
import FolhaPagamento from "./Components/FolhadePagamento/FolhaPagamento";
import RealizaPagamento from "./Components/RealizarPagamento/RealizaPagamento";
import ComissaoForm from "./Components/RealizarPagamento/ComissaoForm";
import ComissaoDetail from "./Components/RealizarPagamento/ComissaoDetail";
import ComissaoDelete from "./Components/RealizarPagamento/ComissaoDelete";
import EditaPerfil from "./Components/Autenticacao/EditaPerfil";
import { ToastProvider } from "./Components/ui/ToastContext";

const App: React.FC = () => {
  const [sidebarMinimized, setSidebarMinimized] = useState(false); // desktop
  const [sidebarMobileOpen, setSidebarMobileOpen] = useState(false); // mobile
  const isKanban = useIsKanbanRoute();

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setSidebarMinimized(false);
      }
    };
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Alterna menu lateral: mobile abre drawer, desktop minimiza
  const handleSidebarToggle = () => {
    if (window.innerWidth < 768) {
      setSidebarMobileOpen((prev) => !prev);
    } else {
      setSidebarMinimized((prev) => !prev);
    }
  };

  // Minimiza menu mobile ao clicar em item
  const handleSidebarMobileClose = () => setSidebarMobileOpen(false);

  return (
    <AuthProvider>
    <ThemeProvider>
      <ToastProvider>
        
        <Navbar
          onMinimizeSidebar={handleSidebarToggle}
          minimized={sidebarMinimized}
          fullWidth={sidebarMinimized && isKanban}
        />
        <div className={`flex min-h-screen ${sidebarMinimized && isKanban ? '' : (sidebarMinimized ? 'md:pl-20' : 'md:pl-64')} bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200`}
          style={{ overflowX: 'hidden' }}
        >
          {/* Sidebar desktop */}
          <div className="hidden md:block">
            <Sidebar minimized={sidebarMinimized} hideWhenMinimizedOnKanban={isKanban} />
          </div>
          {/* Sidebar mobile como drawer/overlay, apenas ícones */}
          {sidebarMobileOpen && (
            <div className="fixed inset-0 z-40 flex md:hidden">
              {/* Overlay escuro */}
              <div className="fixed inset-0 bg-black bg-opacity-40" onClick={handleSidebarMobileClose} aria-label="Fechar menu" />
              {/* Drawer lateral só com ícones */}
              <div className="relative w-16 max-w-full h-full bg-white dark:bg-gray-900 shadow-lg z-50 animate-slideInLeft flex flex-col">
                <Sidebar minimized={true} onItemClick={handleSidebarMobileClose} showCloseButton onClose={handleSidebarMobileClose} />
              </div>
            </div>
          )}
          <main
            className={
              `flex-1 flex flex-col w-full bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-200 transition-colors pt-12 sm:pt-20`
            }
            style={{ minHeight: '100vh', paddingBottom: 'env(safe-area-inset-bottom)' }}
          >
            {/* Rotas */}
            <Routes>
              <Route path="/" element={<ProtectedRoute allowedRoles={["G","V","C"]}><Home  /></ProtectedRoute>} />
              <Route path="/unauthorized" element={<Unauthorized /> } />
              <Route path="/login" element={<Login onLoginSuccess={() => {}} />} />
              <Route path='/editar-perfil' element={<ProtectedRoute allowedRoles={["G","V","C"]}><EditaPerfil /> </ProtectedRoute>} />
              <Route path='/logoff' element={<ProtectedRoute allowedRoles={["G","V","C"]}><Logoff /> </ProtectedRoute>} />
              <Route path="/clientes" element={<ProtectedRoute allowedRoles={["G","V","C"]}> <Clientes /> </ProtectedRoute>} />
              <Route path="/cliente" element={<ProtectedRoute allowedRoles={["G","V","C"]}> <ClienteEdicao /></ProtectedRoute>}></Route>
              <Route path="/cadastro-cliente" element={<ProtectedRoute allowedRoles={["G","V","C"]}> <ClienteCadastro /> </ProtectedRoute>} />
              <Route path="/pesquisa" element={<ProtectedRoute allowedRoles={["G","V","C"]}><Pesquisa /> </ProtectedRoute> } />
              <Route path="/cadastro-os" element={<ProtectedRoute allowedRoles={["G","V","C"]}><NovaOrdem /> </ProtectedRoute> } />
              <Route path="/servicos-cadastro" element={<ServicosCadastro />} />
              <Route path="/laboratorio-cadastro" element={<LaboratorioCadastro />} />
              <Route path="/os" element={<ProtectedRoute allowedRoles={["G","V","C"]}><PesquisaView /> </ProtectedRoute> } />
              <Route path="/kanban" element={<ProtectedRoute allowedRoles={["G","V","C"]}><Kanban /> </ProtectedRoute> } />
              <Route path="/relatorios" element={<ProtectedRoute allowedRoles={["G"]}><Relatorios /> </ProtectedRoute> } />
              <Route path="/estoque" element={<ProtectedRoute allowedRoles={["G"]}><Estoque /> </ProtectedRoute>  } />
              <Route path="/produtos/:id" element={ <ProtectedRoute allowedRoles={["G"]}> <ProdutoEdit /> </ProtectedRoute>  } />
              <Route path="/fornecedores" element={<ProtectedRoute allowedRoles={["G"]}><FornecedorList /> </ProtectedRoute> } />
              <Route path="/tipos" element={<ProtectedRoute allowedRoles={["G"]}><TipoList /> </ProtectedRoute>} />
              <Route path="/estilos" element={<ProtectedRoute allowedRoles={["G"]}><EstiloList /> </ProtectedRoute> } />
              <Route path="/tipos-unitarios" element={<ProtectedRoute allowedRoles={["G"]}><TipoUnitarioList /> </ProtectedRoute> } />
              <Route path="/caixa" element={ <ProtectedRoute allowedRoles={["G","C"]}> <Caixa /> </ProtectedRoute> } />
              <Route path="/caixa-mes" element={<ProtectedRoute allowedRoles={["G","C"]}><VisualizarMesAnterior /> </ProtectedRoute>} />
              <Route path="/caixa/adicionar" element={<ProtectedRoute allowedRoles={["G","C"]}> <AdicionarCaixa onClose={() => window.history.back()} /> </ProtectedRoute>  } />
              <Route path="/minhas-vendas" element={<ProtectedRoute allowedRoles={["G","V","C"]}><MinhasVendas /> </ProtectedRoute> } />
              <Route path="/folha-pagamento" element={<ProtectedRoute allowedRoles={["G"]}><FolhaPagamento /> </ProtectedRoute> } />
              <Route path="/realizar-pagamento" element={<ProtectedRoute allowedRoles={["G"]}><RealizaPagamento /> </ProtectedRoute>} />
              <Route path="/comissao/nova" element={<ProtectedRoute allowedRoles={["G"]}><ComissaoForm /> </ProtectedRoute> } />
              <Route path="/comissao/:id" element={<ProtectedRoute allowedRoles={["G"]}><ComissaoDetail /> </ProtectedRoute>} />
              <Route path="/comissao/:id/delete" element={<ProtectedRoute allowedRoles={["G"]}><ComissaoDelete /> </ProtectedRoute> } />
            </Routes>
          </main>
        </div>
      </ToastProvider>
    </ThemeProvider>
    </AuthProvider>
  );
};

export default App
