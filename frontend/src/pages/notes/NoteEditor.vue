<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useNotesStore, useCategoriesStore, useTagsStore } from '@/stores';
import MarkdownEditor from '@/components/editor/MarkdownEditor.vue';
import type { CreateNoteParams, UpdateNoteParams } from '@/types';

const router = useRouter();
const route = useRoute();
const notesStore = useNotesStore();
const categoriesStore = useCategoriesStore();
const tagsStore = useTagsStore();

const isEditing = computed(() => route.name === 'NoteEdit' || route.path.includes('/edit'));
const noteId = computed(() => (isEditing.value ? parseInt(route.params.id as string) : null));

const title = ref('');
const content = ref('');
const selectedCategoryId = ref<number | null>(null);
const selectedTagIds = ref<number[]>([]);
const isPinned = ref(false);
const isSaving = ref(false);
const error = ref('');
const isLoading = ref(false);

// Category dropdown state
const categoryDropdownOpen = ref(false);
const categorySearchQuery = ref('');
const categoryDropdownRef = ref<HTMLDivElement | null>(null);

// Tag input state
const tagInputRef = ref<HTMLInputElement | null>(null);
const tagSearchQuery = ref('');
const tagDropdownOpen = ref(false);
const tagDropdownRef = ref<HTMLDivElement | null>(null);
const newlyAddedTag = ref('');

// Load categories and tags
onMounted(async () => {
  isLoading.value = true;
  try {
    await Promise.all([
      categoriesStore.fetchCategoryTree(),
      tagsStore.fetchTags(),
    ]);
  } finally {
    isLoading.value = false;
  }

  // If editing, load note
  if (isEditing.value && noteId.value) {
    isLoading.value = true;
    try {
      const note = await notesStore.fetchNoteDetail(noteId.value);
      if (note) {
        title.value = note.title;
        content.value = note.content || [];
        selectedCategoryId.value = note.category_id;
        selectedTagIds.value = note.tag_ids || [];
        isPinned.value = note.is_pinned;
      }
    } catch (e) {
      error.value = '加载笔记失败';
    } finally {
      isLoading.value = false;
    }
  }

  // 添加全局点击监听器
  document.addEventListener('click', handleGlobalClick);
});

// 全局点击处理 - 关闭下拉框
const handleGlobalClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement;

  // 检查分类下拉框
  if (categoryDropdownRef.value && !categoryDropdownRef.value.contains(target)) {
    categoryDropdownOpen.value = false;
  }

  // 检查标签下拉框
  if (tagDropdownRef.value && !tagDropdownRef.value.contains(target)) {
    tagDropdownOpen.value = false;
  }
};

// 卸载时移除监听器
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick);
});

// Flatten categories for display
const categoryOptions = computed(() => {
  const flatten = (nodes: any[]): any[] => {
    return nodes.reduce((acc, node) => {
      acc.push({ id: node.id, name: node.name, depth: node.depth });
      if (node.children) {
        acc.push(...flatten(node.children));
      }
      return acc;
    }, []);
  };
  return flatten(categoriesStore.categoryTree || []);
});

// Filtered categories based on search
const filteredCategories = computed(() => {
  if (!categorySearchQuery.value.trim()) {
    return categoryOptions.value;
  }
  const query = categorySearchQuery.value.toLowerCase();
  return categoryOptions.value.filter(
    cat => cat.name.toLowerCase().includes(query)
  );
});

const availableTags = computed(() => tagsStore.tags || []);

// Filter tags for dropdown
const filteredTags = computed(() => {
  const query = tagSearchQuery.value.toLowerCase();
  const selected = selectedTagIds.value;
  return availableTags.value.filter(tag => {
    const matchesSearch = tag.name.toLowerCase().includes(query);
    const notSelected = !selected.includes(tag.id);
    const notNewlyAdded = tag.name !== newlyAddedTag.value;
    return matchesSearch && notSelected && notNewlyAdded;
  });
});

// Get selected tag objects
const selectedTags = computed(() => {
  return availableTags.value.filter(tag => selectedTagIds.value.includes(tag.id));
});

