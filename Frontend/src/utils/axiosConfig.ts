// utils/axiosConfig.ts

import axios, { AxiosError } from 'axios';
import type { AxiosRequestConfig,AxiosResponse } from 'axios';
import { getTenantBaseURL } from './getTenantBaseURL';
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './auth';

// Estendendo AxiosRequestConfig para adicionar uma propriedade personalizada
interface CustomAxiosRequestConfig extends AxiosRequestConfig {
  _retry?: boolean;
}

// Criação da instância com baseURL
const api = axios.create({
  baseURL: getTenantBaseURL(),
});

// Interceptor de requisição para incluir o token de autenticação
  api.interceptors.request.use(config => {
    const token = getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  });

// Interceptor de resposta para lidar com refresh do token
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as CustomAxiosRequestConfig;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${getTenantBaseURL()}token/refresh/`, {
          refresh: getRefreshToken(),
        });

        const { access } = res.data as { access: string };
        const refresh = getRefreshToken();

        if (access && refresh) {
          setTokens({ access, refresh });

          // Atualiza o header da instância e da requisição original
          api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          if (originalRequest.headers) {
            originalRequest.headers['Authorization'] = `Bearer ${access}`;
          }

          return api(originalRequest);
        } else {
          throw new Error('Tokens inválidos no refresh.');
        }
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
