import React, { createContext, useState, useEffect, ReactNode } from "react";
import api from "../../utils/axiosConfig";
import useAuth from "../../hooks/useAuth";

interface User {
    firstName: string;
    funcao: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean | null;
    setAuthData: (userId: string | null) => void;

}

export const AuthContext = createContext<AuthContextType>({
    user: null,
    isAuthenticated: null,
    setAuthData: () => {}
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const { userId, loading: authLoading } = useAuth();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    const fetchUserData = (userId: string) => {
        api
            .get(`/usuarios/${userId}/`)
            
            .then((response) => {
                
                setUser({
                    firstName: response.data.first_name || "Usuário",
                    funcao: response.data.FUNCAO || "",
                });
                setIsAuthenticated(true);
            })
            .catch((error) => {
                console.error("[AuthProvider] Erro ao buscar dados do usuário:", error);
                setUser(null);
                setIsAuthenticated(false);

            });
    };

    // Função para configurar os dados de autenticação
    const setAuthData = (userId: string | null) => {
       
        if (userId) {
            localStorage.setItem("user_id", userId);
            fetchUserData(userId);
        }
    };

    // Verifica autenticação inicial
    useEffect(() => {
        const userId = localStorage.getItem("user_id");
        

        if (userId) {
            fetchUserData(userId);
        } else {
            setIsAuthenticated(false);
        }
    }, [isAuthenticated, userId]);

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, setAuthData,  }}>
            {children}
        </AuthContext.Provider>
    );
};