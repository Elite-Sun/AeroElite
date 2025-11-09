import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Design APIs
export const designAPI = {
  create: (data: any) => apiClient.post('/design/create', data),
  get: (id: number) => apiClient.get(`/design/${id}`),
  list: (params?: any) => apiClient.get('/design', { params }),
  update: (id: number, data: any) => apiClient.put(`/design/${id}`, data),
  validate: (id: number) => apiClient.post(`/design/${id}/validate`),
  delete: (id: number) => apiClient.delete(`/design/${id}`),
};

// Assembly APIs
export const assemblyAPI = {
  create: (data: any) => apiClient.post('/assembly/create', data),
  get: (id: number) => apiClient.get(`/assembly/${id}`),
  list: (params?: any) => apiClient.get('/assembly', { params }),
  validate: (id: number) => apiClient.post(`/assembly/${id}/validate`),
};

// Dataset APIs
export const datasetAPI = {
  list: () => apiClient.get('/datasets/list'),
  search: (query: string) => apiClient.get('/datasets/search', { params: { query } }),
  download: (name: string) => apiClient.post(`/datasets/download/${name}`),
};

// Auth APIs
export const authAPI = {
  register: (data: any) => apiClient.post('/auth/register', data),
  login: (data: any) => apiClient.post('/auth/login', data),
  me: () => apiClient.get('/auth/me'),
};

// Export APIs
export const exportAPI = {
  export: (id: number, format: string) =>
    apiClient.post(`/export/${id}`, { format }),
  download: (id: number) =>
    `${API_BASE_URL}/api/v1/export/${id}/download`,
};

export default apiClient;
