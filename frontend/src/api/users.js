import api from './axios';

export const fetchUsers = () => api.get('/api/accounts/users/');
export const fetchUser = (id) => api.get(`/api/accounts/users/${id}/`);
export const createUser = (data) => api.post('/api/accounts/users/', data);
export const updateUser = (id, data) => api.put(`/api/accounts/users/${id}/`, data);
export const deleteUser = (id) => api.delete(`/api/accounts/users/${id}/`);
