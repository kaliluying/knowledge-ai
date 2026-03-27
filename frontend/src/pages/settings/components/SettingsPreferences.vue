<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';

const preferences = ref({
  theme: 'light' as 'light' | 'dark' | 'auto',
  language: 'zh-CN',
  emailNotifications: true,
  browserNotifications: false,
  autoSave: true,
  compactMode: false,
});

const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);

const applyTheme = (theme: string) => {
  document.documentElement.removeAttribute('data-theme');
  document.documentElement.removeAttribute('class');
  if (theme !== 'light') {
    document.documentElement.setAttribute('data-theme', theme);
  }
};

const handleThemeChange = (theme: 'light' | 'dark' | 'auto') => {
  preferences.value.theme = theme;
  applyTheme(theme);
  localStorage.setItem('userPreferences', JSON.stringify(preferences.value));
};

const handleSavePreferences = async () => {
  isSaving.value = true;
  message.value = null;

  try {
    await authApi.updatePreferences({
      theme: preferences.value.theme,
      language: preferences.value.language,
    });

    localStorage.setItem('userPreferences', JSON.stringify(preferences.value));
    applyTheme(preferences.value.theme);

    message.value = { type: 'success', text: '偏好设置已保存' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch (error: unknown) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    message.value = {
      type: 'error',
      text: axiosError.response?.data?.message || '保存失败'
    };
  } finally {
    isSaving.value = false;
  }
};

const loadPreferences = async () => {
  try {
    const response = await authApi.getPreferences();
    if (response?.data) {
      preferences.value.theme = ((response.data as Record<string, unknown>).theme as "light" | "dark" | "auto") || 'light';
      preferences.value.language = (response.data as Record<string, unknown>).language as string || 'zh-CN';
      applyTheme(preferences.value.theme);
    }
  } catch {
    const savedPrefs = localStorage.getItem('userPreferences');
    if (savedPrefs) {
      const parsed = JSON.parse(savedPrefs);
      preferences.value.theme = parsed.theme || 'light';
      preferences.value.language = parsed.language || 'zh-CN';
      applyTheme(preferences.value.theme);
    }
  }
};

onMounted(() => {
  loadPreferences();
});
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

    <div class="section-header">
      <h2>偏好设置</h2>
      <p>自定义你的使用体验</p>
    </div>

    <div class="form-card">
      <h3 class="card-title">外观</h3>

      <div class="form-group">
        <label>主题</label>
        <div class="toggle-group">
          <button
            class="toggle-btn"
            :class="{ active: preferences.theme === 'light' }"
            @click="handleThemeChange('light')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" />
              <line x1="12" y1="21" x2="12" y2="23" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
              <line x1="1" y1="12" x2="3" y2="12" />
              <line x1="21" y1="12" x2="23" y2="12" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            </svg>
            浅色
          </button>
          <button
            class="toggle-btn"
            :class="{ active: preferences.theme === 'dark' }"
            @click="handleThemeChange('dark')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
            </svg>
            深色
          </button>
          <button
            class="toggle-btn"
            :class="{ active: preferences.theme === 'auto' }"
            @click="handleThemeChange('auto')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41" />
            </svg>
            跟随系统
          </button>
        </div>
      </div>

      <div class="form-group">
        <label>语言</label>
        <select v-model="preferences.language" class="form-input">
          <option value="zh-CN">简体中文</option>
          <option value="en-US">English</option>
        </select>
      </div>

      <div class="form-group">
        <label class="toggle-label">
          <span>简洁模式</span>
          <span class="toggle-hint">减少界面元素，更专注于内容</span>
        </label>
        <label class="switch">
          <input type="checkbox" v-model="preferences.compactMode" />
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <div class="form-card">
      <h3 class="card-title">通知</h3>

      <div class="form-group">
        <label class="toggle-label">
          <span>邮件通知</span>
          <span class="toggle-hint">通过邮件接收重要通知</span>
        </label>
        <label class="switch">
          <input type="checkbox" v-model="preferences.emailNotifications" />
          <span class="slider"></span>
        </label>
      </div>

      <div class="form-group">
        <label class="toggle-label">
          <span>浏览器通知</span>
          <span class="toggle-hint">在浏览器中接收实时通知</span>
        </label>
        <label class="switch">
          <input type="checkbox" v-model="preferences.browserNotifications" />
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <div class="form-card">
      <h3 class="card-title">编辑器</h3>

      <div class="form-group">
        <label class="toggle-label">
          <span>自动保存</span>
          <span class="toggle-hint">编辑时自动保存内容</span>
        </label>
        <label class="switch">
          <input type="checkbox" v-model="preferences.autoSave" />
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <div class="form-actions">
      <button class="save-btn" @click="handleSavePreferences" :disabled="isSaving">
        <span v-if="isSaving">保存中...</span>
        <span v-else>保存设置</span>
      </button>
    </div>
  </div>
</template>

<style scoped src="../settings-shared.css"></style>
