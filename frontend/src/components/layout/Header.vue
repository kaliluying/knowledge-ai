<script setup lang="ts">
import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
</script>

<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Logo -->
      <div class="logo">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <span class="logo-text">Knowledge</span>
      </div>

      <!-- User info -->
      <div class="user-section">
        <div v-if="authStore.user" class="user-info">
          <div class="user-avatar">
            <img
              v-if="authStore.user.avatar"
              :src="authStore.user.avatar"
              :alt="authStore.user.username"
            />
            <span v-else>{{ authStore.user.username?.charAt(0).toUpperCase() }}</span>
          </div>
          <span class="user-name">{{ authStore.user.username }}</span>
        </div>
        <button class="logout-btn" @click="authStore.logout()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  height: 64px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid #f3f4f6;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}

.logo-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px 6px 6px;
  background: #f8fafc;
  border-radius: 30px;
  border: 1px solid #e5e7eb;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar span {
  color: white;
  font-size: 14px;
  font-weight: 600;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.logout-btn {
  width: 40px;
  height: 40px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
}

.logout-btn:hover {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.logout-btn svg {
  width: 18px;
  height: 18px;
}
</style>
