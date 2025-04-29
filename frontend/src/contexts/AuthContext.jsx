import React, {
  createContext,
  useState,
  useEffect,
  useCallback
} from 'react';
import api from '../api/axios';
import { loginRequest, refreshRequest, meRequest } from '../api/auth';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext({
  user: null,
  isAuthenticated: false,
  login: async () => {},
  logout: () => {}
});

export function AuthProvider({ children }) {
  const navigate = useNavigate();

  const [accessToken, setAccessToken] = useState(
    () => localStorage.getItem('accessToken')
  );
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const reqId = api.interceptors.request.use(cfg => {
      if (accessToken) {
        cfg.headers['Authorization'] = `Bearer ${accessToken}`;
      }
      return cfg;
    });

    const resId = api.interceptors.response.use(
      res => res,
      async err => {
        const original = err.config;
        if (err.response?.status === 401 && !original._retry) {
          original._retry = true;
          try {
            const { data } = await refreshRequest();
            localStorage.setItem('accessToken', data.access);
            setAccessToken(data.access);
            original.headers['Authorization'] = `Bearer ${data.access}`;
            return api(original);
          } catch {
            logout();
          }
        }
        return Promise.reject(err);
      }
    );

    return () => {
      api.interceptors.request.eject(reqId);
      api.interceptors.response.eject(resId);
    };
  }, [accessToken]);

  useEffect(() => {
    async function init() {
      if (accessToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        try {
          const { data } = await meRequest();
          setUser(data);
        } catch {
          localStorage.removeItem('accessToken');
          setAccessToken(null);
        }
      }
      setLoading(false);
    }
    init();
  }, [accessToken]);

  const login = async ({ login, password, remember }) => {
    const { data } = await loginRequest({ login, password, remember });
    localStorage.setItem('accessToken', data.access);
    setAccessToken(data.access);
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
    const { data: me } = await meRequest();
    setUser(me);
    const to = window.history.state?.usr?.location?.state?.from?.pathname || '/';
    navigate(to, { replace: true });
  };

  const logout = useCallback(() => {
    localStorage.removeItem('accessToken');
    setAccessToken(null);
    setUser(null);
    navigate('/login', { replace: true });
  }, [navigate]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: Boolean(user),
        login,
        logout
      }}
    >
      {loading ? null : children}
    </AuthContext.Provider>
  );
}
