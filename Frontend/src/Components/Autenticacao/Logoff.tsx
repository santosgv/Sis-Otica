import { useNavigate } from 'react-router-dom';
import { useEffect } from "react";
import useAuth from '../../hooks/useAuth.js';


const Logoff = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {

    logout(); // Executa a função de logout
    window.location.assign("/login");
  }, [logout, navigate]);

  return null; // Não renderiza nada
};

export default Logoff;