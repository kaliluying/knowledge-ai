<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  fullscreen?: boolean;
}

withDefaults(defineProps<Props>(), {
  size: 'md',
  fullscreen: false,
});
</script>

<template>
  <div :class="['loading', { fullscreen }]">
    <div class="loading-spinner" :class="size">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    <p v-if="text" class="loading-text">{{ text }}</p>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.loading.fullscreen {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.9);
  z-index: 9999;
}

.loading-spinner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner-ring {
  position: absolute;
  border-radius: 50%;
  border: 3px solid transparent;
  border-top-color: #8b5cf6;
  animation: spin 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.spinner-ring:nth-child(1) {
  animation-delay: -0.45s;
}

.spinner-ring:nth-child(2) {
  animation-delay: -0.3s;
}

.spinner-ring:nth-child(3) {
  animation-delay: -0.15s;
}

.loading-sm .spinner-ring {
  width: 24px;
  height: 24px;
}

.loading-md .spinner-ring {
  width: 40px;
  height: 40px;
}

.loading-lg .spinner-ring {
  width: 64px;
  height: 64px;
}

.loading-text {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
