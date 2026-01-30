<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useTagsStore } from '@/stores';
import TagComponent from './Tag.vue';
import type { Tag } from '@/types';

interface Props {
  modelValue: Tag[];
  placeholder?: string;
  disabled?: boolean;
  maxTags?: number;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '选择标签...',
  disabled: false,
  maxTags: 5,
});

const emit = defineEmits<{
  'update:modelValue': [tags: Tag[]];
  add: [tag: Tag];
  remove: [tag: Tag];
}>();

const tagsStore = useTagsStore();
const searchQuery = ref('');
const isOpen = ref(false);
const highlightedIndex = ref(-1);

const allTags = computed(() => tagsStore.tags);

const filteredTags = computed(() => {
  if (!searchQuery.value) return allTags.value;
  const query = searchQuery.value.toLowerCase();
  return allTags.value.filter(tag =>
    tag.name.toLowerCase().includes(query)
  );
});

const selectedTags = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
});

const availableTags = computed(() =>
  filteredTags.value.filter(tag => !selectedTags.value.find(t => t.id === tag.id))
);

const isMaxReached = computed(() => selectedTags.value.length >= props.maxTags);

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
    if (isOpen.value) {
      searchQuery.value = '';
      highlightedIndex.value = -1;
    }
  }
};

const closeDropdown = () => {
  isOpen.value = false;
  searchQuery.value = '';
  highlightedIndex.value = -1;
};

const selectTag = (tag: Tag) => {
  if (props.disabled || isMaxReached.value) return;
  if (selectedTags.value.find(t => t.id === tag.id)) return;

  const newTags = [...selectedTags.value, tag];
  selectedTags.value = newTags;
  emit('add', tag);
  searchQuery.value = '';
  highlightedIndex.value = -1;
};

const removeTag = (tag: Tag) => {
  selectedTags.value = selectedTags.value.filter(t => t.id !== tag.id);
  emit('remove', tag);
};

const handleKeydown = (e: KeyboardEvent) => {
  if (!isOpen.value) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleDropdown();
    }
    return;
  }

  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault();
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, availableTags.value.length - 1);
      break;
    case 'ArrowUp':
      e.preventDefault();
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1);
      break;
    case 'Enter':
      e.preventDefault();
      if (highlightedIndex.value >= 0) {
        const tag = availableTags.value[highlightedIndex.value];
        if (tag) {
          selectTag(tag);
        }
      }
      break;
    case 'Escape':
      closeDropdown();
      break;
  }
};

watch(isOpen, (open) => {
  if (open) {
    tagsStore.fetchTags();
  }
});
</script>

<template>
  <div class="tag-select" :class="{ disabled, open: isOpen }">
    <div class="selected-tags" @click="toggleDropdown">
      <TagComponent
        v-for="tag in selectedTags"
        :key="tag.id"
        :tag="tag"
        removable
        @remove="removeTag"
      />
      <input
        v-model="searchQuery"
        type="text"
        :placeholder="selectedTags.length === 0 ? placeholder : ''"
        :disabled="disabled || isMaxReached"
        class="search-input"
        @focus="isOpen = true"
        @keydown="handleKeydown"
      />
      <span v-if="isMaxReached" class="max-hint">最多 {{ maxTags }} 个</span>
    </div>

    <div v-if="isOpen" class="dropdown">
      <div class="dropdown-header">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索标签..."
          class="dropdown-search"
          @keydown="handleKeydown"
        />
      </div>

      <div class="dropdown-list">
        <button
          v-for="(tag, index) in availableTags"
          :key="tag.id"
          class="dropdown-item"
          :class="{ highlighted: index === highlightedIndex }"
          @click="selectTag(tag)"
          @mouseenter="highlightedIndex = index"
        >
          <TagComponent :tag="tag" size="sm" />
        </button>

        <div v-if="availableTags.length === 0" class="dropdown-empty">
          <p>没有找到标签</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tag-select {
  position: relative;
  border: 2px solid var(--color-border);
  border-radius: 10px;
  background: var(--color-surface);
  transition: all 0.2s;
}

.tag-select:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
}

.tag-select.disabled {
  background: var(--color-bg-secondary);
  cursor: not-allowed;
}

.tag-select.open {
  border-color: var(--color-primary);
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  min-height: 44px;
}

.search-input {
  flex: 1;
  min-width: 80px;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-text);
  background: transparent;
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.max-hint {
  font-size: 12px;
  color: var(--color-text-muted);
}

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  z-index: 100;
  animation: dropdownIn 0.2s ease;
}

@keyframes dropdownIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
}

.dropdown-header svg {
  width: 18px;
  height: 18px;
  color: var(--color-text-muted);
}

.dropdown-search {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: var(--color-text);
}

.dropdown-list {
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.dropdown-item:hover,
.dropdown-item.highlighted {
  background: var(--color-surface-hover);
}

.dropdown-empty {
  padding: 20px;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 14px;
}
</style>
