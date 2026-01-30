<script setup lang="ts">
import { ref } from 'vue';

type ToastType = 'success' | 'error' | 'warning' | 'info';

interface ToastItem {
  id: number;
  type: ToastType;
  message: string;
  duration?: number;
}

const toasts = ref<ToastItem[]>([]);
let toastId = 0;

export function show(message: string, type: ToastType = 'info', duration = 3000) {
  const id = ++toastId;
  const toast: ToastItem = { id, type, message, duration };
  toasts.value.push(toast);

  if (duration > 0) {
    setTimeout(() => remove(id), duration);
  }

  return id;
}

export function success(message: string, duration?: number) {
  return show(message, 'success', duration);
}

export function error(message: string, duration?: number) {
  return show(message, 'error', duration);
}

export function warning(message: string, duration?: number) {
  return show(message, 'warning', duration);
}

export function info(message: string, duration?: number) {
  return show(message, 'info', duration);
}

export function remove(id: number) {
  const index = toasts.value.findIndex(t => t.id === id);
  if (index > -1) {
    toasts.value.splice(index, 1);
  }
}

export function clear() {
  toasts.value = [];
}

const typeIcons: Record<ToastType, string> = {
  success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  error: 'M10 14l2-2m0 0l2-2m-2 2l-2-2M6 10l2 2m0 0l2 2m-2-2l2-2m2 2l2 2',
  warning: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
  info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
};

function getIconPath(type: ToastType) {
  return typeIcons[type];
}
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="toast.type"
      >
        <svg class="toast-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path :d="getIconPath(toast.type)" />
        </svg>
        <span class="toast-message">{{ toast.message }}</span>
        <button class="toast-close" @click="remove(toast.id)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
}

.toast.success {
  border-left: 4px solid #10b981;
}

.toast.error {
  border-left: 4px solid #ef4444;
}

.toast.warning {
  border-left: 4px solid #f59e0b;
}

.toast.info {
  border-left: 4px solid #3b82f6;
}

.toast-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.toast.success .toast-icon {
  color: #10b981;
}

.toast.error .toast-icon {
  color: #ef4444;
}

.toast.warning .toast-icon {
  color: #f59e0b;
}

.toast.info .toast-icon {
  color: #3b82f6;
}

.toast-message {
  flex: 1;
  font-size: 14px;
  color: #1f2937;
  line-height: 1.5;
}

.toast-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.toast-close:hover {
  opacity: 1;
}

.toast-close svg {
  width: 16px;
  height: 16px;
  color: #6b7280;
}

/* Transitions */
.toast-enter-active {
  animation: slideIn 0.3s ease;
}

.toast-leave-active {
  animation: slideOut 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}
</style>
