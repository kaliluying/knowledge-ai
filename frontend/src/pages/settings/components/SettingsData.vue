<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';

const storageStats = ref({
  notes_count: 0,
  notes_size: 0,
  attachments_count: 0,
  attachments_size: 0,
  images_count: 0,
  images_size: 0,
  total_size: 0,
});

const isSaving = ref(false);
const message = ref<{ type: 'success' | 'error'; text: string } | null>(null);

const loadStorageStats = async () => {
  try {
    const response = await authApi.getStorage();
    if (response?.data) {
      storageStats.value = response.data as typeof storageStats.value;
    }
  } catch {
    //
  }
};

const handleExportData = async () => {
  isSaving.value = true;
  try {
    const response = await authApi.exportData();
    if (response?.data) {
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

onMounted(() => {
  loadStorageStats();
});
</script>

<template>
  <div class="settings-section">
    <div v-if="message" class="message" :class="message.type">
      {{ message.text }}
    </div>

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
</template>

<style scoped src="../settings-shared.css"></style>
