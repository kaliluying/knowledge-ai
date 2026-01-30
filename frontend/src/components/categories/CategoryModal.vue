<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import type { Category, CreateCategoryParams, UpdateCategoryParams } from '@/types';
import { useCategoriesStore } from '@/stores/categories';
import { useModal } from '@/composables/useModal';

interface Props {
  modelValue: boolean;
  category?: Category | null;
  mode?: 'create' | 'edit';
  parentId?: number | null;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  category: null,
  mode: 'create',
  parentId: null,
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  success: [category: Category];
  close: [];
}>();

const categoriesStore = useCategoriesStore();
const { open, close } = useModal();

const form = ref<CreateCategoryParams>({
  name: '',
  description: '',
  color: '#8b5cf6',
  icon: '',
  parent_id: null,
  sort_order: 0,
});

const errors = ref<Record<string, string>>({});
const isLoading = ref(false);

const isOpen = computed(() => props.modelValue);

const colorPresets = [
  '#8b5cf6', '#10b981', '#f59e0b', '#ef4444',
  '#3b82f6', '#ec4899', '#06b6d4', '#84cc16',
];

const iconPresets = ['📁', '📝', '💡', '🎯', '🚀', '📚', '🔧', '⭐'];

watch(() => props.modelValue, (val) => {
  if (val) {
    openCategoryModal();
  }
});

watch(() => props.category, (val) => {
  if (val && props.mode === 'edit') {
    form.value = {
      name: val.name,
      description: val.description || '',
      color: val.color,
      icon: val.icon || '',
      parent_id: val.parent,
      sort_order: val.sort_order,
    };
  }
});

function openCategoryModal() {
  if (props.mode === 'create') {
    form.value = {
      name: '',
      description: '',
      color: '#8b5cf6',
      icon: '',
      parent_id: props.parentId,
      sort_order: 0,
    };
  }
  errors.value = {};
}

function closeModal() {
  emit('update:modelValue', false);
  emit('close');
}

function selectColor(color: string) {
  form.value.color = color;
}

function selectIcon(icon: string) {
  form.value.icon = icon;
}

function validate(): boolean {
  errors.value = {};
  
  if (!form.value.name.trim()) {
    errors.value.name = '请输入分类名称';
  } else if (form.value.name.length > 50) {
    errors.value.name = '分类名称不能超过50个字符';
  }
  
  return Object.keys(errors.value).length === 0;
}

async function handleSubmit() {
  if (!validate()) return;
  
  isLoading.value = true;
  
  try {
    let result;
    
    if (props.mode === 'edit' && props.category) {
      const updateData: UpdateCategoryParams = {
        name: form.value.name,
        description: form.value.description,
        color: form.value.color,
        icon: form.value.icon || undefined,
        parent_id: form.value.parent_id || undefined,
      };
      result = await categoriesStore.updateCategory(props.category.id, updateData);
    } else {
      result = await categoriesStore.createCategory(form.value);
    }
    
    if (result.success) {
      emit('success', result.data);
      closeModal();
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal" @click.stop>
          <!-- Header -->
          <div class="modal-header">
            <h3>{{ mode === 'create' ? '新建分类' : '编辑分类' }}</h3>
            <button class="close-btn" @click="closeModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <!-- 分类名称 -->
            <div class="form-group">
              <label class="form-label">分类名称 <span class="required">*</span></label>
              <input
                v-model="form.name"
                type="text"
                placeholder="请输入分类名称"
                class="form-input"
                :class="{ 'has-error': errors.name }"
                maxlength="50"
              />
              <p v-if="errors.name" class="form-error">{{ errors.name }}</p>
            </div>

            <!-- 分类描述 -->
            <div class="form-group">
              <label class="form-label">分类描述</label>
              <textarea
                v-model="form.description"
                placeholder="可选的分类描述"
                class="form-textarea"
                rows="3"
              ></textarea>
            </div>

            <!-- 颜色选择 -->
            <div class="form-group">
              <label class="form-label">颜色</label>
              <div class="color-picker">
                <button
                  v-for="color in colorPresets"
                  :key="color"
                  type="button"
                  class="color-option"
                  :class="{ active: form.color === color }"
                  :style="{ backgroundColor: color }"
                  @click="selectColor(color)"
                ></button>
                <input
                  v-model="form.color"
                  type="color"
                  class="color-input"
                />
              </div>
            </div>

            <!-- 图标选择 -->
            <div class="form-group">
              <label class="form-label">图标</label>
              <div class="icon-picker">
                <button
                  v-for="icon in iconPresets"
                  :key="icon"
                  type="button"
                  class="icon-option"
                  :class="{ active: form.icon === icon }"
                  @click="selectIcon(icon)"
                >
                  {{ icon }}
                </button>
              </div>
            </div>

            <!-- 预览 -->
            <div class="form-group">
              <label class="form-label">预览</label>
              <div class="preview">
                <span class="preview-icon" :style="{ color: form.color }">
                  {{ form.icon || '📁' }}
                </span>
                <span class="preview-name">{{ form.name || '分类名称' }}</span>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="modal-footer">
            <button class="btn-cancel" @click="closeModal" :disabled="isLoading">
              取消
            </button>
            <button class="btn-submit" @click="handleSubmit" :disabled="isLoading || !form.name.trim()">
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ mode === 'create' ? '创建' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: modalIn 0.3s ease;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: #f3f4f6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
}

.close-btn svg {
  width: 18px;
  height: 18px;
  color: #6b7280;
}

.modal-body {
  padding: 24px;
  max-height: calc(80vh - 200px);
  overflow-y: auto;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.required {
  color: #ef4444;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #1f2937;
  background: white;
  outline: none;
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.form-input.has-error {
  border-color: #ef4444;
}

.form-error {
  font-size: 13px;
  color: #ef4444;
  margin-top: 6px;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

/* Color Picker */
.color-picker {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.color-option {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #1f2937;
  box-shadow: 0 0 0 2px white, 0 0 0 4px #8b5cf6;
}

.color-input {
  width: 32px;
  height: 32px;
  padding: 0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Icon Picker */
.icon-picker {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.icon-option {
  width: 40px;
  height: 40px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-option:hover {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.05);
}

.icon-option.active {
  border-color: #8b5cf6;
  background: rgba(139, 92, 246, 0.1);
}

/* Preview */
.preview {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 10px;
}

.preview-icon {
  font-size: 24px;
}

.preview-name {
  font-size: 14px;
  color: #1f2937;
}

/* Footer */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #f3f4f6;
}

.btn-cancel {
  padding: 10px 20px;
  background: #f3f4f6;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}
</style>
