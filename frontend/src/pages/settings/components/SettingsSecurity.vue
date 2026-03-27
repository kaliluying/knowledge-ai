<script setup lang="ts">
import { ref, watch } from 'vue';
import { authApi } from '@/api/auth';

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});

const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);

const passwordStrength = ref({
  hasLength: false,
  hasUpper: false,
  hasLower: false,
  hasDigit: false,
  hasSpecial: false,
});

const checkPasswordStrength = (password: string) => {
  passwordStrength.value = {
    hasLength: password.length >= 8,
    hasUpper: /[A-Z]/.test(password),
    hasLower: /[a-z]/.test(password),
    hasDigit: /[0-9]/.test(password),
    hasSpecial: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password),
  };
};

watch(() => passwordForm.value.newPassword, (newVal) => {
  checkPasswordStrength(newVal);
});

const handleChangePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    message.value = { type: 'error', text: '两次输入的密码不一致' };
    return;
  }

  const { hasLength, hasUpper, hasLower, hasDigit, hasSpecial } = passwordStrength.value;
  if (!hasLength || !hasUpper || !hasLower || !hasDigit || !hasSpecial) {
    message.value = { type: 'error', text: '密码不符合强度要求' };
    return;
  }

  isSaving.value = true;
  message.value = null;

  try {
    await authApi.changePassword(
      passwordForm.value.currentPassword,
      passwordForm.value.newPassword
    );
    message.value = { type: 'success', text: '密码已成功更改' };
    passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch (error: unknown) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    message.value = {
      type: 'error',
      text: axiosError.response?.data?.message || '密码更改失败，请检查当前密码是否正确'
    };
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

    <div class="section-header">
      <h2>账户安全</h2>
      <p>管理你的密码和安全设置</p>
    </div>

    <div class="form-card">
      <h3 class="card-title">修改密码</h3>

      <div class="form-group">
        <label>当前密码</label>
        <div class="input-with-action">
          <input
            v-model="passwordForm.currentPassword"
            :type="showCurrentPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="输入当前密码"
          />
          <button type="button" class="toggle-visibility" @click="showCurrentPassword = !showCurrentPassword">
            <svg v-if="!showCurrentPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" />
              <line x1="1" y1="1" x2="23" y2="23" />
            </svg>
          </button>
        </div>
      </div>

      <div class="form-group">
        <label>新密码</label>
        <div class="input-with-action">
          <input
            v-model="passwordForm.newPassword"
            :type="showNewPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="输入新密码"
          />
          <button type="button" class="toggle-visibility" @click="showNewPassword = !showNewPassword">
            <svg v-if="!showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" />
              <line x1="1" y1="1" x2="23" y2="23" />
            </svg>
          </button>
        </div>

        <div class="password-strength">
          <div class="strength-item" :class="{ met: passwordStrength.hasLength }">
            <span class="check">✓</span> 至少 8 个字符
          </div>
          <div class="strength-item" :class="{ met: passwordStrength.hasUpper }">
            <span class="check">✓</span> 大写字母
          </div>
          <div class="strength-item" :class="{ met: passwordStrength.hasLower }">
            <span class="check">✓</span> 小写字母
          </div>
          <div class="strength-item" :class="{ met: passwordStrength.hasDigit }">
            <span class="check">✓</span> 数字
          </div>
          <div class="strength-item" :class="{ met: passwordStrength.hasSpecial }">
            <span class="check">✓</span> 特殊字符
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>确认新密码</label>
        <div class="input-with-action">
          <input
            v-model="passwordForm.confirmPassword"
            :type="showConfirmPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="再次输入新密码"
          />
          <button type="button" class="toggle-visibility" @click="showConfirmPassword = !showConfirmPassword">
            <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" />
              <line x1="1" y1="1" x2="23" y2="23" />
            </svg>
          </button>
        </div>
      </div>

      <div class="form-actions">
        <button class="save-btn" @click="handleChangePassword" :disabled="isSaving">
          <span v-if="isSaving">更改中...</span>
          <span v-else>更改密码</span>
        </button>
      </div>
    </div>

    <div class="security-tips">
      <h4>安全提示</h4>
      <ul>
        <li>使用强密码并定期更换</li>
        <li>不要在其他网站使用相同密码</li>
        <li>启用两步验证可进一步提高安全性</li>
      </ul>
    </div>
  </div>
</template>

<style scoped src="../settings-shared.css"></style>
