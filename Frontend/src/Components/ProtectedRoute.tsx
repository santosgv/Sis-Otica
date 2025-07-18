// src/components/ProtectedRoute.tsx
import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "./Autenticacao/AuthContext";  // ajuste o caminho conforme necessário

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles: string[]; // exemplo: ["G", "C"]
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { isAuthenticated, user } = useContext(AuthContext);

  if (isAuthenticated === null) {
    return <p>Carregando...</p>; // loading placeholder
  }

  if (!isAuthenticated || !user || !allowedRoles.includes(user.funcao)) {
    return <Navigate to="/unauthorized" />;
  }

  return children;
};

export default ProtectedRoute;
