<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores';
import { authApi } from '@/api/auth';

const authStore = useAuthStore();

const profileForm = ref({
  username: '',
  email: '',
  bio: '',
  avatar: '',
});

const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);
const avatarFile = ref<File | null>(null);
const avatarPreview = ref('');

const loadUserProfile = async () => {
  if (!authStore.user) {
    await authStore.fetchProfile();
  }
  if (authStore.user) {
    profileForm.value = {
      username: authStore.user.username || '',
      email: authStore.user.email || '',
      bio: authStore.user.bio || '',
      avatar: authStore.user.avatar || '',
    };
  }
};

const handleAvatarChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];
    if (file.size > 2 * 1024 * 1024) {
      message.value = { type: 'error', text: '头像大小不能超过2MB' };
      return;
    }
    avatarFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      avatarPreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const handleSaveProfile = async () => {
  isSaving.value = true;
  message.value = null;

  try {
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

onMounted(() => {
  loadUserProfile();
});
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

    <div class="section-header">
      <h2>个人资料</h2>
      <p>更新你的账户信息和头像</p>
    </div>

    <div class="form-card">
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
</template>

<style scoped src="../settings-shared.css"></style>
