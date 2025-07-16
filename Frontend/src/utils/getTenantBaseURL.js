export const getTenantBaseURL = () => {
  const hostname = window.location.hostname; // Ex: cliente1.app.local
  return `http://${hostname}:8000/api/v1/`; // ou https se for produção
};