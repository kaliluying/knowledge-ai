<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores';
import type { LoginParams } from '@/types';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = ref<LoginParams>({
  email: '',
  password: '',
});

const error = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const handleSubmit = async () => {
  error.value = '';
  isLoading.value = true;

  try {
    const result = await authStore.login(form.value);
    if (result.success) {
      const redirect = route.query.redirect as string;
      router.push(redirect || '/');
    } else {
      error.value = result.message || '登录失败，请检查账号和密码';
    }
  } catch {
    error.value = '登录失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-page">
    <!-- Left side - Decorative -->
    <div class="left-panel">
      <!-- Gradient background -->
      <div class="gradient-bg"></div>
      
      <!-- Decorative circles -->
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      
      <!-- Content -->
      <div class="left-content">
        <div class="left-content-inner">
          <!-- Logo -->
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          
          <!-- Heading -->
          <h1 class="title">知识管理</h1>
          <p class="subtitle">记录你的思考，连接你的知识，构建你的第二大脑</p>
          
          <!-- Features -->
          <div class="features">
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>优雅的笔记体验</span>
            </div>
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>智能分类整理</span>
            </div>
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>知识图谱可视化</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right side - Login form -->
    <div class="right-panel">
      <div class="right-content">
        <!-- Mobile logo -->
        <div class="mobile-logo">
          <div class="mobile-logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h1>Knowledge</h1>
        </div>

        <!-- Login card -->
        <div class="login-card">
          <div class="card-header">
            <h2>欢迎回来 👋</h2>
            <p>请登录您的账号以继续</p>
          </div>

          <!-- Error message -->
          <div v-if="error" class="error-message">
            <span class="error-icon">!</span>
            {{ error }}
          </div>

          <form class="login-form" @submit.prevent="handleSubmit">
            <!-- Email -->
            <div class="form-group">
              <label for="email">邮箱地址</label>
              <div class="input-wrapper">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </span>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  required
                  placeholder="请输入邮箱地址"
                  class="form-input"
                />
              </div>
            </div>

            <!-- Password -->
            <div class="form-group">
              <div class="label-row">
                <label for="password">密码</label>
                <a href="#" class="forgot-link">忘记密码？</a>
              </div>
              <div class="input-wrapper">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </span>
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  placeholder="请输入密码"
                  class="form-input"
                />
                <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                  <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Submit -->
            <button type="submit" :disabled="isLoading" class="submit-btn">
              <span v-if="isLoading" class="loading">
                <svg class="spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" opacity="0.25"/>
                  <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                登录中...
              </span>
              <span v-else>登录</span>
            </button>
          </form>

          <!-- Register link -->
          <div class="register-link">
            <p>还没有账号？<router-link to="/register">立即注册 →</router-link></p>
          </div>
        </div>

        <!-- Footer -->
        <p class="footer">© 2025 Knowledge. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Login page container */
.login-page {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

/* Left panel */
.left-panel {
  width: 45%;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gradient-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 50%, #6366f1 100%);
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
}

.circle-2 {
  width: 400px;
  height: 400px;
  bottom: -150px;
  left: -150px;
}

.circle-3 {
  width: 500px;
  height: 500px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.05);
}

/* Left content */
.left-content {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 480px;
  padding: 40px;
}

.left-content-inner {
  color: white;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  backdrop-filter: blur(10px);
}

.logo-icon svg {
  width: 48px;
  height: 48px;
}

.title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.2;
}

.subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  margin-bottom: 32px;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.check-icon {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

/* Right panel */
.right-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: linear-gradient(135deg, #f8fafc 0%, #f5f3ff 50%, #ede9fe 100%);
}

.right-content {
  width: 100%;
  max-width: 440px;
}

.mobile-logo {
  display: none;
  text-align: center;
  margin-bottom: 32px;
}

.mobile-logo-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  box-shadow: 0 10px 40px rgba(124, 58, 237, 0.3);
}

.mobile-logo-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.mobile-logo h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

/* Login card */
.login-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px);
}

.card-header {
  margin-bottom: 32px;
}

.card-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.card-header p {
  font-size: 14px;
  color: #6b7280;
}

/* Error message */
.error-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 24px;
}

.error-icon {
  width: 20px;
  height: 20px;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.forgot-link {
  font-size: 14px;
  color: #8b5cf6;
  text-decoration: none;
}

.forgot-link:hover {
  color: #7c3aed;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  width: 20px;
  height: 20px;
  color: #9ca3af;
  z-index: 10;
  transition: color 0.2s;
}

.input-wrapper:focus-within .input-icon {
  color: #8b5cf6;
}

.input-icon svg {
  width: 100%;
  height: 100%;
}

.form-input {
  width: 100%;
  padding: 14px 16px 14px 52px;
  background: #f8fafc;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus {
  background: white;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.toggle-password {
  position: absolute;
  right: 16px;
  width: 20px;
  height: 20px;
  color: #9ca3af;
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
}

.toggle-password:hover {
  color: #6b7280;
}

.toggle-password svg {
  width: 100%;
  height: 100%;
}

/* Submit button */
.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(124, 58, 237, 0.5);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Register link */
.register-link {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.register-link p {
  font-size: 14px;
  color: #6b7280;
}

.register-link a {
  color: #8b5cf6;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  color: #7c3aed;
}

/* Footer */
.footer {
  text-align: center;
  margin-top: 32px;
  font-size: 13px;
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 1024px) {
  .left-panel {
    display: none;
  }
  
  .right-panel {
    width: 100%;
  }
  
  .mobile-logo {
    display: block;
  }
}
</style>
