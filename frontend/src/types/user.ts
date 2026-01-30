/**
 * 用户类型定义
 */

export interface User {
  id: number;
  email: string;
  username: string;
  avatar: string | null;
  bio: string | null;
  created_at: string;
  updated_at: string;
}

export interface LoginParams {
  email: string;
  password: string;
}

export interface RegisterParams {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  code: number;
  message: string;
  data: {
    user: User;
    access: string;
    refresh: string;
  };
}
