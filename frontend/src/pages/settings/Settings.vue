<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { authApi } from '@/api/auth';

const router = useRouter();
const authStore = useAuthStore();

// Profile form
const profileForm = ref({
  username: '',
  email: '',
  bio: '',
  avatar: '',
});

// Password form
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});

// Password visibility
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

// Password strength
const passwordStrength = ref({
  hasLength: false,
  hasUpper: false,
  hasLower: false,
  hasDigit: false,
  hasSpecial: false,
});

// Preferences
const preferences = ref({
  theme: 'light' as 'light' | 'dark' | 'auto',
  language: 'zh-CN',
  emailNotifications: true,
  browserNotifications: false,
  autoSave: true,
  compactMode: false,
});

// Sessions management
const sessions = ref<Array<{ id: string; device: string; location: string; lastActive: string; current: boolean }>>([]);
const showSessionModal = ref(false);

// Storage stats
const storageStats = ref({
  notes_count: 0,
  notes_size: 0,
  attachments_count: 0,
  attachments_size: 0,
  images_count: 0,
  images_size: 0,
  total_size: 0,
});

// UI state
const activeTab = ref('profile');
const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);
const showDeleteModal = ref(false);
const deleteConfirmText = ref('');
const avatarFile = ref<File | null>(null);
const avatarPreview = ref('');

// Tabs
const tabs = [
  { id: 'profile', label: '个人资料', icon: 'user' },
  { id: 'security', label: '账户安全', icon: 'shield' },
  { id: 'preferences', label: '偏好设置', icon: 'settings' },
  { id: 'sessions', label: '登录设备', icon: 'laptop' },
  { id: 'data', label: '数据管理', icon: 'database' },
  { id: 'danger', label: '危险区域', icon: 'danger' },
];

// Load user profile
const loadUserProfile = async () => {
  await authStore.fetchProfile();
  if (authStore.user) {
    profileForm.value = {
      username: authStore.user.username || '',
      email: authStore.user.email || '',
      bio: authStore.user.bio || '',
      avatar: authStore.user.avatar || '',
    };
  }
  // Load preferences from backend
  await loadPreferences();
  // Load storage stats
  await loadStorageStats();
};

// Apply theme
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

// Password strength checker
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

// Handle avatar selection
const handleAvatarChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];
    if (file.size > 2 * 1024 * 1024) {
      message.value = { type: 'error', text: '头像大小不能超过2MB' };
      return;
    }
    avatarFile.value = file;
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      avatarPreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

// Save profile
const handleSaveProfile = async () => {
  isSaving.value = true;
  message.value = null;

  try {
    // Upload avatar if selected
    if (avatarFile.value) {
      const formData = new FormData();
      formData.append('avatar', avatarFile.value);
      await authApi.updateAvatar(formData);
    }

    await authApi.updateProfile({
      username: profileForm.value.username,
      bio: profileForm.value.bio,
    });

    await authStore.fetchProfile();
    message.value = { type: 'success', text: '个人资料已更新' };
    avatarFile.value = null;
    avatarPreview.value = '';
    setTimeout(() => { message.value = null; }, 3000);
  } catch {
    message.value = { type: 'error', text: '更新失败，请稍后重试' };
  } finally {
    isSaving.value = false;
  }
};

// Change password
const handleChangePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    message.value = { type: 'error', text: '两次输入的密码不一致' };
    return;
  }

  // Check password strength
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

