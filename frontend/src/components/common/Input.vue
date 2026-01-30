<script setup lang="ts">
interface Props {
  modelValue: string | number;
  type?: string;
  placeholder?: string;
  label?: string;
  error?: string;
  disabled?: boolean;
  readonly?: boolean;
  size?: 'sm' | 'md' | 'lg';
  prefixIcon?: string;
  suffixIcon?: string;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  disabled: false,
  readonly: false,
  size: 'md',
});

const emit = defineEmits<{
  'update:modelValue': [value: string | number];
  blur: [event: FocusEvent];
  focus: [event: FocusEvent];
}>();

const handleInput = (e: Event) => {
  const target = e.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};

const sizeClasses = {
  sm: 'input-sm',
  md: 'input-md',
  lg: 'input-lg',
};
</script>

<template>
  <div class="input-wrapper" :class="{ 'has-error': error }">
    <label v-if="label" class="input-label">{{ label }}</label>
    <div class="input-container" :class="sizeClasses[size]">
      <svg v-if="prefixIcon" class="input-icon prefix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path v-if="prefixIcon === 'search'" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <input
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        class="input"
        :class="{ 'has-prefix': prefixIcon, 'has-suffix': suffixIcon }"
        @input="handleInput"
        @blur="emit('blur', $event)"
        @focus="emit('focus', $event)"
      />
      <svg v-if="suffixIcon" class="input-icon suffix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle v-if="suffixIcon === 'calendar'" cx="12" cy="12" r="10" />
        <path v-if="suffixIcon === 'calendar'" d="M12 6v6l4 2" />
      </svg>
    </div>
    <p v-if="error" class="input-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input {
  width: 100%;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #1f2937;
  background: white;
  outline: none;
  transition: all 0.2s;
}

.input:focus {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.input:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.input:read-only {
  background: #f9fafb;
  cursor: default;
}

.input-icon {
  position: absolute;
  width: 18px;
  height: 18px;
  color: #9ca3af;
}

.input-icon.prefix {
  left: 14px;
}

.input-icon.suffix {
  right: 14px;
}

.has-prefix .input {
  padding-left: 44px;
}

.has-suffix .input {
  padding-right: 44px;
}

/* Sizes */
.input-sm {
  font-size: 13px;
}

.input-sm .input {
  padding: 8px 12px;
}

.input-md .input {
  padding: 10px 14px;
}

.input-lg .input {
  padding: 14px 16px;
  font-size: 16px;
}

/* Error state */
.has-error .input {
  border-color: #ef4444;
}

.has-error .input:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);
}

.input-error {
  font-size: 13px;
  color: #ef4444;
}
</style>
