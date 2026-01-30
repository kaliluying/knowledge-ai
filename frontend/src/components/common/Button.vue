<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  block?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  block: false,
  type: 'button',
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

const handleClick = (e: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', e);
  }
};

const variantClasses = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  outline: 'btn-outline',
  ghost: 'btn-ghost',
  danger: 'btn-danger',
};

const sizeClasses = {
  sm: 'btn-sm',
  md: 'btn-md',
  lg: 'btn-lg',
};
</script>

<template>
  <button
    :type="type"
    class="btn"
    :class="[variantClasses[variant], sizeClasses[size], { block, loading }]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <svg v-if="loading" class="spinner" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="31.4 31.4" />
    </svg>
    <slot />
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Variants */
.btn-primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
}

.btn-secondary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}

.btn-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
}

.btn-outline {
  background: transparent;
  color: #8b5cf6;
  border: 2px solid #8b5cf6;
}

.btn-outline:hover:not(:disabled) {
  background: rgba(139, 92, 246, 0.1);
}

.btn-ghost {
  background: transparent;
  color: #6b7280;
}

.btn-ghost:hover:not(:disabled) {
  background: #f3f4f6;
  color: #1f2937;
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
}

.btn-danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
}

/* Sizes */
.btn-sm {
  padding: 8px 14px;
  font-size: 13px;
}

.btn-md {
  padding: 10px 20px;
  font-size: 14px;
}

.btn-lg {
  padding: 14px 28px;
  font-size: 16px;
}

.block {
  width: 100%;
}
</style>
