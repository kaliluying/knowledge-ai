<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useCollectionsStore } from '@/stores';

const router = useRouter();
const collectionsStore = useCollectionsStore();

const url = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const handleSubmit = async () => {
  if (!url.value.trim()) {
    errorMessage.value = '请输入 URL';
    return;
  }

  // 验证 URL 格式
  try {
    new URL(url.value);
  } catch {
    errorMessage.value = '请输入有效的 URL';
    return;
  }

  errorMessage.value = '';
  isLoading.value = true;

  try {
    const result = await collectionsStore.createCollection({ url: url.value.trim() });
    if (result.success) {
      router.push(`/collections/${result.data.id}`);
    } else {
      errorMessage.value = result.message || '添加收藏失败';
    }
  } catch (error) {
    errorMessage.value = '添加收藏失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};

const presetUrls = [
  { name: 'GitHub', url: 'https://github.com' },
  { name: '知乎', url: 'https://www.zhihu.com' },
  { name: '掘金', url: 'https://juejin.cn' },
  { name: 'CSDN', url: 'https://www.csdn.net' },
];

const selectPreset = (presetUrl: string) => {
  url.value = presetUrl;
  errorMessage.value = '';
};
</script>

<template>
  <div class="add-collection-page">
    <div class="page-container">
      <button class="back-btn" @click="router.back()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
        返回
      </button>

      <div class="form-container">
        <h1>添加收藏</h1>
        <p class="subtitle">收藏你喜欢的网页内容，随时随地阅读</p>

        <form @submit.prevent="handleSubmit" class="add-form">
          <div class="form-group">
            <label for="url">网页地址</label>
            <input
              id="url"
              v-model="url"
              type="url"
              placeholder="https://example.com/article"
              class="form-input"
              :disabled="isLoading"
            />
            <p class="form-hint">输入要收藏的网页链接，系统会自动抓取标题和内容</p>
          </div>

          <div v-if="errorMessage" class="error-message">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 8v4m0 4h.01" />
            </svg>
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            class="submit-btn"
            :disabled="isLoading || !url.trim()"
          >
            <svg v-if="isLoading" class="spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" />
            </svg>
            <span v-else>添加收藏</span>
          </button>
        </form>

        <div class="preset-section">
          <p class="preset-title">快速添加</p>
          <div class="preset-list">
            <button
              v-for="preset in presetUrls"
              :key="preset.url"
              class="preset-btn"
              @click="selectPreset(preset.url)"
              :disabled="isLoading"
            >
              {{ preset.name }}
            </button>
          </div>
        </div>

        <div class="features">
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 016.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z" />
              </svg>
            </div>
            <div class="feature-text">
              <h4>智能提取</h4>
              <p>自动提取标题、描述和正文内容</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <path d="M21 15l-5-5L5 21" />
              </svg>
            </div>
            <div class="feature-text">
              <h4>封面图片</h4>
              <p>自动获取网页封面图</p>
            </div>
          </div>
          <div class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9" />
              </svg>
            </div>
            <div class="feature-text">
              <h4>离线阅读</h4>
              <p>保存内容到本地，随时离线阅读</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.add-collection-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 50%, #d1fae5 100%);
}

.page-container {
  width: 100%;
  max-width: 520px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.back-btn:hover {
  background: #f9fafb;
  color: #1f2937;
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

.form-container {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.form-container h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 15px;
  color: #9ca3af;
  margin-bottom: 32px;
}

.add-form {
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 16px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus {
  border-color: #10b981;
  background: white;
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-hint {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 8px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 20px;
}

.error-message svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.submit-btn {
  width: 100%;
  padding: 14px 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(16, 185, 129, 0.5);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinner {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.preset-section {
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
  margin-bottom: 32px;
}

.preset-title {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 12px;
}

.preset-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.preset-btn {
  padding: 10px 16px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
}

.preset-btn:hover:not(:disabled) {
  background: #10b981;
  color: white;
}

.preset-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.feature-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
  color: #059669;
}

.feature-text h4 {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.feature-text p {
  font-size: 13px;
  color: #9ca3af;
}

@media (max-width: 480px) {
  .form-container {
    padding: 24px;
  }

  .form-container h1 {
    font-size: 24px;
  }
}
</style>
