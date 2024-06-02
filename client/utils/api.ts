import axios from 'axios';
import { BASE_URL } from './constants';

const instance = axios.create({
  baseURL: BASE_URL,
});

const getAuthToken = () => {
  return localStorage.getItem('authToken');
};

const getRefreshToken = () => {
  return localStorage.getItem('refreshToken');
};

const setAuthToken = (token: string) => {
  localStorage.setItem('authToken', token);
};

const refreshAuthToken = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/jwt/refresh/`, {
      refresh: getRefreshToken(),
    });
    setAuthToken(response.data.access);
    return response.data.access;
  } catch (error) {
    console.error('Error refreshing token:', error);
    throw new Error('Unable to refresh token');
  }
};

instance.interceptors.request.use(
  async (config) => {
    let token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response.status === 401 &&
      error.response.data.code === 'token_not_valid' &&
      error.response.data.messages &&
      error.response.data.messages[0].token_class === 'AccessToken' &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        const newToken = await refreshAuthToken();
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return instance(originalRequest);
      } catch (error) {
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export const apiPost = async (path: string, data: any) => {
  try {
    const response = await instance.post(path, data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};

export const imageApiPost = async (path: string, data: any) => {
  try {
    let formData = new FormData();
    formData.append('file', data);
    console.log(formData);
    const response = await instance.post(path, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};

export const apiGet = async (path: string, params: any = {}) => {
  try {
    const response = await instance.get(path, { params });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(`Error: ${error.response.data.error}`);
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};
