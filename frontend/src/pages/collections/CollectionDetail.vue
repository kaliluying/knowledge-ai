<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCollectionsStore } from '@/stores';

const router = useRouter();
const route = useRoute();
const collectionsStore = useCollectionsStore();

const showDeleteConfirm = ref(false);
const isDeleting = ref(false);

const collectionId = computed(() => Number(route.params.id));

const loadCollection = async () => {
  await collectionsStore.fetchCollectionDetail(collectionId.value);
};

onMounted(() => {
  loadCollection();
});

const handleRefresh = async () => {
  await collectionsStore.refreshCollection(collectionId.value);
};

const handleDelete = async () => {
  isDeleting.value = true;
  await collectionsStore.deleteCollection(collectionId.value);
  router.push('/collections');
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatSize = (wordCount: number) => {
  if (wordCount < 1000) return `${wordCount} 字`;
  return `${(wordCount / 1000).toFixed(1)}k 字`;
};

const openExternal = () => {
  if (collectionsStore.currentCollection?.url) {
    window.open(collectionsStore.currentCollection.url, '_blank');
  }
};
</script>

<template>
  <div class="collection-detail-page">
    <div v-if="collectionsStore.isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <template v-else-if="collectionsStore.currentCollection">
      <!-- Header -->
      <div class="detail-header">
        <button class="back-btn" @click="router.back()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          返回收藏列表
        </button>

        <div class="header-actions">
          <button class="action-btn" @click="handleRefresh" :disabled="collectionsStore.isLoading">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 4v6h-6" />
              <path d="M1 20v-6h6" />
              <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
            </svg>
            刷新
          </button>
          <button class="action-btn" @click="openExternal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" />
              <path d="M15 3h6v6" />
              <path d="M10 14L21 3" />
            </svg>
            访问原文
          </button>
          <button class="action-btn delete" @click="showDeleteConfirm = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
            </svg>
            删除
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="detail-content">
        <div class="content-header">
          <div class="source-info">
            <img
              v-if="collectionsStore.currentCollection.favicon"
              :src="collectionsStore.currentCollection.favicon"
              :alt="collectionsStore.currentCollection.domain"
              class="source-favicon"
              @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
            />
            <div v-else class="source-favicon-placeholder">
              {{ collectionsStore.currentCollection.domain.charAt(0).toUpperCase() }}
            </div>
            <span class="source-domain">{{ collectionsStore.currentCollection.domain }}</span>
            <span class="status-badge" :class="{ processed: collectionsStore.currentCollection.is_processed }">
              {{ collectionsStore.currentCollection.is_processed ? '已处理' : '处理中' }}
            </span>
          </div>

          <h1 class="content-title">{{ collectionsStore.currentCollection.title || '未标题' }}</h1>

          <div class="content-meta">
            <span v-if="collectionsStore.currentCollection.reading_time">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 6v6l4 2" />
              </svg>
              {{ collectionsStore.currentCollection.reading_time }} 分钟阅读
            </span>
            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                <path d="M14 2v6h6" />
              </svg>
              {{ formatSize(collectionsStore.currentCollection.word_count) }}
            </span>
            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              {{ collectionsStore.currentCollection.view_count }} 次浏览
            </span>
            <span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
              {{ formatDate(collectionsStore.currentCollection.created_at) }}
            </span>
          </div>
        </div>

        <div v-if="collectionsStore.currentCollection.image" class="cover-image">
          <img
            :src="collectionsStore.currentCollection.image"
            :alt="collectionsStore.currentCollection.title"
            @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
          />
        </div>

        <div class="content-body">
          <div v-if="collectionsStore.currentCollection.description" class="description">
            <h3>简介</h3>
            <p>{{ collectionsStore.currentCollection.description }}</p>
          </div>

          <div class="main-content">
            <h3>正文内容</h3>
            <div v-if="collectionsStore.currentCollection.content" class="text-content">
              {{ collectionsStore.currentCollection.content }}
            </div>
            <div v-else class="no-content">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p>暂无内容</p>
              <button class="refresh-btn" @click="handleRefresh">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 4v6h-6" />
                  <path d="M1 20v-6h6" />
                  <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
                </svg>
                重新抓取
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Delete Confirm Modal -->
      <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="showDeleteConfirm = false">
        <div class="modal small">
          <h2>确认删除</h2>
          <p>删除收藏后无法恢复，确定要删除吗？</p>
          <div class="modal-actions">
            <button class="cancel-btn" @click="showDeleteConfirm = false">取消</button>
            <button class="delete-btn" :disabled="isDeleting" @click="handleDelete">
              {{ isDeleting ? '删除中...' : '删除' }}
            </button>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="error-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <h3>收藏不存在</h3>
      <p>该收藏可能已被删除</p>
      <button class="back-btn-large" @click="router.push('/collections')">
        返回收藏列表
      </button>
    </div>
  </div>
</template>

<style scoped>
.collection-detail-page {
  max-width: 800px;
  margin: 0 auto;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #9ca3af;
  font-size: 15px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f9fafb;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #d1d5db;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn.delete {
  color: #dc2626;
  border-color: #fecaca;
}

.action-btn.delete:hover:not(:disabled) {
  background: #fef2f2;
  border-color: #fca5a5;
}

.detail-content {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.content-header {
  padding: 32px;
  border-bottom: 1px solid #f3f4f6;
}

.source-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.source-favicon {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  object-fit: contain;
}

.source-favicon-placeholder {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
}

.source-domain {
  font-size: 14px;
  color: #6b7280;
}

.status-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  background: #fef3c7;
  color: #d97706;
}

.status-badge.processed {
  background: #d1fae5;
  color: #059669;
}

.content-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.4;
  margin-bottom: 20px;
}

.content-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.content-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #9ca3af;
}

.content-meta svg {
  width: 16px;
  height: 16px;
}

.cover-image {
  width: 100%;
  max-height: 300px;
  overflow: hidden;
}

.cover-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.content-body {
  padding: 32px;
}

.description {
  margin-bottom: 28px;
  padding-bottom: 28px;
  border-bottom: 1px solid #f3f4f6;
}

.description h3,
.main-content h3 {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.description p {
  font-size: 15px;
  color: #4b5563;
  line-height: 1.7;
}

.text-content {
  font-size: 16px;
  color: #1f2937;
  line-height: 1.8;
  white-space: pre-wrap;
  padding: 24px;
  background: #f9fafb;
  border-radius: 12px;
}

.no-content {
  text-align: center;
  padding: 48px 24px;
  background: #f9fafb;
  border-radius: 12px;
}

.no-content svg {
  width: 48px;
  height: 48px;
  color: #d1d5db;
  margin-bottom: 16px;
}

.no-content p {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 20px;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.refresh-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  background: white;
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 440px;
}

.modal.small {
  max-width: 400px;
}

.modal h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.modal.small p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
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
  opacity: 0.6;
  cursor: not-allowed;
}

.error-state {
  text-align: center;
  padding: 80px 20px;
}

.error-state svg {
  width: 64px;
  height: 64px;
  color: #d1d5db;
  margin-bottom: 24px;
}

.error-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.error-state p {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 24px;
}

.back-btn-large {
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.back-btn-large:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
}

@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .content-header,
  .content-body {
    padding: 20px;
  }

  .content-title {
    font-size: 20px;
  }

  .content-meta {
    gap: 12px;
  }
}
</style>