// Get category name by ID
const getCategoryName = (id: number | null) => {
  if (!id) return '选择分类';
  const cat = categoryOptions.value.find(c => c.id === id);
  return cat ? cat.name : '选择分类';
};

// Category handlers
const selectCategory = (catId: number | null) => {
  selectedCategoryId.value = catId;
  categoryDropdownOpen.value = false;
  categorySearchQuery.value = '';
};

const toggleCategoryDropdown = () => {
  categoryDropdownOpen.value = !categoryDropdownOpen.value;
  if (categoryDropdownOpen.value) {
    categorySearchQuery.value = '';
  }
};

// Tag handlers
const addTag = (tagId: number) => {
  if (!selectedTagIds.value.includes(tagId)) {
    selectedTagIds.value.push(tagId);
  }
  tagSearchQuery.value = '';
  tagDropdownOpen.value = false;
};

const addNewTag = () => {
  const name = tagSearchQuery.value.trim();
  if (name && !selectedTags.value.some(t => t.name === name) && !availableTags.value.some(t => t.name === name)) {
    selectedTagIds.value.push(-1); // -1 indicates a new tag
    newlyAddedTag.value = name;
  }
  tagSearchQuery.value = '';
  tagDropdownOpen.value = false;
};

const removeTag = (index: number) => {
  const tag = selectedTags.value[index];
  if (tag) {
    selectedTagIds.value.splice(selectedTagIds.value.indexOf(tag.id), 1);
  } else {
    // It's a newly added tag
    selectedTagIds.value.splice(index, 1);
    newlyAddedTag.value = '';
  }
};

const handleTagInputFocus = () => {
  tagDropdownOpen.value = true;
  tagSearchQuery.value = '';
};

watch(tagDropdownOpen, (isOpen) => {
  if (isOpen) {
    nextTick(() => tagInputRef.value?.focus());
  }
});

// Save handlers
const handleSave = async () => {
  if (!title.value.trim()) {
    error.value = '请输入标题';
    return;
  }

  if (!content.value.trim()) {
    error.value = '请输入内容';
    return;
  }

  isSaving.value = true;
  error.value = '';

  try {
    const data: CreateNoteParams | UpdateNoteParams = {
      title: title.value,
      content: content.value,
      category_id: selectedCategoryId.value || undefined,
      tag_ids: selectedTagIds.value.length > 0 ? selectedTagIds.value.filter(id => id !== -1) : undefined,
      is_pinned: isPinned.value,
    };

    if (isEditing.value && noteId.value) {
      await notesStore.updateNote(noteId.value, data as UpdateNoteParams);
      router.replace(`/notes/${noteId.value}`);
    } else {
      const result = await notesStore.createNote(data as CreateNoteParams);
      if (result.success) {
        router.push('/notes');
      } else {
        error.value = result.message || '创建笔记失败';
      }
    }
  } catch (e) {
    error.value = isEditing.value ? '更新笔记失败' : '创建笔记失败';
  } finally {
    isSaving.value = false;
  }
};

const handleCancel = () => {
  if (isEditing.value && noteId.value) {
    router.replace(`/notes/${noteId.value}`);
  } else {
    router.push('/notes');
  }
};
</script>

<script lang="ts">
import { nextTick } from 'vue';
</script>

