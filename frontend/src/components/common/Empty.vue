<script setup lang="ts">
interface Props {
  type?: 'empty' | 'search' | 'folder' | 'bookmark' | 'image';
  title?: string;
  description?: string;
  actionLabel?: string;
  actionRoute?: string;
}

withDefaults(defineProps<Props>(), {
  type: 'empty',
  title: '暂无数据',
  description: '',
  actionLabel: '',
});

const emit = defineEmits<{
  action: [];
}>();

const typeIcons = {
  empty: 'M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z',
  search: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
  folder: 'M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z',
  bookmark: 'M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z',
  image: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
};
</script>

<template>
  <div class="empty-state">
    <div class="empty-icon" :class="type">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path :d="typeIcons[type]" />
      </svg>
    </div>
    <h3 class="empty-title">{{ title }}</h3>
    <p v-if="description" class="empty-description">{{ description }}</p>
    <button
      v-if="actionLabel"
      class="empty-action"
      @click="emit('action')"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 10px 40px rgba(139, 92, 246, 0.2);
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.empty-icon.empty {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.empty-icon.search {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 10px 40px rgba(59, 130, 246, 0.2);
}

.empty-icon.folder {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 10px 40px rgba(245, 158, 11, 0.2);
}

.empty-icon.bookmark {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.2);
}

.empty-icon.image {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  box-shadow: 0 10px 40px rgba(236, 72, 153, 0.2);
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.empty-description {
  font-size: 14px;
  color: #9ca3af;
  margin: 0 0 20px 0;
  max-width: 300px;
  line-height: 1.6;
}

.empty-action {
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);
}

.empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
}
</style>
