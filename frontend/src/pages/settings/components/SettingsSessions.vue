<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';

const sessions = ref<Array<{ id: string; device: string; location: string; lastActive: string; current: boolean }>>([]);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);

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
    sessions.value = [{
      id: 'current',
      device: '当前设备',
      location: '本地',
      lastActive: new Date().toISOString(),
      current: true,
    }];
  }
};

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

onMounted(() => {
  loadSessions();
});
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

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
</template>

<style scoped src="../settings-shared.css"></style>
