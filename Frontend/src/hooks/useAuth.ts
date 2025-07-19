import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { getAccessToken, clearTokens } from '../utils/auth';

// Tipo para o payload do token JWT
interface JwtPayload {
  exp: number;
  user_id?: number | string;
  tipo_plano?: 'free' | 'premium';
  [key: string]: any; // permite campos extras
}

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<JwtPayload | null>(null);
  const [userId, setUserId] = useState<number | string | null>(null);
  const [tipoPlano, setTipoPlano] = useState<'free' | 'premium' | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      setIsAuthenticated(false);
      setUser(null);
      setUserId(null);
      setTipoPlano(null);
      setLoading(false);
      return;
    }

    try {
      const decoded = jwtDecode<JwtPayload>(token);
      const now = Date.now() / 1000;

      if (decoded.exp > now) {
        setIsAuthenticated(true);
        setUser(decoded);
        const id = decoded.user_id ?? null;
        setUserId(id);
        setTipoPlano(decoded.tipo_plano ?? null);
        console.log('AuthProvider tipoPlano:', tipoPlano);
        if (id !== null) {
          localStorage.setItem('user_id', id.toString());
        }
      } else {
        clearTokens();
        localStorage.removeItem('user_id');
        setIsAuthenticated(false);
        setUser(null);
        setTipoPlano(null);
        setUserId(null);
      }
    } catch (err) {
      console.error('Error decoding JWT:', err);
      clearTokens();
      localStorage.removeItem('user_id');
      setIsAuthenticated(false);
      setUser(null);
      setTipoPlano(null);
      setUserId(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = () => {
    clearTokens();
    localStorage.removeItem('user_id');
    setIsAuthenticated(false);
    setUser(null);
    setTipoPlano(null);
    setUserId(null);
  };

  return { isAuthenticated, user, userId, logout,tipoPlano, loading };
};

export default useAuth;
