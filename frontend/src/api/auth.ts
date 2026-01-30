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

  // 上传头像
  async updateAvatar(formData: FormData) {
    const response = await api.put('/auth/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
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

  // 获取偏好设置
  async getPreferences() {
    const response = await api.get<{ code: number; message: string; data: Record<string, unknown> }>(
      '/auth/preferences/'
    );
    return response.data;
  },

  // 更新偏好设置
  async updatePreferences(data: Record<string, unknown>) {
    const response = await api.put('/auth/preferences/', data);
    return response.data;
  },

  // 获取登录设备列表
  async getSessions() {
    const response = await api.get<{ code: number; message: string; data: { sessions: Array<{ id: string; device: string; location: string; last_active: string; current: boolean }> } }>(
      '/auth/sessions/'
    );
    return response.data;
  },

  // 退出指定设备
  async revokeSession(sessionId: string) {
    const response = await api.delete(`/auth/sessions/${sessionId}/`);
    return response.data;
  },

  // 获取存储统计
  async getStorage() {
    const response = await api.get<{
      code: number;
      message: string;
      data: {
        notes_count: number;
        notes_size: number;
        attachments_count: number;
        attachments_size: number;
        images_count: number;
        images_size: number;
        total_size: number;
      };
    }>('/auth/storage/');
    return response.data;
  },

  // 导出用户数据
  async exportData() {
    const response = await api.get<{ code: number; message: string; data: Record<string, unknown> }>(
      '/auth/export/'
    );
    return response.data;
  },

  // 删除账户
  async deleteAccount(password: string, refreshToken: string) {
    const response = await api.delete('/auth/account/', {
      data: { password, refresh: refreshToken },
    });
    return response.data;
  },
};
