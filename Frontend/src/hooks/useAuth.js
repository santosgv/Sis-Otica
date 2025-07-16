import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { getAccessToken, clearTokens } from '../utils/auth';

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      setIsAuthenticated(false);
      setUser(null);
      setUserId(null);
      setLoading(false);
      return;
    }

    try {
      const decoded = jwtDecode(token);
      const now = Date.now() / 1000;

      if (decoded.exp > now) {
        setIsAuthenticated(true);
        setUser(decoded);
        // Extract user_id
        const id = decoded.user_id || null;
        setUserId(id);
        // Store in localStorage
        if (id !== null) {
          localStorage.setItem('user_id', id.toString());
        }
      } else {
        clearTokens();
        localStorage.removeItem('user_id');
        setIsAuthenticated(false);
        setUser(null);
        setUserId(null);
      }
    } catch (err) {
      console.error('Error decoding JWT:', err);
      clearTokens();
      localStorage.removeItem('user_id');
      setIsAuthenticated(false);
      setUser(null);
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
    setUserId(null);
  };

  return { isAuthenticated, user, userId, logout, loading };
};

export default useAuth;