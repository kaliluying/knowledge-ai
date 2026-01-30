<script setup lang="ts">
import { ref, onMounted } from 'vue';
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
});

// Password form
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});

// Preferences
const preferences = ref({
  theme: 'light' as 'light' | 'dark',
  language: 'zh-CN',
  emailNotifications: true,
  browserNotifications: false,
});

// UI state
const activeTab = ref('profile');
const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);
const showDeleteModal = ref(false);
const deleteConfirmText = ref('');

const tabs = [
  { id: 'profile', label: '个人资料', icon: 'user' },
  { id: 'security', label: '安全', icon: 'shield' },
  { id: 'preferences', label: '偏好设置', icon: 'settings' },
  { id: 'danger', label: '危险区域', icon: 'danger' },
];

const loadUserProfile = async () => {
  await authStore.fetchProfile();
  if (authStore.user) {
    profileForm.value = {
      username: authStore.user.username || '',
      email: authStore.user.email || '',
      bio: authStore.user.bio || '',
    };
  }
};

onMounted(() => {
  loadUserProfile();
});

const handleSaveProfile = async () => {
  isSaving.value = true;
  message.value = null;

  try {
    await authApi.updateProfile(profileForm.value);
    await authStore.fetchProfile();
    message.value = { type: 'success', text: '个人资料已更新' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch {
    message.value = { type: 'error', text: '更新失败，请稍后重试' };
  } finally {
    isSaving.value = false;
  }
};

const handleChangePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    message.value = { type: 'error', text: '两次输入的密码不一致' };
    return;
  }

  if (passwordForm.value.newPassword.length < 8) {
    message.value = { type: 'error', text: '密码长度至少8位' };
    return;
  }

  isSaving.value = true;
  message.value = null;

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    message.value = { type: 'success', text: '密码已更改' };
    passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch {
    message.value = { type: 'error', text: '密码更改失败' };
  } finally {
    isSaving.value = false;
  }
};

const handleSavePreferences = async () => {
  isSaving.value = true;
  message.value = null;

  try {
    await new Promise(resolve => setTimeout(resolve, 500));
    message.value = { type: 'success', text: '偏好设置已保存' };
    setTimeout(() => { message.value = null; }, 3000);
  } catch {
    message.value = { type: 'error', text: '保存失败' };
  } finally {
    isSaving.value = false;
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

const handleDeleteAccount = async () => {
  if (deleteConfirmText.value !== authStore.user?.username) {
    message.value = { type: 'error', text: '用户名不匹配' };
    return;
  }

  isSaving.value = true;
  try {
    // Simulate account deletion
    await new Promise(resolve => setTimeout(resolve, 1500));
    await authStore.logout();
    router.push('/login');
  } catch {
    message.value = { type: 'error', text: '账户删除失败' };
    isSaving.value = false;
  }
};

const switchTab = (tabId: string) => {
  activeTab.value = tabId;
  message.value = null;
};
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
            <p>更新你的账户信息</p>
          </div>

          <div class="form-card">
            <div class="form-group">
              <label>用户名</label>
              <input
                v-model="profileForm.username"
                type="text"
                class="form-input"
                placeholder="输入用户名"
              />
            </div>

            <div class="form-group">
              <label>邮箱</label>
              <input
                v-model="profileForm.email"
                type="email"
                class="form-input"
                placeholder="输入邮箱"
              />
            </div>

            <div class="form-group">
              <label>个人简介</label>
              <textarea
                v-model="profileForm.bio"
                class="form-textarea"
                placeholder="介绍一下你自己..."
                rows="4"
              ></textarea>
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
            <h2>安全设置</h2>
            <p>管理你的密码</p>
          </div>

          <div class="form-card">
            <div class="form-group">
              <label>当前密码</label>
              <input
                v-model="passwordForm.currentPassword"
                type="password"
                class="form-input"
                placeholder="输入当前密码"
              />
            </div>

            <div class="form-group">
              <label>新密码</label>
              <input
                v-model="passwordForm.newPassword"
                type="password"
                class="form-input"
                placeholder="输入新密码（至少8位）"
              />
            </div>

            <div class="form-group">
              <label>确认新密码</label>
              <input
                v-model="passwordForm.confirmPassword"
                type="password"
                class="form-input"
                placeholder="再次输入新密码"
              />
            </div>

            <div class="form-actions">
              <button class="save-btn" @click="handleChangePassword" :disabled="isSaving">
                <span v-if="isSaving">更改中...</span>
                <span v-else>更改密码</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Preferences Tab -->
        <div v-if="activeTab === 'preferences'" class="settings-section">
          <div class="section-header">
            <h2>偏好设置</h2>
            <p>自定义你的使用体验</p>
          </div>

          <div class="form-card">
            <div class="form-group">
              <label>主题</label>
              <div class="toggle-group">
                <button
                  class="toggle-btn"
                  :class="{ active: preferences.theme === 'light' }"
                  @click="preferences.theme = 'light'"
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
                  @click="preferences.theme = 'dark'"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
                  </svg>
                  深色
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
              <label>通知设置</label>
              <div class="checkbox-group">
                <label class="checkbox-item">
                  <input type="checkbox" v-model="preferences.emailNotifications" />
                  <span class="checkmark"></span>
                  <span>邮件通知</span>
                </label>
                <label class="checkbox-item">
                  <input type="checkbox" v-model="preferences.browserNotifications" />
                  <span class="checkmark"></span>
                  <span>浏览器通知</span>
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
