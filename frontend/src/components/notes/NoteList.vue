<script setup lang="ts">
import { computed } from 'vue';
import Empty from '@/components/common/Empty.vue';
import NoteSearch from '@/components/notes/NoteSearch.vue';
import NoteCard from '@/components/notes/NoteCard.vue';
import type { NoteListItem } from '@/types';

interface Props {
  notes: NoteListItem[];
  searchQuery?: string;
  showArchived?: boolean;
  isLoading?: boolean;
  hasMore?: boolean;
  total?: number;
  showCreateButton?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  searchQuery: '',
  showArchived: false,
  isLoading: false,
  hasMore: false,
  total: 0,
  showCreateButton: true,
});

const emit = defineEmits<{
  'update:searchQuery': [value: string];
  'update:showArchived': [value: boolean];
  search: [value: string];
  toggleArchived: [value: boolean];
  create: [];
  open: [id: number];
  edit: [id: number];
  archive: [id: number];
  remove: [id: number];
  togglePin: [id: number];
  loadMore: [];
}>();

const noteCount = computed(() => (props.total ? props.total : props.notes.length));

const handleSearchUpdate = (value: string) => {
  emit('update:searchQuery', value);
};

const handleArchivedUpdate = (value: boolean) => {
  emit('update:showArchived', value);
};
</script>

<template>
  <div class="notes-page">
    <div class="page-header">
      <div class="header-left">
        <h1>{{ showArchived ? '归档笔记' : '我的笔记' }}</h1>
        <p>{{ noteCount }} 篇笔记</p>
      </div>
      <button
        v-if="!showArchived && showCreateButton"
        class="create-btn"
        @click="emit('create')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        新建笔记
      </button>
    </div>

    <NoteSearch
      :model-value="searchQuery"
      :archived="showArchived"
      @update:modelValue="handleSearchUpdate"
      @update:archived="handleArchivedUpdate"
      @search="emit('search', $event)"
      @toggle-archived="emit('toggleArchived', $event)"
    />

    <div v-if="isLoading" class="loading-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card">
        <div class="skeleton-line title"></div>
        <div class="skeleton-line content"></div>
        <div class="skeleton-footer"></div>
      </div>
    </div>

    <div v-else-if="notes.length === 0" class="empty-state">
      <Empty
        :title="showArchived ? '暂无归档笔记' : '暂无笔记'"
        :description="showArchived ? '归档的笔记会显示在这里' : '开始创建你的第一篇笔记吧'"
        :action-label="showArchived ? '' : '新建笔记'"
        @action="emit('create')"
      />
    </div>

    <div v-else class="notes-grid">
      <NoteCard
        v-for="note in notes"
        :key="note.id"
        :note="note"
        :highlight="searchQuery"
        @open="emit('open', $event)"
        @edit="emit('edit', $event)"
        @archive="emit('archive', $event)"
        @remove="emit('remove', $event)"
        @togglePin="emit('togglePin', $event)"
      />
    </div>

    <div v-if="hasMore && !isLoading" class="load-more">
      <button class="load-more-btn" @click="emit('loadMore')">加载更多</button>
    </div>
  </div>
</template>

<style scoped>
.notes-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.header-left h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.header-left p {
  font-size: 14px;
  color: #9ca3af;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(124, 58, 237, 0.5);
}

.create-btn svg {
  width: 18px;
  height: 18px;
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.skeleton-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #e5e7eb;
}

.skeleton-line {
  height: 20px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  margin-bottom: 12px;
  animation: skeleton 1.5s ease-in-out infinite;
}

.skeleton-line.title {
  height: 24px;
  width: 80%;
}

.skeleton-line.content {
  height: 16px;
  width: 100%;
}

.skeleton-footer {
  height: 16px;
  width: 40%;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 6px;
  margin-top: 16px;
  animation: skeleton 1.5s ease-in-out infinite;
}

@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty-state {
  margin-top: 24px;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-top: 24px;
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.load-more-btn {
  padding: 10px 20px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 10px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}
</style>
