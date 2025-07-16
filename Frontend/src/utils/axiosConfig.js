import axios from 'axios';
import { getTenantBaseURL } from './getTenantBaseURL';
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './auth';

const api = axios.create({
  baseURL: getTenantBaseURL(),
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${getTenantBaseURL()}token/refresh/`, {
          refresh: getRefreshToken()
        });
        const { access } = res.data;
        setTokens({ access, refresh: getRefreshToken() });

        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        return api(originalRequest);
      } catch (err) {
        clearTokens();
        window.location.href = '/';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default api;