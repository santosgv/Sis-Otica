// src/components/ProtectedRoute.tsx
import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "./Autenticacao/AuthContext";  // ajuste o caminho conforme necessário

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: string[]; // exemplo: ["G", "C"]
  requiredPlan?: 'free' | 'premium';
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles,requiredPlan }) => {
  const { isAuthenticated, user,tipoPlano } = useContext(AuthContext);

  if (isAuthenticated === null) {
    return <p>Carregando...</p>; // loading placeholder
  }

  if (!isAuthenticated || !user || !allowedRoles.includes(user.funcao)) {
    return <Navigate to="/unauthorized" />;
  }

  if (requiredPlan && tipoPlano !== requiredPlan) {
    return <p className="relative bg-white dark:bg-gray-900 py-8 px-4 flex flex-col items-center transition-colors duration-300 text-center">Nao Liberado para o plano gratuito...</p>;
  }

  return children;
};

export default ProtectedRoute;
