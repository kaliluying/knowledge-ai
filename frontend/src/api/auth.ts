/**
 * 认证 API
 */

import { api } from './index';
import type { User, LoginParams, RegisterParams, AuthResponse } from '@/types';

export const authApi = {
  // 注册
  async register(data: RegisterParams) {
    const response = await api.post<AuthResponse>('/auth/register/', data);
    return response.data;
  },

  // 登录
  async login(data: LoginParams) {
    const response = await api.post<AuthResponse>('/auth/login/', data);
    return response.data;
  },

  // 登出
  async logout(refreshToken: string) {
    const response = await api.post('/auth/logout/', { refresh: refreshToken });
    return response.data;
  },

  // 获取用户信息
  async getProfile() {
    const response = await api.get<{ code: number; message: string; data: User }>('/auth/profile/');
    return response.data;
  },

  // 更新用户信息
  async updateProfile(data: Partial<User>) {
    const response = await api.put('/auth/profile/', data);
    return response.data;
  },

  // 修改密码
  async changePassword(oldPassword: string, newPassword: string) {
    const response = await api.post('/auth/password/', {
      old_password: oldPassword,
      new_password: newPassword,
    });
    return response.data;
  },

  // 刷新 Token
  async refreshToken(refreshToken: string) {
    const response = await api.post<{ code: number; message: string; data: { access: string } }>(
      '/auth/refresh/',
      { refresh: refreshToken }
    );
    return response.data;
  },
};
