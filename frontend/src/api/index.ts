/**
 * API 导出汇总
 */

import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Centralized default API URL configuration
const DEFAULT_API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || DEFAULT_API_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器 - 处理 401 错误，自动刷新 token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 401 未授权，尝试刷新 token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(
            `${import.meta.env.VITE_API_URL || DEFAULT_API_URL}/auth/refresh/`,
            { refresh: refreshToken }
          );

          if (response.data?.data?.access) {
            const newAccessToken = response.data.data.access;
            localStorage.setItem('accessToken', newAccessToken);

            // 重试原请求
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return api(originalRequest);
          }
        } catch {
          // 刷新失败，清除 token 并跳转登录
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
          return Promise.reject(error);
        }
      }
    }

    return Promise.reject(error);
  }
);

export { api };
export * from './auth';
export * from './notes';
export * from './categories';
export * from './tags';
export * from './collections';
export * from './attachments';
export * from './graph';
