<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { authApi } from '@/api/auth';

const router = useRouter();
const authStore = useAuthStore();

const showDeleteModal = ref(false);
const deleteConfirmText = ref('');
const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);

const passwordForm = ref({
  currentPassword: ''
});

const handleDeleteAccount = async () => {
  if (deleteConfirmText.value !== authStore.user?.username) {
    message.value = { type: 'error', text: '用户名不匹配' };
    return;
  }

  isSaving.value = true;
  try {
    const password = passwordForm.value.currentPassword;
    if (!password) {
      const input = prompt("请输入密码进行确认:");
      if (!input) {
        isSaving.value = false;
        return;
      }
      passwordForm.value.currentPassword = input;
    }

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
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

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
          
          <div class="form-group" style="margin-top: 10px;">
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: modalIn 0.3s ease;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 24px 24px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-header.danger svg {
  color: #ef4444;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.modal-header svg {
  width: 28px;
  height: 28px;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  font-size: 15px;
  color: #4b5563;
  margin: 0 0 12px 0;
  line-height: 1.6;
}

.modal-actions {
  padding: 20px 24px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 10px 20px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.delete-btn {
  padding: 10px 20px;
  background: #ef4444;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.delete-btn:hover:not(:disabled) {
  background: #dc2626;
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
</style>

<style scoped src="../settings-shared.css"></style>
