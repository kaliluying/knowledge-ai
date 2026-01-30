<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useTagsStore } from '@/stores';
import type { Tag } from '@/types';

const tagsStore = useTagsStore();

const searchQuery = ref('');
const showCreateModal = ref(false);
const editingTag = ref<Tag | null>(null);
const deleteConfirmId = ref<number | null>(null);
const bulkCreateText = ref('');

const newTag = ref({
  name: '',
  color: '#8b5cf6',
});

const colorOptions = [
  '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
  '#06b6d4', '#6366f1', '#ef4444', '#84cc16'
];

const loadTags = async () => {
  await tagsStore.fetchTags();
};

onMounted(() => {
  loadTags();
});

const filteredTags = computed(() => {
  if (!searchQuery.value) return tagsStore.tags;
  const query = searchQuery.value.toLowerCase();
  return tagsStore.tags.filter(tag =>
    tag.name.toLowerCase().includes(query)
  );
});

const handleCreateTag = async () => {
  if (!newTag.value.name.trim()) return;
  await tagsStore.createTag({
    name: newTag.value.name,
    color: newTag.value.color,
  });
  showCreateModal.value = false;
  newTag.value = { name: '', color: '#8b5cf6' };
};

const handleBulkCreateTags = async () => {
  if (!bulkCreateText.value.trim()) return;
  const names = bulkCreateText.value
    .split(',')
    .map(name => name.trim())
    .filter(name => name.length > 0);

  if (names.length === 0) return;

  await tagsStore.bulkCreateTags(names);
  showCreateModal.value = false;
  bulkCreateText.value = '';
};

const handleUpdateTag = async () => {
  if (!editingTag.value) return;
  await tagsStore.updateTag(editingTag.value.id, {
    name: editingTag.value.name,
    color: editingTag.value.color,
  });
  editingTag.value = null;
};

const handleDeleteTag = async (id: number) => {
  await tagsStore.deleteTag(id);
  deleteConfirmId.value = null;
};

const openEditModal = (tag: Tag) => {
  editingTag.value = { ...tag };
};
</script>

<template>
  <div class="tags-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>标签管理</h1>
        <p>{{ tagsStore.tags.length }} 个标签</p>
      </div>
      <button class="create-btn" @click="showCreateModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        新建标签
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
          placeholder="搜索标签..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="tagsStore.isLoading" class="loading-grid">
      <div v-for="n in 8" :key="n" class="skeleton-card">
        <div class="skeleton-line"></div>
        <div class="skeleton-count"></div>
      </div>
    </div>

    <!-- Tags Grid -->
    <div v-else-if="filteredTags.length > 0" class="tags-grid">
      <div
        v-for="tag in filteredTags"
        :key="tag.id"
        class="tag-card"
      >
        <div class="tag-header">
          <div class="tag-color" :style="{ background: tag.color }"></div>
          <span class="tag-name">{{ tag.name }}</span>
        </div>

        <div class="tag-footer">
          <span class="tag-count">{{ tag.usage_count || 0 }} 篇笔记</span>
          <div class="tag-actions">
            <button class="action-btn" @click="openEditModal(tag)" title="编辑">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
              </svg>
            </button>
            <button class="action-btn delete" @click="deleteConfirmId = tag.id" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
      </div>
      <h3>暂无标签</h3>
      <p>创建标签来组织你的笔记</p>
      <button class="create-btn-small" @click="showCreateModal = true">
        新建标签
      </button>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h2>新建标签</h2>

        <!-- Single Tag Creation -->
        <div class="form-group">
          <label>标签名称</label>
          <input
            v-model="newTag.name"
            type="text"
            placeholder="输入标签名称"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>颜色</label>
          <div class="color-picker">
            <button
              v-for="color in colorOptions"
              :key="color"
              class="color-option"
              :class="{ active: newTag.color === color }"
              :style="{ background: color }"
              @click="newTag.color = color"
            ></button>
          </div>
        </div>

        <div class="bulk-create-section">
          <div class="divider">
            <span>或批量创建</span>
          </div>

          <div class="form-group">
            <label>多个标签（用逗号分隔）</label>
            <textarea
              v-model="bulkCreateText"
              placeholder="标签1, 标签2, 标签3"
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
        </div>

        <div class="modal-actions">
          <button class="cancel-btn" @click="showCreateModal = false">取消</button>
          <button
            v-if="newTag.name.trim()"
            class="submit-btn"
            @click="handleCreateTag"
          >
            创建
          </button>
          <button
            v-else-if="bulkCreateText.trim()"
            class="submit-btn"
            @click="handleBulkCreateTags"
          >
            批量创建
          </button>
          <button v-else class="submit-btn disabled" disabled>
            创建
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingTag" class="modal-overlay" @click.self="editingTag = null">
      <div class="modal">
        <h2>编辑标签</h2>
        <div class="form-group">
          <label>名称</label>
          <input
            v-model="editingTag.name"
            type="text"
            placeholder="输入标签名称"
            class="form-input"
          />
        </div>
        <div class="form-group">
          <label>颜色</label>
          <div class="color-picker">
            <button
              v-for="color in colorOptions"
              :key="color"
              class="color-option"
              :class="{ active: editingTag.color === color }"
              :style="{ background: color }"
              @click="editingTag.color = color"
            ></button>
          </div>
        </div>
        <div class="modal-actions">
          <button class="cancel-btn" @click="editingTag = null">取消</button>
          <button class="submit-btn" @click="handleUpdateTag">保存</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirm -->
    <div v-if="deleteConfirmId" class="modal-overlay" @click.self="deleteConfirmId = null">
      <div class="modal small">
        <h2>确认删除</h2>
        <p>删除标签后，所有笔记中的该标签将被移除。此操作不可撤销。</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="deleteConfirmId = null">取消</button>
          <button class="delete-btn" @click="handleDeleteTag(deleteConfirmId!)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tags-page {
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
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(124, 58, 237, 0.5);
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
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.skeleton-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 2px solid #e5e7eb;
}

.skeleton-line {
  height: 20px;
  width: 60%;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  animation: skeleton 1.5s ease-in-out infinite;
}

.skeleton-count {
  height: 14px;
  width: 40%;
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

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.tag-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
}

.tag-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: #8b5cf6;
}

.tag-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.tag-color {
  width: 16px;
  height: 16px;
  border-radius: 6px;
  flex-shrink: 0;
}

.tag-name {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.tag-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tag-count {
  font-size: 13px;
  color: #9ca3af;
}

.tag-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.tag-card:hover .tag-actions {
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
  background: #8b5cf6;
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
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(219, 39, 119, 0.3);
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
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
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
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
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
  margin-bottom: 24px;
}

.modal.small h2 {
  margin-bottom: 12px;
}

.modal.small p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
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
  padding: 12px 16px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
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
  padding: 12px 16px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
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

.color-picker {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 3px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #1f2937;
}

.bulk-create-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e5e7eb;
}

.divider span {
  font-size: 13px;
  color: #9ca3af;
  white-space: nowrap;
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

.submit-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.submit-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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

  .tags-grid {
    grid-template-columns: 1fr;
  }

  .tag-actions {
    opacity: 1;
  }
}
</style>
