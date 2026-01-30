/**
 * 认证状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi } from '@/api';
import type { User, LoginParams, RegisterParams } from '@/types';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();

  // 状态
  const user = ref<User | null>(null);
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const isLoading = ref(false);
  const isInitialized = ref(false);

  // 计算属性
  const isAuthenticated = computed(() => !!accessToken.value);
  const userName = computed(() => user.value?.username || '');
  const userAvatar = computed(() => user.value?.avatar || '');

  // 方法
  async function login(params: LoginParams) {
    isLoading.value = true;
    try {
      const response = await authApi.login(params);
      const { user: userData, access, refresh } = response?.data || {};

      if (userData && access && refresh) {
        user.value = userData;
        accessToken.value = access;
        refreshToken.value = refresh;
        isInitialized.value = true;

        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        return { success: true };
      }
      return { success: false, message: '登录失败' };
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { message?: string } } };
      return {
        success: false,
        message: axiosError.response?.data?.message || '登录失败'
      };
    } finally {
      isLoading.value = false;
    }
  }

  async function register(params: RegisterParams) {
    isLoading.value = true;
    try {
      const response = await authApi.register(params);
      const { user: userData, access, refresh } = response?.data || {};

      if (userData && access && refresh) {
        user.value = userData;
        accessToken.value = access;
        refreshToken.value = refresh;
        isInitialized.value = true;

        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);

        return { success: true };
      }
      return { success: false, message: '注册失败' };
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { message?: string } } };
      return {
        success: false,
        message: axiosError.response?.data?.message || '注册失败'
      };
    } finally {
      isLoading.value = false;
    }
  }

  async function initAuth() {
    if (isInitialized.value) return;

    const storedAccessToken = localStorage.getItem('accessToken');
    const storedRefreshToken = localStorage.getItem('refreshToken');

    if (!storedAccessToken || !storedRefreshToken) {
      isInitialized.value = true;
      return;
    }

    accessToken.value = storedAccessToken;
    refreshToken.value = storedRefreshToken;

    // 尝试获取用户信息（使用 fetch 避免 axios 拦截器干扰）
    try {
      const response = await fetch(`http://localhost:8000/api/auth/profile/`, {
        headers: {
          'Authorization': `Bearer ${storedAccessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const json = await response.json();
        if (json.data) {
          user.value = json.data;
        }
      } else {
        // 401 - token 无效，尝试刷新
        if (response.status === 401) {
          await refreshTokenDirect(storedRefreshToken);
        }
      }
    } catch {
      // 网络错误或其他问题
    }

    isInitialized.value = true;
  }

  async function refreshTokenDirect(refresh: string) {
    try {
      const response = await fetch(`http://localhost:8000/api/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });

      if (response.ok) {
        const json = await response.json();
        if (json.data?.access) {
          accessToken.value = json.data.access;
          localStorage.setItem('accessToken', json.data.access);

          // 用新 token 获取用户信息
          const profileResponse = await fetch(`http://localhost:8000/api/auth/profile/`, {
            headers: {
              'Authorization': `Bearer ${json.data.access}`,
              'Content-Type': 'application/json',
            },
          });

          if (profileResponse.ok) {
            const profileJson = await profileResponse.json();
            if (profileJson.data) {
              user.value = profileJson.data;
            }
          }
        } else {
          clearAuth();
        }
      } else {
        // 刷新失败，清除认证状态
        clearAuth();
      }
    } catch {
      clearAuth();
    }
  }

  function clearAuth() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  function logout(navigate = true) {
    clearAuth();
    isInitialized.value = false;
    if (navigate) {
      router?.push?.('/login');
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    isInitialized,
    isAuthenticated,
    userName,
    userAvatar,
    login,
    register,
    initAuth,
    logout,
  };
});
