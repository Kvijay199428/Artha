import axios, { AxiosError } from 'axios';

// Production (via Nginx proxy): /api/v1 — same origin, no CORS
// Development: http://localhost:8000/api/v1 (set in .env.development)
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.dispatchEvent(new Event('unauthorized'));
    }

    const customError = {
      message: 'An unexpected error occurred',
      code: 'UNKNOWN_ERROR',
      fields: {} as Record<string, string>,
      status: error.response?.status || 500,
    };

    if (error.response?.data) {
      const data = error.response.data as any;
      if (data.detail && Array.isArray(data.detail)) {
        customError.message = 'Validation failed';
        customError.code = 'VALIDATION_ERROR';
        data.detail.forEach((err: any) => {
          customError.fields[err.loc.join('.')] = err.msg;
        });
      } else if (data.error) {
        customError.message = data.error.message || data.message || 'An error occurred';
        customError.code = data.error.code || 'API_ERROR';
      } else if (data.message) {
        customError.message = data.message;
        customError.code = data.code || 'API_ERROR';
      }
    }

    return Promise.reject(customError);
  }
);
