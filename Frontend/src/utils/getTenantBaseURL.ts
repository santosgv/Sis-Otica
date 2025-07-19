// utils/getTenantBaseURL.ts

export const getTenantBaseURL = (): string => {
  const hostname = window.location.hostname;

  // Garante que o hostname seja válido
  if (!hostname) {
    console.warn('Hostname não identificado. Usando fallback.');
    return 'https:sgosistemas.com.br/api/v1/';
  }

  // Detecta se está em produção
  const isProduction = window.location.protocol === 'https:';

  const protocol = isProduction ? 'https' : 'http';

  // Em produção, o backend normalmente não usa :8000
  const port = isProduction ? '' : ':8000';

  return `${protocol}://${hostname}${port}/api/v1/`;
};
