<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import type { Category, CategoryTreeItem } from '@/types';
import { useCategoriesStore } from '@/stores/categories';
import { useModal } from '@/composables/useModal';

interface Props {
  modelValue: number | null;
  placeholder?: string;
  disabled?: boolean;
  clearable?: boolean;
  showTree?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '选择分类',
  disabled: false,
  clearable: true,
  showTree: true,
});

const emit = defineEmits<{
  'update:modelValue': [value: number | null];
  change: [category: Category | null];
}>();

const categoriesStore = useCategoriesStore();
const { open, close, isOpen } = useModal();

const searchQuery = ref('');
const selectedCategory = ref<Category | null>(null);

const categoryTree = computed(() => categoriesStore.categoryTree);

const flatCategories = computed(() => {
  const result: Category[] = [];
  const traverse = (nodes: CategoryTreeItem[]) => {
    for (const node of nodes) {
      result.push(node as unknown as Category);
      if (node.children && node.children.length > 0) {
        traverse(node.children);
      }
    }
  };
  traverse(categoryTree.value);
  return result;
});

const filteredCategories = computed(() => {
  if (!searchQuery.value) return flatCategories.value;
  const query = searchQuery.value.toLowerCase();
  return flatCategories.value.filter(c =>
    c.name.toLowerCase().includes(query)
  );
});

watch(modelValue, async (newId) => {
  if (newId) {
    await fetchCategoryDetail(newId);
  } else {
    selectedCategory.value = null;
  }
}, { immediate: true });

async function fetchCategoryDetail(id: number) {
  try {
    const response = await categoriesStore.fetchCategoryDetail(id);
    selectedCategory.value = response;
  } catch {
    selectedCategory.value = null;
  }
}

function openSelector() {
  if (!props.disabled) {
    searchQuery.value = '';
    open('category-select');
  }
}

function closeSelector() {
  close('category-select');
}

function selectCategory(category: Category) {
  emit('update:modelValue', category.id);
  emit('change', category);
  selectedCategory.value = category;
  closeSelector();
}

function clearSelection(e: Event) {
  e.stopPropagation();
  emit('update:modelValue', null);
  emit('change', null);
  selectedCategory.value = null;
}

function getCategoryPath(category: Category): string {
  // 简化版本，只显示名称
  return category.name;
}

onMounted(async () => {
  await categoriesStore.fetchCategoryTree();
});
</script>

<template>
  <div class="category-select">
    <!-- 已选分类显示 -->
    <div
      class="selected-display"
      :class="{ disabled }"
      @click="openSelector"
    >
      <span v-if="selectedCategory" class="selected-name">
        <span class="category-icon" :style="{ color: selectedCategory.color }">
          {{ selectedCategory.icon || '📁' }}
        </span>
        {{ selectedCategory.name }}
      </span>
      <span v-else class="placeholder">{{ placeholder }}</span>

      <div class="select-actions">
        <button
          v-if="clearable && selectedCategory"
          class="clear-btn"
          @click="clearSelection"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
        <svg class="dropdown-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 9l6 6 6-6" />
        </svg>
      </div>
    </div>

    <!-- 分类选择弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="isOpen('category-select')" class="modal-overlay" @click.self="closeSelector">
          <div class="selector-modal">
            <div class="modal-header">
              <h3>选择分类</h3>
              <button class="close-btn" @click="closeSelector">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- 搜索框 -->
            <div class="search-wrapper">
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

            <!-- 分类列表 -->
            <div class="category-list">
              <div
                v-for="category in filteredCategories"
                :key="category.id"
                class="category-item"
                :class="{ selected: category.id === modelValue }"
                @click="selectCategory(category)"
              >
                <span class="category-icon" :style="{ color: category.color }">
                  {{ category.icon || '📁' }}
                </span>
                <span class="category-name">{{ category.name }}</span>
              </div>

              <div v-if="filteredCategories.length === 0" class="no-result">
                未找到分类
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.category-select {
  width: 100%;
}

.selected-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border: 2px solid var(--color-border);
  border-radius: 10px;
  background: var(--color-surface);
  cursor: pointer;
  transition: all 0.2s;
}

.selected-display:hover:not(.disabled) {
  border-color: var(--color-text-muted);
}

.selected-display.disabled {
  background: var(--color-bg-secondary);
  cursor: not-allowed;
}

.selected-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-text);
}

.category-icon {
  font-size: 16px;
}

.placeholder {
  font-size: 14px;
  color: var(--color-text-muted);
}

.select-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.clear-btn:hover {
  opacity: 1;
}

.clear-btn svg {
  width: 14px;
  height: 14px;
  color: var(--color-text-muted);
}

.dropdown-icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.selector-modal {
  background: var(--color-surface);
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  max-height: 500px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  border: 1px solid var(--color-border);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: var(--color-surface-hover);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: var(--color-border);
}

.close-btn svg {
  width: 18px;
  height: 18px;
  color: var(--color-text-muted);
}

.search-wrapper {
  position: relative;
  padding: 12px 20px;
  border-bottom: 1px solid var(--color-border);
}

.search-icon {
  position: absolute;
  left: 32px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--color-text-muted);
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 40px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background: var(--color-surface);
  color: var(--color-text);
}

.search-input:focus {
  border-color: var(--color-primary);
}

.category-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.category-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:hover {
  background: var(--color-surface-hover);
}

.category-item.selected {
  background: var(--color-primary-bg);
}

.category-name {
  font-size: 14px;
  color: var(--color-text);
}

.no-result {
  padding: 40px 20px;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 14px;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .selector-modal,
.modal-leave-active .selector-modal {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .selector-modal,
.modal-leave-to .selector-modal {
  opacity: 0;
  transform: scale(0.95);
}
</style>
