<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

interface Option {
  value: string | number | null;
  label: string;
  disabled?: boolean;
}

interface Props {
  modelValue: string | number | null;
  options: Option[];
  placeholder?: string;
  label?: string;
  error?: string;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
  clearable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请选择',
  disabled: false,
  size: 'md',
  clearable: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null];
  change: [value: string | number | null];
}>();

const isOpen = ref(false);
const searchQuery = ref('');
const selectRef = ref<HTMLElement>();

const selectedOption = computed(() => {
  return props.options.find(opt => opt.value === props.modelValue);
});

const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options;
  const query = searchQuery.value.toLowerCase();
  return props.options.filter(opt =>
    opt.label.toLowerCase().includes(query) &&
    opt.value !== props.modelValue
  );
});

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
    if (isOpen.value) {
      searchQuery.value = '';
    }
  }
};

const selectOption = (option: Option) => {
  if (!option.disabled) {
    emit('update:modelValue', option.value);
    emit('change', option.value);
    isOpen.value = false;
  }
};

const clearSelection = (e: Event) => {
  e.stopPropagation();
  emit('update:modelValue', null);
  emit('change', null);
};

const handleClickOutside = (e: MouseEvent) => {
  if (selectRef.value && !selectRef.value.contains(e.target as Node)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

const sizeClasses = {
  sm: 'select-sm',
  md: 'select-md',
  lg: 'select-lg',
};
</script>

<template>
  <div ref="selectRef" class="select-wrapper" :class="{ 'has-error': error, 'is-open': isOpen }">
    <label v-if="label" class="select-label">{{ label }}</label>
    <div
      class="select-trigger"
      :class="[sizeClasses[size], { disabled, 'has-value': modelValue }]"
      @click="toggleDropdown"
    >
      <span v-if="selectedOption" class="select-value">{{ selectedOption.label }}</span>
      <span v-else class="select-placeholder">{{ placeholder }}</span>

      <div class="select-suffix">
        <button
          v-if="clearable && modelValue"
          class="clear-btn"
          @click="clearSelection"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 9l6 6 6-6" />
        </svg>
      </div>
    </div>

    <Transition name="dropdown">
      <div v-if="isOpen" class="dropdown">
        <div v-if="options.length > 10" class="dropdown-search">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索..."
            class="search-input"
          />
        </div>
        <div class="dropdown-list">
          <div
            v-for="option in filteredOptions"
            :key="option.value"
            class="dropdown-item"
            :class="{ disabled: option.disabled, selected: option.value === modelValue }"
            @click="selectOption(option)"
          >
            <span class="item-content">{{ option.label }}</span>
            <svg v-if="option.value === modelValue" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5" />
            </svg>
          </div>
          <div v-if="filteredOptions.length === 0" class="no-options">
            <span>无匹配选项</span>
          </div>
        </div>
      </div>
    </Transition>

    <p v-if="error" class="select-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.select-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.select-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.select-trigger {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-trigger:hover:not(.disabled) {
  border-color: #8b5cf6;
  background: #f9fafb;
}

.select-wrapper.is-open .select-trigger {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.select-trigger.disabled {
  background: #f9fafb;
  cursor: not-allowed;
  opacity: 0.6;
}

.select-value {
  flex: 1;
  font-size: 14px;
  color: #1f2937;
  font-weight: 500;
}

.select-placeholder {
  flex: 1;
  font-size: 14px;
  color: #6b7280;
}

.select-suffix {
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  border-radius: 50%;
}

.select-trigger:hover .clear-btn {
  opacity: 0.5;
}

.clear-btn:hover {
  opacity: 1 !important;
  background: #f3f4f6;
}

.clear-btn svg {
  width: 12px;
  height: 12px;
  color: #6b7280;
}

.chevron {
  width: 16px;
  height: 16px;
  color: #6b7280;
  transition: transform 0.2s ease;
}

.is-open .chevron {
  transform: rotate(180deg);
}

/* Sizes */
.select-sm {
  padding: 6px 10px;
  font-size: 13px;
}

.select-md {
  padding: 8px 12px;
  font-size: 14px;
}

.select-lg {
  padding: 10px 14px;
  font-size: 15px;
}

/* Dropdown */
.dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  right: 0;
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(124, 58, 237, 0.12), 0 2px 8px rgba(17, 24, 39, 0.08);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-search {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
}

.search-icon {
  width: 16px;
  height: 16px;
  color: #9ca3af;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: #1f2937;
  outline: none;
}

.search-input:-webkit-autofill,
.search-input:-webkit-autofill:hover,
.search-input:-webkit-autofill:focus {
  -webkit-text-fill-color: #1f2937;
  transition: background-color 5000s ease-in-out 0s;
}

.search-input::placeholder {
  color: #9ca3af;
}

.dropdown-list {
  max-height: 240px;
  overflow-y: auto;
  padding: 6px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  font-size: 14px;
  color: #1f2937;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.dropdown-item:hover:not(.disabled) {
  background: rgba(139, 92, 246, 0.08);
}

.dropdown-item.selected {
  background: rgba(139, 92, 246, 0.12);
  color: #7c3aed;
  font-weight: 500;
}

.dropdown-item.disabled {
  color: #9ca3af;
  cursor: not-allowed;
}

.item-content {
  flex: 1;
}

.check-icon {
  width: 16px;
  height: 16px;
  color: #8b5cf6;
  flex-shrink: 0;
}

.no-options {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px 12px;
  color: #9ca3af;
  font-size: 14px;
}

/* Error state */
.has-error .select-trigger {
  border-color: #ef4444;
}

.has-error.is-open .select-trigger {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.has-error .select-label {
  color: #ef4444;
}

.select-error {
  font-size: 13px;
  color: #ef4444;
}

/* Transitions */
.dropdown-enter-active {
  animation: dropdownIn 0.2s ease;
}

.dropdown-leave-active {
  animation: dropdownOut 0.15s ease;
}

@keyframes dropdownIn {
  from {
    opacity: 0;
    transform: translateY(-8px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes dropdownOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-8px) scale(0.98);
  }
}
</style>
