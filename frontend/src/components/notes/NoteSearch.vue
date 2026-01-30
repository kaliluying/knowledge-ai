<script setup lang="ts">
interface Props {
  modelValue: string;
  archived?: boolean;
  placeholder?: string;
  activeLabel?: string;
  archivedLabel?: string;
}

const props = withDefaults(defineProps<Props>(), {
  archived: false,
  placeholder: '搜索笔记...',
  activeLabel: '查看归档',
  archivedLabel: '查看活跃',
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  'update:archived': [value: boolean];
  search: [value: string];
  toggleArchived: [value: boolean];
}>();

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};

const handleEnter = () => {
  emit('search', props.modelValue);
};

const toggleArchived = () => {
  const next = !props.archived;
  emit('update:archived', next);
  emit('toggleArchived', next);
};
</script>

<template>
  <div class="search-bar">
    <div class="search-input-wrapper">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8" />
        <path d="M21 21l-4.35-4.35" />
      </svg>
      <input
        :value="modelValue"
        type="text"
        class="search-input"
        :placeholder="placeholder"
        @input="handleInput"
        @keyup.enter="handleEnter"
      />
    </div>
    <button
      class="filter-btn"
      :class="{ active: archived }"
      @click="toggleArchived"
    >
      {{ archived ? archivedLabel : activeLabel }}
    </button>
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-input-wrapper {
  flex: 1;
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
  z-index: 10;
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

.search-input::placeholder {
  color: #9ca3af;
}

.filter-btn {
  padding: 14px 20px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.filter-btn.active {
  background: #8b5cf6;
  border-color: #8b5cf6;
  color: white;
}
</style>
