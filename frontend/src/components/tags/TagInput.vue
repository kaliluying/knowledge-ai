<script setup lang="ts">
import { ref, computed } from 'vue';
import { useTagsStore } from '@/stores';
import TagComponent from './Tag.vue';
import type { Tag } from '@/types';

interface Props {
  placeholder?: string;
  disabled?: boolean;
  showColors?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '输入标签名称...',
  disabled: false,
  showColors: true,
});

const emit = defineEmits<{
  created: [tag: Tag];
}>();

const tagsStore = useTagsStore();

const tagName = ref('');
const selectedColor = ref('#8b5cf6');
const isLoading = ref(false);
const errorMessage = ref('');

const colorOptions = [
  '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
  '#06b6d4', '#6366f1', '#ef4444', '#84cc16',
  '#f97316', '#8b5cf6', '#14b8a6', '#a855f7',
];

const isValid = computed(() => {
  const name = tagName.value.trim();
  return name.length >= 1 && name.length <= 20;
});

const isNameExists = computed(() => {
  const name = tagName.value.trim().toLowerCase();
  return tagsStore.tags.some(t => t.name.toLowerCase() === name);
});

const handleSubmit = async () => {
  if (!isValid.value || props.disabled || isLoading.value) return;
  if (isNameExists.value) {
    errorMessage.value = '标签已存在';
    return;
  }

  errorMessage.value = '';
  isLoading.value = true;

  try {
    const result = await tagsStore.createTag({
      name: tagName.value.trim(),
      color: selectedColor.value,
    });

    if (result.success && result.data) {
      emit('created', result.data as Tag);
      tagName.value = '';
      selectedColor.value = '#8b5cf6';
    } else {
      errorMessage.value = '创建失败';
    }
  } catch {
    errorMessage.value = '创建失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};

const selectColor = (color: string) => {
  selectedColor.value = color;
};

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSubmit();
  }
};
</script>

<template>
  <div class="tag-input" :class="{ disabled }">
    <div class="input-row">
      <input
        v-model="tagName"
        type="text"
        :placeholder="placeholder"
        :disabled="disabled || isLoading"
        class="name-input"
        @keydown="handleKeydown"
      />

      <div v-if="showColors" class="color-picker">
        <button
          v-for="color in colorOptions"
          :key="color"
          class="color-option"
          :class="{ active: selectedColor === color }"
          :style="{ background: color }"
          @click="selectColor(color)"
        />
      </div>

      <button
        class="submit-btn"
        :disabled="!isValid || disabled || isLoading || isNameExists"
        @click="handleSubmit"
      >
        <svg v-if="isLoading" class="spinner" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" />
        </svg>
        <span v-else>添加</span>
      </button>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="isNameExists && tagName.trim()" class="warning-message">
      标签 "{{ tagName.trim() }}" 已存在
    </div>

    <div v-if="tagName.trim().length > 20" class="warning-message">
      标签名称不能超过 20 个字符
    </div>

    <div v-if="tagName.trim()" class="preview">
      <span class="preview-label">预览：</span>
      <TagComponent :tag="{ 
        id: 0, 
        name: tagName.trim(), 
        color: selectedColor, 
        slug: '',
        description: null,
        owner: 0,
        usage_count: 0,
        created_at: '',
        updated_at: ''
      }" />
    </div>
  </div>
</template>

<style scoped>
.tag-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tag-input.disabled {
  opacity: 0.6;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.name-input {
  flex: 1;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s;
}

.name-input:focus {
  border-color: #8b5cf6;
}

.name-input:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.color-picker {
  display: flex;
  gap: 6px;
}

.color-option {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #1f2937;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 80px;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.spinner {
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-message {
  font-size: 13px;
  color: #ef4444;
  padding: 4px 0;
}

.warning-message {
  font-size: 13px;
  color: #f59e0b;
  padding: 4px 0;
}

.preview {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid #f3f4f6;
}

.preview-label {
  font-size: 13px;
  color: #9ca3af;
}

@media (max-width: 640px) {
  .input-row {
    flex-wrap: wrap;
  }

  .color-picker {
    order: 3;
    width: 100%;
    margin-top: 8px;
    justify-content: flex-start;
  }

  .color-option {
    width: 28px;
    height: 28px;
  }
}
</style>
