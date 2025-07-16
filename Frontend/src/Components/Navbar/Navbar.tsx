import React, { useState, useEffect,useContext } from "react";
import { FaBars, FaUserCircle, FaChevronDown } from "react-icons/fa";
import { AuthContext } from "../Autenticacao/AuthContext";

interface NavbarProps {
    onMinimizeSidebar?: () => void;
    minimized?: boolean;
    fullWidth?: boolean;
}

const funcaoLabel = (funcao?: string) => {
    if (funcao === "G") return "Gerente";
    if (funcao === "C") return "Caixa";
    if (funcao === "V") return "Vendedor";
    return "";
};

const Navbar: React.FC<NavbarProps> = ({ onMinimizeSidebar, minimized, fullWidth }) => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const { user, isAuthenticated } = useContext(AuthContext);
    const [isMobile, setIsMobile] = useState(false);


    // Detecta se está em mobile
    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 768);
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    // Garante darkmode como padrão
    useEffect(() => {
        if (typeof window !== "undefined") {
            document.documentElement.classList.add("dark");
        }
    }, []);



    // Enquanto verifica autenticação, não renderiza nada
    if (isAuthenticated === null) {
        return <div>Carregando...</div>;
    }



    const sidebarOculta = isMobile && minimized && fullWidth;

    return (
        <nav
            className={
                sidebarOculta
                    ? "fixed top-0 left-0 w-full z-30 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 transition-colors"
                    : "fixed top-0 z-30 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 transition-colors"
            }
            style={
                sidebarOculta
                    ? { height: "48px", left: 0, width: "100%" }
                    : isMobile
                    ? { height: "48px", left: minimized ? "64px" : "0", width: minimized ? "calc(100% - 64px)" : "100%" }
                    : {
                          left: fullWidth ? 0 : minimized ? "80px" : "256px",
                          width: fullWidth ? "100%" : `calc(100% - ${minimized ? "80px" : "256px"})`,
                          height: "80px",
                      }
            }
        >
            <div className={sidebarOculta || isMobile ? "w-full h-full flex items-center justify-between px-3" : "h-full flex items-center justify-between px-8"}>
                <button
                    onClick={onMinimizeSidebar}
                    className="inline-flex md:hidden text-gray-900 dark:text-white bg-transparent border-0 cursor-pointer text-xl mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    aria-label={minimized ? "Expandir menu" : "Minimizar menu"}
                    tabIndex={0}
                >
                    <FaBars className="text-gray-900 dark:text-white" />
                </button>
                <div className={isMobile ? "font-bold text-base text-gray-900 dark:text-white" : "font-bold text-xl text-gray-900 dark:text-white"}>
                    Sis-Ótica
                </div>

                <div style={{ position: "relative" }}>
                    <button
                        onClick={() => setDropdownOpen((open) => !open)}
                        className={isMobile ? "flex items-center text-gray-900 dark:text-white bg-transparent border-0 cursor-pointer text-base rounded-none" : "flex items-center text-gray-900 dark:text-white bg-transparent border-0 cursor-pointer text-lg rounded-none"}
                    >
                        <FaUserCircle size={isMobile ? 24 : 28} className="text-gray-700 dark:text-white" />
                        <span className="ml-1 sm:ml-2 font-medium text-gray-900 dark:text-white xs:inline">
                            {user?.firstName}
                        </span>
                        {user?.funcao && (
                            <span className="ml-1 sm:ml-2 bg-cyan-600 text-white rounded-none px-1.5 py-0.5 text-[10px] sm:text-xs">
                                {funcaoLabel(user.funcao)}
                            </span>
                        )}
                        <FaChevronDown className="ml-1 sm:ml-2 text-gray-900 dark:text-white" />
                    </button>
                    {dropdownOpen && (
                        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-none shadow-lg text-gray-900 dark:text-white absolute right-0 mt-2 min-w-[140px] sm:min-w-[160px] z-40">
                            <a
                                href="/editar-perfil"
                                className="block px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-white text-xs sm:text-sm"
                            >
                                Editar Perfil
                            </a>
                            <div className="border-t border-gray-200 dark:border-gray-700" />
                            <a
                                href="/logoff"
                                className="block px-3 py-2 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 text-xs sm:text-sm"
                                onClick={() => {
                                    localStorage.removeItem("user_id");
                                    
                                }}
                            >
                                Sair
                            </a>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;