<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCollectionsStore } from '@/stores';

const router = useRouter();
const collectionsStore = useCollectionsStore();

const searchQuery = ref('');
const showDeleteConfirm = ref(false);
const deletingId = ref<number | null>(null);

const loadCollections = async () => {
  await collectionsStore.fetchCollections({ page: 1 });
};

onMounted(() => {
  loadCollections();
});

const filteredCollections = computed(() => {
  if (!searchQuery.value) return collectionsStore.collections;
  const query = searchQuery.value.toLowerCase();
  return collectionsStore.collections.filter((c) =>
    c.title.toLowerCase().includes(query) ||
    c.description.toLowerCase().includes(query) ||
    c.domain.toLowerCase().includes(query)
  );
});

const handleDelete = async (id: number) => {
  await collectionsStore.deleteCollection(id);
  showDeleteConfirm.value = false;
  deletingId.value = null;
};

const openDeleteConfirm = (id: number) => {
  deletingId.value = id;
  showDeleteConfirm.value = true;
};

const formatSize = (wordCount: number) => {
  if (wordCount < 1000) return `${wordCount} 字`;
  return `${(wordCount / 1000).toFixed(1)}k 字`;
};
</script>

<template>
  <div class="collections-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>我的收藏</h1>
        <p>{{ collectionsStore.collections.length }} 个收藏</p>
      </div>
      <button class="create-btn" @click="router.push('/collections/add')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        添加收藏
      </button>
    </div>

    <!-- Search -->
    <div class="search-bar">
      <div class="search-input-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索收藏..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="collectionsStore.isLoading" class="loading-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card">
        <div class="skeleton-favicon"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-desc"></div>
      </div>
    </div>

    <!-- Collections Grid -->
    <div v-else-if="filteredCollections.length > 0" class="collections-grid">
      <div
        v-for="item in filteredCollections"
        :key="item.id"
        class="collection-card"
        @click="router.push(`/collections/${item.id}`)"
      >
        <div class="collection-header">
          <img
            v-if="item.favicon"
            :src="item.favicon"
            :alt="item.domain"
            class="collection-favicon"
            @error="(e) => (e.target as HTMLImageElement).style.display = 'none'"
          />
          <div v-else class="collection-favicon-placeholder">
            {{ item.domain.charAt(0).toUpperCase() }}
          </div>
          <span class="collection-domain">{{ item.domain }}</span>
        </div>

        <h3 class="collection-title">{{ item.title || '未标题' }}</h3>

        <p class="collection-description">
          {{ item.description || '暂无描述' }}
        </p>

        <div class="collection-footer">
          <div class="collection-meta">
            <span v-if="item.reading_time" class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 6v6l4 2" />
              </svg>
              {{ item.reading_time }} 分钟
            </span>
            <span class="meta-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                <path d="M14 2v6h6" />
                <path d="M16 13H8M16 17H8M10 9H8" />
              </svg>
              {{ formatSize(item.word_count) }}
            </span>
          </div>
          <div class="collection-status" :class="{ processed: item.is_processed }">
            {{ item.is_processed ? '已处理' : '处理中' }}
          </div>
        </div>

        <div class="collection-actions" @click.stop>
          <button
            class="action-btn"
            title="刷新"
            @click="collectionsStore.refreshCollection(item.id)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 4v6h-6" />
              <path d="M1 20v-6h6" />
              <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
            </svg>
          </button>
          <button
            class="action-btn delete"
            title="删除"
            @click="openDeleteConfirm(item.id)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
        </svg>
      </div>
      <h3>暂无收藏</h3>
      <p>添加你喜欢的网页内容到收藏夹</p>
      <button class="create-btn-small" @click="router.push('/collections/add')">
        添加收藏
      </button>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click.self="showDeleteConfirm = false">
      <div class="modal small">
        <h2>确认删除</h2>
        <p>删除收藏后无法恢复，确定要删除吗？</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showDeleteConfirm = false">取消</button>
          <button class="delete-btn" @click="handleDelete(deletingId!)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.collections-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
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

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(16, 185, 129, 0.5);
}

.create-btn svg {
  width: 18px;
  height: 18px;
}

.search-bar {
  margin-bottom: 24px;
}

.search-input-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 14px 16px 14px 52px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.skeleton-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 2px solid #e5e7eb;
}

.skeleton-favicon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  animation: skeleton 1.5s ease-in-out infinite;
  margin-bottom: 16px;
}

.skeleton-line {
  height: 18px;
  width: 80%;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  animation: skeleton 1.5s ease-in-out infinite;
}

.skeleton-desc {
  height: 14px;
  width: 100%;
  margin-top: 12px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 6px;
  animation: skeleton 1.5s ease-in-out infinite;
}

@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.collections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.collection-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.collection-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: #10b981;
}

.collection-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.collection-favicon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  object-fit: contain;
}

.collection-favicon-placeholder {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.collection-domain {
  font-size: 13px;
  color: #9ca3af;
}

.collection-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.collection-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.collection-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.collection-meta {
  display: flex;
  gap: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #9ca3af;
}

.meta-item svg {
  width: 14px;
  height: 14px;
}

.collection-status {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  background: #fef3c7;
  color: #d97706;
}

.collection-status.processed {
  background: #d1fae5;
  color: #059669;
}

.collection-actions {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.collection-card:hover .collection-actions {
  opacity: 1;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  background: #f3f4f6;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #10b981;
  color: white;
}

.action-btn.delete:hover {
  background: #ef4444;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 24px;
}

.create-btn-small {
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
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
  animation: slideUp 0.3s ease;
}

.modal.small {
  max-width: 400px;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  margin-bottom: 24px;
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

.delete-btn:hover {
  background: #dc2626;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .collections-grid {
    grid-template-columns: 1fr;
  }

  .collection-actions {
    opacity: 1;
  }
}
</style>