<template>
  <div class="editor-page">
    <!-- Loading -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Editor form -->
    <div v-else class="editor-content">
      <!-- Header -->
      <div class="editor-header">
        <button class="back-btn" @click="handleCancel">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 18L18 6M6 6l12 12" />
          </svg>
          取消
        </button>
        <div class="header-actions">
          <button
            class="action-btn icon-btn"
            :class="{ active: isPinned }"
            @click="isPinned = !isPinned"
            title="置顶"
          >
            <svg v-if="isPinned" class="icon filled" viewBox="0 0 24 24" fill="currentColor">
              <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            <svg v-else class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
          <button class="action-btn primary" @click="handleSave" :disabled="isSaving">
            <svg v-if="isSaving" class="spinner-small" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" opacity="0.25"/>
              <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <span v-else>{{ isEditing ? '保存' : '发布' }}</span>
          </button>
        </div>
      </div>

      <!-- Error message -->
      <div v-if="error" class="error-message">
        <span class="error-icon">!</span>
        <span>{{ error }}</span>
      </div>

      <!-- Title -->
      <input
        v-model="title"
        type="text"
        placeholder="笔记标题"
        class="title-input"
      />

      <!-- Category and Tags -->
      <div class="meta-row">
        <!-- Category Dropdown -->
        <div class="meta-item category-wrapper" ref="categoryDropdownRef" @click.stop>
          <label>分类</label>
          <div class="custom-select" @click="toggleCategoryDropdown">
            <span class="select-value">{{ getCategoryName(selectedCategoryId) }}</span>
            <svg class="select-arrow" :class="{ open: categoryDropdownOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6" />
            </svg>
          </div>
          <div v-if="categoryDropdownOpen" class="dropdown-menu">
            <div class="dropdown-search">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8" />
                <path d="M21 21l-4.35-4.35" />
              </svg>
              <input
                v-model="categorySearchQuery"
                type="text"
                placeholder="搜索分类..."
                class="dropdown-search-input"
              />
            </div>
            <div class="dropdown-options">
              <div
                class="dropdown-option"
                :class="{ active: selectedCategoryId === null }"
                @click="selectCategory(null)"
              >
                <span>无分类</span>
              </div>
              <div
                v-for="cat in filteredCategories"
                :key="cat.id"
                class="dropdown-option"
                :class="{ active: selectedCategoryId === cat.id }"
                @click="selectCategory(cat.id)"
              >
                <span class="indent" :style="{ width: `${cat.depth * 16}px` }"></span>
                {{ cat.name }}
              </div>
            </div>
          </div>
        </div>

        <!-- Tags Input -->
        <div class="meta-item tags-item tags-wrapper" ref="tagDropdownRef" @click.stop>
          <label>标签</label>
          <div class="tags-input-container">
            <div class="tags-display">
              <span
                v-for="(tag, index) in selectedTags"
                :key="'selected-' + tag.id"
                class="tag-pill selected"
              >
                {{ tag.name }}
                <button class="tag-remove" @click.stop="removeTag(index)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
              <span
                v-if="selectedTagIds.some(id => id === -1)"
                class="tag-pill selected new-tag"
              >
                {{ newlyAddedTag }}
                <button class="tag-remove" @click.stop="removeTag(selectedTags.length)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
              <input
                ref="tagInputRef"
                v-model="tagSearchQuery"
                type="text"
                placeholder="添加标签..."
                class="tag-input"
                @focus="handleTagInputFocus"
                @keydown.enter="addNewTag"
              />
            </div>
            <div v-if="tagDropdownOpen" class="tags-dropdown">
              <div class="dropdown-search">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
                <input
                  v-model="tagSearchQuery"
                  type="text"
                  placeholder="搜索标签..."
                  class="dropdown-search-input"
                />
              </div>
              <div class="dropdown-options">
                <div
                  v-for="tag in filteredTags"
                  :key="tag.id"
                  class="dropdown-option"
                  @click="addTag(tag.id)"
                >
                  {{ tag.name }}
                </div>
                <div
                  v-if="tagSearchQuery.trim() && !availableTags.some(t => t.name === tagSearchQuery.trim())"
                  class="dropdown-option new"
                  @click="addNewTag"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 5v14M5 12h14" />
                  </svg>
                  创建 "{{ tagSearchQuery.trim() }}"
                </div>
                <div v-if="filteredTags.length === 0 && !tagSearchQuery.trim()" class="dropdown-empty">
                  所有标签已添加
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Editor -->
      <MarkdownEditor
        v-model="content"
        placeholder="开始书写你的笔记...（支持 Markdown 语法）"
        class="editor-wrapper"
      />
    </div>
  </div>
</template>

<style scoped>
.editor-page {
  max-width: 900px;
  margin: 0 auto;
}

