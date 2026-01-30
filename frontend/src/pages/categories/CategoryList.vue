<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useCategoriesStore } from '@/stores';
import type { CategoryTreeItem } from '@/types';

const categoriesStore = useCategoriesStore();

const searchQuery = ref('');
const showCreateModal = ref(false);
const editingCategory = ref<CategoryTreeItem | null>(null);
const deleteConfirmId = ref<number | null>(null);

const newCategory = ref({
  name: '',
  color: '#8b5cf6',
  parent_id: null as number | null,
});

const colorOptions = [
  '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
  '#06b6d4', '#6366f1', '#ef4444', '#84cc16'
];

const loadCategories = async () => {
  await categoriesStore.fetchCategoryTree();
};

onMounted(() => {
  loadCategories();
});

const filteredTree = computed(() => {
  if (!searchQuery.value) return categoriesStore.categoryTree;
  const query = searchQuery.value.toLowerCase();
  return filterTree(categoriesStore.categoryTree, query);
});

const filterTree = (nodes: CategoryTreeItem[], query: string): CategoryTreeItem[] => {
  return nodes.filter(node => {
    const matches = node.name.toLowerCase().includes(query);
    if (node.children && node.children.length > 0) {
      node.children = filterTree(node.children, query);
    }
    return matches || (node.children && node.children.length > 0);
  });
};

const handleCreateCategory = async () => {
  if (!newCategory.value.name.trim()) return;
  await categoriesStore.createCategory({
    name: newCategory.value.name,
    color: newCategory.value.color,
    parent_id: newCategory.value.parent_id ?? undefined,
  });
  showCreateModal.value = false;
  newCategory.value = { name: '', color: '#8b5cf6', parent_id: null };
};

const handleUpdateCategory = async () => {
  if (!editingCategory.value) return;
  await categoriesStore.updateCategory(editingCategory.value.id, {
    name: editingCategory.value.name,
    color: editingCategory.value.color,
  });
  editingCategory.value = null;
};

const handleDeleteCategory = async (id: number) => {
  await categoriesStore.deleteCategory(id);
  deleteConfirmId.value = null;
};

const openEditModal = (category: CategoryTreeItem) => {
  editingCategory.value = { ...category };
};

const getTreeDepth = (category: CategoryTreeItem): number => {
  if (!category.children || category.children.length === 0) return 0;
  return 1 + Math.max(...category.children.map(getTreeDepth));
};
</script>

<template>
  <div class="categories-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>分类管理</h1>
        <p>{{ categoriesStore.categoryTree.length }} 个分类</p>
      </div>
      <button class="create-btn" @click="showCreateModal = true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        新建分类
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
          placeholder="搜索分类..."
          class="search-input"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="categoriesStore.isLoading" class="loading">
      <div v-for="n in 4" :key="n" class="skeleton-item">
        <div class="skeleton-line"></div>
      </div>
    </div>

    <!-- Categories Tree -->
    <div v-else-if="filteredTree.length > 0" class="categories-tree">
      <div
        v-for="category in filteredTree"
        :key="category.id"
        class="category-node"
        :style="{ paddingLeft: `${20 + getTreeDepth(category) * 24}px` }"
      >
        <div class="category-content">
          <div class="category-color" :style="{ background: category.color }"></div>
          <span class="category-name">{{ category.name }}</span>
          <span class="category-count">{{ category.notes_count || 0 }} 篇</span>
          <div class="category-actions">
            <button class="action-btn" @click="openEditModal(category)" title="编辑">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
              </svg>
            </button>
            <button class="action-btn delete" @click="deleteConfirmId = category.id" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Children -->
        <div v-if="category.children && category.children.length > 0" class="children">
          <div
            v-for="child in category.children"
            :key="child.id"
            class="category-node child"
            :style="{ paddingLeft: '60px' }"
          >
            <div class="category-content">
              <div class="category-color" :style="{ background: child.color }"></div>
          <span class="category-name">{{ child.name }}</span>
          <span class="category-count">{{ child.notes_count || 0 }} 篇</span>
              <div class="category-actions">
                <button class="action-btn" @click="openEditModal(child)" title="编辑">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                  </svg>
                </button>
                <button class="action-btn delete" @click="deleteConfirmId = child.id" title="删除">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                  </svg>
                </button>
              </div>
            </div>
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
      <h3>暂无分类</h3>
      <p>创建分类来组织你的笔记</p>
      <button class="create-btn-small" @click="showCreateModal = true">
        新建分类
      </button>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h2>新建分类</h2>
        <div class="form-group">
          <label>名称</label>
          <input
            v-model="newCategory.name"
            type="text"
            placeholder="输入分类名称"
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
              :class="{ active: newCategory.color === color }"
              :style="{ background: color }"
              @click="newCategory.color = color"
            ></button>
          </div>
        </div>
        <div class="form-group">
          <label>父分类（可选）</label>
          <select v-model="newCategory.parent_id" class="form-input">
            <option :value="null">无（顶级分类）</option>
            <option v-for="cat in categoriesStore.categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showCreateModal = false">取消</button>
          <button class="submit-btn" @click="handleCreateCategory">创建</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingCategory" class="modal-overlay" @click.self="editingCategory = null">
      <div class="modal">
        <h2>编辑分类</h2>
        <div class="form-group">
          <label>名称</label>
          <input
            v-model="editingCategory.name"
            type="text"
            placeholder="输入分类名称"
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
              :class="{ active: editingCategory.color === color }"
              :style="{ background: color }"
              @click="editingCategory.color = color"
            ></button>
          </div>
        </div>
        <div class="modal-actions">
          <button class="cancel-btn" @click="editingCategory = null">取消</button>
          <button class="submit-btn" @click="handleUpdateCategory">保存</button>
        </div>
      </div>
    </div>

    <!-- Delete Confirm -->
    <div v-if="deleteConfirmId" class="modal-overlay" @click.self="deleteConfirmId = null">
      <div class="modal small">
        <h2>确认删除</h2>
        <p>删除分类后，该分类下的笔记将变为未分类状态。此操作不可撤销。</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="deleteConfirmId = null">取消</button>
          <button class="delete-btn" @click="handleDeleteCategory(deleteConfirmId!)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.categories-page {
  max-width: 900px;
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

.loading {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-item {
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  border: 2px solid #e5e7eb;
}

.skeleton-line {
  height: 20px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  animation: skeleton 1.5s ease-in-out infinite;
}

.categories-tree {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-node {
  background: white;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.2s;
}

.category-node:hover {
  border-color: #8b5cf6;
}

.category-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
}

.category-color {
  width: 12px;
  height: 12px;
  border-radius: 4px;
  flex-shrink: 0;
}

.category-name {
  flex: 1;
  font-weight: 500;
  color: #1f2937;
}

.category-count {
  font-size: 13px;
  color: #9ca3af;
}

.category-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.category-node:hover .category-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
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
  width: 16px;
  height: 16px;
}

.children {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 20px 16px;
}

.category-node.child {
  margin-left: 20px;
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(217, 119, 6, 0.3);
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

  .category-actions {
    opacity: 1;
  }
}
</style>
