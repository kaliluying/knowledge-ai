/**
 * 认证逻辑组合式函数
 */

import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

export function useAuth() {
  const authStore = useAuthStore();
  const router = useRouter();

  // 状态
  const user = computed(() => authStore.user);
  const isAuthenticated = computed(() => authStore.isAuthenticated);
  const isLoading = computed(() => authStore.isLoading);

  // 方法
  async function login(email: string, password: string) {
    const result = await authStore.login({ email, password });
    if (result.success) {
      router.push('/');
    }
    return result;
  }

  async function register(data: { username: string; email: string; password: string; password2: string }) {
    const result = await authStore.register(data);
    if (result.success) {
      router.push('/login');
    }
    return result;
  }

  function logout() {
    authStore.logout();
    router.push('/login');
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };
}