/* Loading */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #9ca3af;
  font-size: 14px;
}

/* Editor content */
.editor-content {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.08);
}

/* Editor header */
.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f8fafc;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f1f5f9;
  color: #1f2937;
}

.back-btn .icon {
  width: 18px;
  height: 18px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn .icon {
  width: 18px;
  height: 18px;
}

.action-btn.icon-btn {
  padding: 10px;
  background: #f8fafc;
  color: #6b7280;
}

.action-btn.icon-btn:hover {
  background: #f1f5f9;
  color: #1f2937;
}

.action-btn.icon-btn.active {
  background: #fef3c7;
  color: #d97706;
}

.action-btn.icon-btn .icon.filled {
  color: #d97706;
}

.action-btn.primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(124, 58, 237, 0.5);
}

.action-btn.primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner-small {
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

/* Error message */
.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 20px;
}

.error-icon {
  width: 20px;
  height: 20px;
  background: #dc2626;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
}

/* Title input */
.title-input {
  width: 100%;
  padding: 16px 0;
  background: transparent;
  border: none;
  border-bottom: 2px solid #f3f4f6;
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
  margin-bottom: 24px;
}

.title-input:focus {
  border-bottom-color: #8b5cf6;
}

.title-input::placeholder {
  color: #d1d5db;
}

/* Meta row */
.meta-row {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f3f4f6;
}

.meta-item {
  flex: 1;
}

.meta-item > label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 8px;
}

/* Custom Select */
.custom-select {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #f8fafc;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #1f2937;
  cursor: pointer;
  transition: all 0.2s;
}

.custom-select:hover {
  border-color: #d1d5db;
}

.custom-select .select-value {
  flex: 1;
}

.custom-select .select-arrow {
  width: 16px;
  height: 16px;
  color: #9ca3af;
  transition: transform 0.2s;
}

.custom-select .select-arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
  z-index: 100;
  max-height: 280px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.category-wrapper {
  position: relative;
  min-width: 200px;
}

.dropdown-search {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #9ca3af;
  flex-shrink: 0;
}

.dropdown-search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #1f2937;
}

.dropdown-search-input::placeholder {
  color: #9ca3af;
}

.dropdown-options {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.dropdown-option {
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
}

.dropdown-option:hover {
  background: #f8fafc;
}

.dropdown-option.active {
  background: rgba(139, 92, 246, 0.1);
  color: #7c3aed;
}

.dropdown-option .indent {
  display: inline-block;
}

.dropdown-option.new {
  color: #8b5cf6;
}

.dropdown-option.new svg {
  width: 16px;
  height: 16px;
  margin-right: 6px;
}

.dropdown-empty {
  padding: 20px;
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
}

/* Tags */
.tags-item {
  flex: 2;
}

.tags-wrapper {
  position: relative;
}

.tags-input-container {
  background: #f8fafc;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  padding: 8px 12px;
  transition: all 0.2s;
}

.tags-input-container:focus-within {
  border-color: #8b5cf6;
  background: white;
}

.tags-display {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #ede9fe;
  color: #7c3aed;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.tag-pill.new-tag {
  background: #dcfce7;
  color: #16a34a;
}

.tag-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  padding: 0;
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.15s;
}

.tag-remove:hover {
  opacity: 1;
}

.tag-remove svg {
  width: 12px;
  height: 12px;
}

.tag-input {
  flex: 1;
  min-width: 120px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #374151;
  background: transparent;
  padding: 4px 0;
}

.tag-input::placeholder {
  color: #9ca3af;
}

.tags-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
  z-index: 100;
  max-height: 280px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Editor wrapper */
.editor-wrapper {
  min-height: 500px;
  border-radius: 16px;
  overflow: hidden;
  margin-top: 24px;
}

/* Responsive */
@media (max-width: 768px) {
  .editor-content {
    padding: 20px;
  }

  .title-input {
    font-size: 24px;
  }

  .meta-row {
    flex-direction: column;
    gap: 16px;
  }

  .editor-wrapper {
    min-height: 400px;
  }
}
</style>
