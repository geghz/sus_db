import api from './axios';

export function loginRequest({ login, password, remember }) {
  // { login: <username or email>, password, remember }
  return api.post('/api/auth/token/', { login, password, remember });
}

export function refreshRequest() {
  return api.post('/api/auth/token/refresh/');
}

export function meRequest() {
  return api.get('/api/accounts/me/');
}
