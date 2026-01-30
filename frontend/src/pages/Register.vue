<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import type { RegisterParams } from '@/types';

const router = useRouter();
const authStore = useAuthStore();

const form = ref<RegisterParams>({
  email: '',
  username: '',
  password: '',
  password_confirm: '',
});

const error = ref('');
const isLoading = ref(false);
const showPassword = ref(false);
const showPasswordConfirm = ref(false);

const handleSubmit = async () => {
  error.value = '';

  if (form.value.password !== form.value.password_confirm) {
    error.value = '两次输入的密码不一致';
    return;
  }

  // 客户端密码格式验证
  const password = form.value.password;
  if (password.length < 8) {
    error.value = '密码长度至少为8个字符';
    return;
  }
  if (!/[A-Z]/.test(password)) {
    error.value = '密码必须包含至少一个大写字母';
    return;
  }
  if (!/[a-z]/.test(password)) {
    error.value = '密码必须包含至少一个小写字母';
    return;
  }
  if (!/[0-9]/.test(password)) {
    error.value = '密码必须包含至少一个数字';
    return;
  }
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    error.value = '密码必须包含至少一个特殊字符';
    return;
  }

  isLoading.value = true;

  try {
    const result = await authStore.register(form.value);
    if (result.success) {
      router.push('/');
    } else {
      error.value = result.message || '注册失败';
    }
  } catch {
    error.value = '注册失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-page">
    <!-- Left side - Decorative -->
    <div class="left-panel">
      <div class="gradient-bg"></div>
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      
      <div class="left-content">
        <div class="left-content-inner">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          
          <h1 class="title">加入我们</h1>
          <p class="subtitle">创建您的账户，开启知识管理之旅</p>
          
          <div class="features">
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>完全免费使用</span>
            </div>
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>无限笔记存储</span>
            </div>
            <div class="feature-item">
              <span class="check-icon">✓</span>
              <span>数据安全保护</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right side - Register form -->
    <div class="right-panel">
      <div class="right-content">
        <div class="mobile-logo">
          <div class="mobile-logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
          <h1>Knowledge</h1>
        </div>

        <div class="login-card">
          <div class="card-header">
            <h2>创建账号 👋</h2>
            <p>请填写以下信息完成注册</p>
          </div>

          <div v-if="error" class="error-message">
            <span class="error-icon">!</span>
            {{ error }}
          </div>

          <form class="login-form" @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="username">用户名</label>
              <div class="input-wrapper">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </span>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  required
                  minlength="2"
                  maxlength="20"
                  placeholder="请输入用户名（2-20字符）"
                  class="form-input"
                />
              </div>
            </div>

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

            <div class="form-group">
              <label for="password">密码</label>
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
                  minlength="8"
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

            <!-- Password requirements hint -->
            <div class="password-hint">
              <p class="password-hint-title">密码要求：</p>
              <ul class="password-hint-list">
                <li class="password-hint-item">至少 8 个字符</li>
                <li class="password-hint-item">包含大写字母（A-Z）</li>
                <li class="password-hint-item">包含小写字母（a-z）</li>
                <li class="password-hint-item">包含数字（0-9）</li>
                <li class="password-hint-item">包含特殊字符（!@#$%^&amp;* 等）</li>
              </ul>
            </div>

            <div class="form-group">
              <label for="password_confirm">确认密码</label>
              <div class="input-wrapper">
                <span class="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </span>
                <input
                  id="password_confirm"
                  v-model="form.password_confirm"
                  :type="showPasswordConfirm ? 'text' : 'password'"
                  required
                  placeholder="请再次输入密码"
                  class="form-input"
                />
                <button type="button" class="toggle-password" @click="showPasswordConfirm = !showPasswordConfirm">
                  <svg v-if="!showPasswordConfirm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                </button>
              </div>
            </div>

            <button type="submit" :disabled="isLoading" class="submit-btn">
              <span v-if="isLoading" class="loading">
                <svg class="spinner" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" opacity="0.25"/>
                  <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                注册中...
              </span>
              <span v-else>创建账号</span>
            </button>
          </form>

          <div class="register-link">
            <p>已有账号？<router-link to="/login">立即登录 →</router-link></p>
          </div>
        </div>

        <p class="footer">© 2025 Knowledge. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

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

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.password-hint {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 16px;
  margin-top: -8px;
}

.password-hint-title {
  font-size: 13px;
  font-weight: 600;
  color: #0369a1;
  margin-bottom: 10px;
}

.password-hint-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.password-hint-item {
  font-size: 12px;
  color: #0c4a6e;
  display: flex;
  align-items: center;
  gap: 6px;
}

.password-hint-item::before {
  content: "•";
  color: #0284c7;
  font-weight: bold;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
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
  margin-top: 8px;
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

.footer {
  text-align: center;
  margin-top: 32px;
  font-size: 13px;
  color: #9ca3af;
}

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