// Save preferences
const handleSavePreferences = async () => {
  isSaving.value = true;
  message.value = null;

  try {
    // Save to backend
    await authApi.updatePreferences({
      theme: preferences.value.theme,
      language: preferences.value.language,
    });

    // Also save to localStorage for offline/backup
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

// Load preferences from backend
const loadPreferences = async () => {
  try {
    const response = await authApi.getPreferences();
    if (response?.data) {
      preferences.value.theme = ((response.data as Record<string, unknown>).theme as string) || 'light';
      preferences.value.language = (response.data as Record<string, unknown>).language as string || 'zh-CN';
      applyTheme(preferences.value.theme);
    }
  } catch {
    // Use localStorage as fallback
    const savedPrefs = localStorage.getItem('userPreferences');
    if (savedPrefs) {
      const parsed = JSON.parse(savedPrefs);
      preferences.value.theme = parsed.theme || 'light';
      preferences.value.language = parsed.language || 'zh-CN';
      applyTheme(preferences.value.theme);
    }
  }
};

// Load sessions
const loadSessions = async () => {
  try {
    const response = await authApi.getSessions();
    if (response?.data?.sessions) {
      sessions.value = response.data.sessions.map((s: Record<string, unknown>) => ({
        id: String(s.id),
        device: String(s.device || 'Unknown Device'),
        location: String(s.location || 'Unknown'),
        lastActive: String(s.last_active || s.lastActive || new Date().toISOString()),
        current: Boolean(s.current),
      }));
    }
  } catch {
    // Fallback: show current device only
    sessions.value = [{
      id: 'current',
      device: '当前设备',
      location: '本地',
      lastActive: new Date().toISOString(),
      current: true,
    }];
  }
  showSessionModal.value = true;
};

// Revoke session
const revokeSession = async (sessionId: string) => {
  try {
    await authApi.revokeSession(sessionId);
    sessions.value = sessions.value.filter(s => s.id !== sessionId);
    message.value = { type: 'success', text: '设备已退出登录' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch (error: unknown) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    message.value = {
      type: 'error',
      text: axiosError.response?.data?.message || '退出失败'
    };
  }
};

const loadStorageStats = async () => {
  try {
    const response = await authApi.getStorage();
    if (response?.data) {
      storageStats.value = response.data as typeof storageStats.value;
    }
  } catch {
    // Use default values
  }
};

// Export data
const handleExportData = async () => {
  isSaving.value = true;
  try {
    const response = await authApi.exportData();
    if (response?.data) {
      // Create and download file
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `knowledge-ai-export-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }

    message.value = { type: 'success', text: '数据已导出' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch (error: unknown) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    message.value = {
      type: 'error',
      text: axiosError.response?.data?.message || '导出失败'
    };
  } finally {
    isSaving.value = false;
  }
};

// Logout
const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

// Delete account
const handleDeleteAccount = async () => {
  if (deleteConfirmText.value !== authStore.user?.username) {
    message.value = { type: 'error', text: '用户名不匹配' };
    return;
  }

  isSaving.value = true;
  try {
    await authApi.deleteAccount(
      passwordForm.value.currentPassword,
      authStore.refreshToken || ''
    );
    await authStore.logout();
    router.push('/login');
  } catch (error: unknown) {
    const axiosError = error as { response?: { data?: { message?: string } } };
    message.value = {
      type: 'error',
      text: axiosError.response?.data?.message || '账户删除失败，请检查密码是否正确'
    };
    isSaving.value = false;
  }
};

const switchTab = (tabId: string) => {
  activeTab.value = tabId;
  message.value = null;
};

onMounted(() => {
  loadUserProfile();
});
</script>

<template>
  <div class="settings-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>设置</h1>
        <p>管理你的账户和偏好设置</p>
      </div>
    </div>

    <div class="settings-layout">
      <!-- Sidebar -->
      <div class="settings-sidebar">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="switchTab(tab.id)"
        >
          <!-- User Icon -->
          <svg v-if="tab.icon === 'user'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <!-- Shield Icon -->
          <svg v-else-if="tab.icon === 'shield'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          </svg>
          <!-- Laptop Icon -->
          <svg v-else-if="tab.icon === 'laptop'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
            <line x1="2" y1="20" x2="22" y2="20" />
          </svg>
          <!-- Database Icon -->
          <svg v-else-if="tab.icon === 'database'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <ellipse cx="12" cy="5" rx="9" ry="3" />
            <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
            <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
          </svg>
          <!-- Settings Icon -->
          <svg v-else-if="tab.icon === 'settings'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
          </svg>
          <!-- Danger Icon -->
          <svg v-else-if="tab.icon === 'danger'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <span>{{ tab.label }}</span>
        </button>

        <div class="logout-section">
          <button class="logout-btn" @click="handleLogout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
              <polyline points="16,17 21,12 16,7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            退出登录
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="settings-content">
        <!-- Message -->
        <div v-if="message" class="message" :class="message.type">
          {{ message.text }}
        </div>

        <!-- Profile Tab -->
        <div v-if="activeTab === 'profile'" class="settings-section">
          <div class="section-header">
            <h2>个人资料</h2>
            <p>更新你的账户信息和头像</p>
          </div>

          <div class="form-card">
            <!-- Avatar -->
            <div class="avatar-section">
              <div class="avatar-wrapper">
                <img
                  v-if="avatarPreview || authStore.user?.avatar"
                  :src="avatarPreview || authStore.user?.avatar || '/default-avatar.png'"
                  alt="Avatar"
                  class="avatar-image"
                />
                <div v-else class="avatar-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
                    <circle cx="12" cy="7" r="4" />
                  </svg>
                </div>
                <label class="avatar-edit-btn" for="avatar-input">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z" />
                    <circle cx="12" cy="13" r="4" />
                  </svg>
                </label>
                <input
                  id="avatar-input"
                  type="file"
                  accept="image/*"
                  @change="handleAvatarChange"
                  hidden
                />
              </div>
              <div class="avatar-info">
                <p class="avatar-label">头像</p>
                <p class="avatar-hint">支持 JPG、PNG 格式，最大 2MB</p>
              </div>
            </div>

            <div class="form-group">
              <label>用户名</label>
              <input
                v-model="profileForm.username"
                type="text"
                class="form-input"
                placeholder="输入用户名"
                minlength="2"
                maxlength="20"
              />
            </div>

            <div class="form-group">
              <label>邮箱</label>
              <input
                v-model="profileForm.email"
                type="email"
                class="form-input"
                placeholder="输入邮箱"
                disabled
              />
              <p class="form-hint">邮箱不可更改</p>
            </div>

            <div class="form-group">
              <label>个人简介</label>
              <textarea
                v-model="profileForm.bio"
                class="form-textarea"
                placeholder="介绍一下你自己..."
                rows="4"
                maxlength="200"
              ></textarea>
              <p class="form-hint">{{ profileForm.bio.length }}/200</p>
            </div>

            <div class="form-actions">
              <button class="save-btn" @click="handleSaveProfile" :disabled="isSaving">
                <span v-if="isSaving">保存中...</span>
                <span v-else>保存更改</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Security Tab -->
        <div v-if="activeTab === 'security'" class="settings-section">
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

              <!-- Password strength indicator -->
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

          <!-- Security tips -->
          <div class="security-tips">
            <h4>安全提示</h4>
            <ul>
              <li>使用强密码并定期更换</li>
              <li>不要在其他网站使用相同密码</li>
              <li>启用两步验证可进一步提高安全性</li>
            </ul>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-if="activeTab === 'preferences'" class="settings-section">
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

        <!-- Sessions Tab -->
        <div v-if="activeTab === 'sessions'" class="settings-section">
          <div class="section-header">
            <h2>登录设备</h2>
            <p>管理你的登录设备和会话</p>
          </div>

          <div class="form-card">
            <div class="sessions-list">
              <div
                v-for="session in sessions"
                :key="session.id"
                class="session-item"
              >
                <div class="session-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                    <line x1="2" y1="20" x2="22" y2="20" />
                  </svg>
                </div>
                <div class="session-info">
                  <div class="session-device">
                    {{ session.device }}
                    <span v-if="session.current" class="current-badge">当前设备</span>
                  </div>
                  <div class="session-meta">
                    {{ session.location }} · 最后活跃: {{ new Date(session.lastActive).toLocaleString() }}
                  </div>
                </div>
                <button
                  v-if="!session.current"
                  class="revoke-btn"
                  @click="revokeSession(session.id)"
                >
                  退出
                </button>
              </div>
            </div>

            <div class="security-tips">
              <p>如果发现可疑设备，请立即退出该设备并修改密码。</p>
            </div>
          </div>
        </div>

        <!-- Data Management Tab -->
        <div v-if="activeTab === 'data'" class="settings-section">
          <div class="section-header">
            <h2>数据管理</h2>
            <p>导出或管理你的数据</p>
          </div>

          <div class="form-card">
            <h3 class="card-title">导出数据</h3>
            <p class="card-description">导出你的所有数据，包括笔记、分类、标签等信息。</p>

            <div class="export-options">
              <button class="export-btn" @click="handleExportData" :disabled="isSaving">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                导出为 JSON
              </button>
            </div>
          </div>

          <div class="form-card">
            <h3 class="card-title">存储使用</h3>
            <div class="storage-info">
              <div class="storage-item">
                <span class="storage-label">笔记 ({{ storageStats.notes_count }})</span>
                <div class="storage-bar">
                  <div class="storage-fill" :style="{ width: Math.min((storageStats.notes_size / 1024) * 100, 100) + '%' }"></div>
                </div>
                <span class="storage-value">{{ (storageStats.notes_size / 1024).toFixed(1) }} KB</span>
              </div>
              <div class="storage-item">
                <span class="storage-label">附件 ({{ storageStats.attachments_count }})</span>
                <div class="storage-bar">
                  <div class="storage-fill attachments" :style="{ width: Math.min((storageStats.attachments_size / 1024) * 100, 100) + '%' }"></div>
                </div>
                <span class="storage-value">{{ (storageStats.attachments_size / 1024).toFixed(1) }} KB</span>
              </div>
              <div class="storage-item">
                <span class="storage-label">图片 ({{ storageStats.images_count }})</span>
                <div class="storage-bar">
                  <div class="storage-fill images" :style="{ width: Math.min((storageStats.images_size / 1024) * 100, 100) + '%' }"></div>
                </div>
                <span class="storage-value">{{ (storageStats.images_size / 1024).toFixed(1) }} KB</span>
              </div>
              <div class="storage-total">
                <span>总计</span>
                <span class="storage-total-value">{{ (storageStats.total_size / 1024).toFixed(1) }} KB</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Danger Tab -->
        <div v-if="activeTab === 'danger'" class="settings-section">
          <div class="section-header danger">
            <h2>危险区域</h2>
            <p>以下操作不可撤销，请谨慎操作</p>
          </div>

          <div class="danger-card">
            <div class="danger-content">
              <h3>删除账户</h3>
              <p>删除你的账户后，所有数据将被永久删除，包括笔记、分类和标签。此操作无法撤销。</p>
            </div>
            <button class="danger-btn" @click="showDeleteModal = true">
              删除账户
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal">
        <div class="modal-header danger">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            <line x1="12" y1="9" x2="12" y2="13" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
          <h2>删除账户</h2>
        </div>

        <div class="modal-body">
          <p>此操作将永久删除你的账户和所有数据，且无法撤销。</p>
          <p>请输入你的用户名 <strong>{{ authStore.user?.username }}</strong> 以确认。</p>

          <div class="form-group">
            <input
              v-model="deleteConfirmText"
              type="text"
              class="form-input"
              :placeholder="authStore.user?.username"
            />
          </div>
        </div>

        <div class="modal-actions">
          <button class="cancel-btn" @click="showDeleteModal = false">取消</button>
          <button
            class="delete-btn"
            @click="handleDeleteAccount"
            :disabled="deleteConfirmText !== authStore.user?.username || isSaving"
          >
            <span v-if="isSaving">删除中...</span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-page {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.header-left h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.header-left p {
  font-size: 14px;
  color: #9ca3af;
}

.settings-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 32px;
}

.settings-sidebar {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.tab-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.tab-btn.active {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.tab-btn svg {
  width: 20px;
  height: 20px;
}

.logout-section {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  width: 100%;
  background: transparent;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #ef4444;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.1);
}

.logout-btn svg {
  width: 20px;
  height: 20px;
}

.settings-content {
  position: relative;
}

.message {
  position: absolute;
  top: -60px;
  left: 0;
  right: 0;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.success {
  background: #d1fae5;
  color: #065f46;
}

.message.error {
  background: #fee2e2;
  color: #991b1b;
}

.settings-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.section-header {
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.section-header p {
  font-size: 14px;
  color: #9ca3af;
}

.section-header.danger h2 {
  color: #ef4444;
}

.form-card {
  background: white;
  border-radius: 20px;
  border: 2px solid #e5e7eb;
  padding: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
  margin-top: 0;
}

.card-description {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
  margin-top: -8px;
}

.form-hint {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.input-with-action {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-action .form-input {
  padding-right: 48px;
}

.toggle-visibility {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px;
  transition: color 0.2s;
}

.toggle-visibility:hover {
  color: #6b7280;
}

.toggle-visibility svg {
  width: 20px;
  height: 20px;
}

/* Password strength */
.password-strength {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.strength-item {
  font-size: 12px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s;
}

.strength-item.met {
  color: #059669;
}

.strength-item .check {
  width: 14px;
  height: 14px;
  background: #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
  transition: all 0.2s;
}

.strength-item.met .check {
  background: #10b981;
}

/* Toggle switch */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
  flex-shrink: 0;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: 0.3s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

input:checked + .slider {
  background-color: #8b5cf6;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.toggle-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toggle-label span:first-child {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.toggle-hint {
  font-size: 12px;
  color: #9ca3af;
}

/* Avatar section */
.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.avatar-wrapper {
  position: relative;
  width: 96px;
  height: 96px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #e5e7eb;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #e5e7eb;
}

.avatar-placeholder svg {
  width: 40px;
  height: 40px;
  color: #9ca3af;
}

.avatar-edit-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  background: #8b5cf6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 3px solid white;
  transition: background 0.2s;
}

.avatar-edit-btn:hover {
  background: #7c3aed;
}

.avatar-edit-btn svg {
  width: 16px;
  height: 16px;
  color: white;
}

.avatar-info {
  flex: 1;
}

.avatar-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 4px;
}

.avatar-hint {
  font-size: 12px;
  color: #9ca3af;
}

/* Sessions */
.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.session-icon {
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e5e7eb;
}

.session-icon svg {
  width: 24px;
  height: 24px;
  color: #6b7280;
}

.session-info {
  flex: 1;
}

.session-device {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-badge {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  border-radius: 6px;
}

.session-meta {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.revoke-btn {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.revoke-btn:hover {
  background: #fee2e2;
  border-color: #fecaca;
  color: #ef4444;
}

/* Export */
.export-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.export-btn:hover:not(:disabled) {
  border-color: #8b5cf6;
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.export-btn svg {
  width: 20px;
  height: 20px;
}

/* Storage */
.storage-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.storage-item {
  display: grid;
  grid-template-columns: 80px 1fr 60px;
  align-items: center;
  gap: 16px;
}

.storage-label {
  font-size: 14px;
  color: #374151;
}

.storage-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.storage-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 4px;
  transition: width 0.3s;
}

.storage-fill.attachments {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.storage-fill.images {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.storage-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  margin-top: 8px;
}

.storage-total span:first-child {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.storage-total-value {
  font-size: 16px;
  font-weight: 600;
  color: #8b5cf6;
}

.storage-value {
  font-size: 13px;
  color: #6b7280;
  text-align: right;
}

/* Security tips */
.security-tips {
  margin-top: 24px;
  padding: 16px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
}

.security-tips h4 {
  font-size: 14px;
  font-weight: 600;
  color: #0369a1;
  margin: 0 0 8px 0;
}

.security-tips p {
  font-size: 13px;
  color: #0c4a6e;
  margin: 0;
}

.security-tips ul {
  margin: 8px 0 0 0;
  padding-left: 20px;
  font-size: 13px;
  color: #0c4a6e;
}

.security-tips li {
  margin-bottom: 4px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: #8b5cf6;
  background: white;
}

.form-textarea {
  width: 100%;
  padding: 14px 16px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
  resize: vertical;
  font-family: inherit;
}

.form-textarea:focus {
  border-color: #8b5cf6;
  background: white;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  margin-top: 24px;
}

.save-btn {
  padding: 14px 28px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(124, 58, 237, 0.5);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-group {
  display: flex;
  gap: 12px;
}

.toggle-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.toggle-btn.active {
  background: rgba(139, 92, 246, 0.1);
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.toggle-btn svg {
  width: 20px;
  height: 20px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #f9fafb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.checkbox-item:hover {
  background: #f3f4f6;
}

.checkbox-item input {
  display: none;
}

.checkmark {
  width: 22px;
  height: 22px;
  border: 2px solid #e5e7eb;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.checkbox-item input:checked + .checkmark {
  background: #8b5cf6;
  border-color: #8b5cf6;
}

.checkbox-item input:checked + .checkmark::after {
  content: '';
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-item span:last-child {
  font-size: 14px;
  color: #374151;
}

.danger-card {
  background: white;
  border-radius: 20px;
  border: 2px solid #fecaca;
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.danger-content h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.danger-content p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
}

.danger-btn {
  padding: 14px 24px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  flex-shrink: 0;
}

.danger-btn:hover {
  background: #dc2626;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 480px;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.modal-header svg {
  width: 28px;
  height: 28px;
}

.modal-header.danger svg {
  color: #ef4444;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.modal-body p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 16px;
}

.modal-body p strong {
  color: #1f2937;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
}

.cancel-btn {
  padding: 12px 24px;
  background: #f3f4f6;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.delete-btn {
  padding: 12px 24px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.delete-btn:hover:not(:disabled) {
  background: #dc2626;
}

.delete-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .settings-layout {
    grid-template-columns: 1fr;
  }

  .settings-sidebar {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
  }

  .tab-btn span {
    display: none;
  }

  .logout-section {
    margin-top: 0;
    padding-top: 0;
    border-top: none;
  }

  .danger-card {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}
</style>
