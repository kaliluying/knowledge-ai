<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';

import SettingsProfile from './components/SettingsProfile.vue';
import SettingsSecurity from './components/SettingsSecurity.vue';
import SettingsPreferences from './components/SettingsPreferences.vue';
import SettingsSessions from './components/SettingsSessions.vue';
import SettingsData from './components/SettingsData.vue';
import SettingsDanger from './components/SettingsDanger.vue';

const router = useRouter();
const authStore = useAuthStore();

const activeTab = ref('profile');

const tabs = [
  { id: 'profile', label: '个人资料', icon: 'user' },
  { id: 'security', label: '账户安全', icon: 'shield' },
  { id: 'preferences', label: '偏好设置', icon: 'settings' },
  { id: 'sessions', label: '登录设备', icon: 'laptop' },
  { id: 'data', label: '数据管理', icon: 'database' },
  { id: 'danger', label: '危险区域', icon: 'danger' },
];

const switchTab = (tabId: string) => {
  activeTab.value = tabId;
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<template>
  <div class="settings-page">
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
        <SettingsProfile v-if="activeTab === 'profile'" />
        <SettingsSecurity v-if="activeTab === 'security'" />
        <SettingsPreferences v-if="activeTab === 'preferences'" />
        <SettingsSessions v-if="activeTab === 'sessions'" />
        <SettingsData v-if="activeTab === 'data'" />
        <SettingsDanger v-if="activeTab === 'danger'" />
      </div>
    </div>
  </div>
</template>

<style scoped src="./settings-shared.css"></style>
