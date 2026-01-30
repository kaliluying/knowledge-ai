<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useNotesStore, useCategoriesStore, useTagsStore } from '@/stores';
import Select from '@/components/common/Select.vue';

const router = useRouter();
const notesStore = useNotesStore();
const categoriesStore = useCategoriesStore();
const tagsStore = useTagsStore();

const searchQuery = ref('');
const showArchived = ref(false);
const selectedCategoryId = ref<number | null>(null);
const selectedTagId = ref<number | null>(null);

const categoryOptions = computed(() => [
  { value: null, label: '全部分类' },
  ...categoriesStore.categories.map(category => ({
    value: category.id,
    label: category.name,
  })),
]);

const tagOptions = computed(() => [
  { value: null, label: '全部标签' },
  ...tagsStore.tags.map(tag => ({
    value: tag.id,
    label: tag.name,
  })),
]);

const loadNotes = async () => {
  await notesStore.fetchNotes({
    archived: showArchived.value,
    category: selectedCategoryId.value || undefined,
    tag: selectedTagId.value || undefined,
  });
};

onMounted(async () => {
  await Promise.all([
    categoriesStore.fetchCategories(),
    tagsStore.fetchTags(),
  ]);
  loadNotes();
});

const filteredNotes = computed(() => {
  const notes = notesStore.notes.filter(note => note && note.id);
  if (!searchQuery.value) return notes;
  const query = searchQuery.value.toLowerCase();
  return notes.filter(note =>
    note.title.toLowerCase().includes(query) ||
    (note.plain_text && note.plain_text.toLowerCase().includes(query))
  );
});

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (days === 0) return '今天';
  if (days === 1) return '昨天';
  if (days < 7) return `${days}天前`;
  return date.toLocaleDateString('zh-CN');
};

const getPreview = (plainText: string | null, maxLength = 100): string => {
  if (!plainText) return '';
  const text = plainText.replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

const highlightSegments = (text: string, query: string) => {
  if (!query || !text) return [{ text, match: false }];
  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const segments: { text: string; match: boolean }[] = [];
  let start = 0;
  let index = lowerText.indexOf(lowerQuery, start);

  while (index !== -1) {
    if (index > start) {
      segments.push({ text: text.slice(start, index), match: false });
    }
    segments.push({ text: text.slice(index, index + query.length), match: true });
    start = index + query.length;
    index = lowerText.indexOf(lowerQuery, start);
  }

  if (start < text.length) {
    segments.push({ text: text.slice(start), match: false });
  }

  return segments;
};

const navigateToNote = (id: number) => {
  router.push(`/notes/${id}`);
};

const navigateToCreate = () => {
  router.push('/notes/new');
};

const handleSearch = () => {
  loadNotes();
};

const handleFilterChange = () => {
  loadNotes();
};

const toggleArchived = () => {
  showArchived.value = !showArchived.value;
  loadNotes();
};
</script>

<template>
  <div class="notes-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-left">
        <h1>{{ showArchived ? '归档笔记' : '我的笔记' }}</h1>
        <p>{{ filteredNotes.length }} 篇笔记</p>
      </div>
      <button v-if="!showArchived" class="create-btn" @click="navigateToCreate">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        新建笔记
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="search-bar">
      <div class="search-input-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
        <input
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="text"
          placeholder="搜索笔记..."
          class="search-input"
        />
      </div>
      <Select
        v-model="selectedCategoryId"
        class="filter-select"
        :options="categoryOptions"
        size="lg"
        @change="handleFilterChange"
      />
      <Select
        v-model="selectedTagId"
        class="filter-select"
        :options="tagOptions"
        size="lg"
        @change="handleFilterChange"
      />
      <button
        class="filter-btn"
        :class="{ active: showArchived }"
        @click="toggleArchived"
      >
        {{ showArchived ? '查看活跃' : '查看归档' }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="notesStore.isLoading" class="loading-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card">
        <div class="skeleton-line title"></div>
        <div class="skeleton-line content"></div>
        <div class="skeleton-footer"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredNotes.length === 0" class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3>{{ showArchived ? '暂无归档笔记' : '暂无笔记' }}</h3>
      <p>{{ showArchived ? '归档的笔记会显示在这里' : '开始创建你的第一篇笔记吧' }}</p>
      <button v-if="!showArchived" class="create-btn-small" @click="navigateToCreate">
        新建笔记
      </button>
    </div>

    <!-- Notes Grid -->
    <div v-else class="notes-grid">
      <div
        v-for="note in filteredNotes"
        :key="note.id"
        class="note-card"
        @click="navigateToNote(note.id)"
      >
        <div class="note-header">
          <span v-if="note.is_pinned" class="pinned-badge">置顶</span>
        </div>

        <h3 class="note-title">
          <span v-for="(segment, index) in highlightSegments(note.title || '无标题', searchQuery)" :key="index">
            <mark v-if="segment.match">{{ segment.text }}</mark>
            <span v-else>{{ segment.text }}</span>
          </span>
        </h3>

        <p v-if="getPreview(note.plain_text, 120)" class="note-preview">
          <span v-for="(segment, index) in highlightSegments(getPreview(note.plain_text, 120), searchQuery)" :key="index">
            <mark v-if="segment.match">{{ segment.text }}</mark>
            <span v-else>{{ segment.text }}</span>
          </span>
        </p>

        <div class="note-tags">
          <span v-if="note.category_name" class="category-tag">{{ note.category_name }}</span>
          <span
            v-for="tag in note.tag_names"
            :key="tag"
            class="tag"
          >
            {{ tag }}
          </span>
        </div>

        <div class="note-footer">
          <span class="note-date">{{ formatDate(note.updated_at) }}</span>
          <div class="note-stats">
            <span class="view-count">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              {{ note.view_count }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Load More -->
    <div v-if="notesStore.hasMore && !notesStore.isLoading" class="load-more">
      <button class="load-more-btn" @click="loadNotes">加载更多</button>
    </div>
  </div>
</template>

<style scoped>
.notes-page {
  max-width: 1200px;
  margin: 0 auto;
}

/* Page header */
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

/* Search bar */
.search-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
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

.filter-select {
  min-width: 160px;
}

.filter-select :deep(.select-trigger) {
  padding: 12px 16px;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  background: white;
}

.filter-select :deep(.select-trigger:hover) {
  border-color: #8b5cf6;
}

.filter-select :deep(.select-wrapper.is-open .select-trigger) {
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
}

.filter-select :deep(.select-value),
.filter-select :deep(.select-placeholder) {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.filter-select :deep(.select-placeholder) {
  color: #6b7280;
}

.filter-select :deep(.dropdown) {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(124, 58, 237, 0.12), 0 2px 8px rgba(17, 24, 39, 0.08);
}

.filter-select :deep(.dropdown-item) {
  border-radius: 8px;
}

.filter-select :deep(.dropdown-item:hover:not(.disabled)) {
  background: rgba(139, 92, 246, 0.08);
}

.filter-select :deep(.dropdown-item.selected) {
  background: rgba(139, 92, 246, 0.12);
  color: #7c3aed;
}

.filter-select :deep(.dropdown-item.selected .check-icon) {
  color: #7c3aed;
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

/* Loading */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
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

/* Empty state */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: #f8fafc;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #9ca3af;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #9ca3af;
  margin-bottom: 24px;
}

.create-btn-small {
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

/* Notes grid */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.note-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
}

.note-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: #8b5cf6;
}

.note-header {
  margin-bottom: 12px;
}

.pinned-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background: #fef3c7;
  color: #d97706;
  font-size: 12px;
  font-weight: 600;
  border-radius: 6px;
}

.note-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.note-preview {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.note-preview :deep(mark),
.note-title :deep(mark) {
  background: #fef08a;
  color: #854d0e;
  padding: 0 2px;
  border-radius: 2px;
  font-weight: 600;
}

.note-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.category-tag {
  padding: 4px 12px;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
}

.tag {
  padding: 4px 12px;
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
}

.note-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.note-date {
  font-size: 13px;
  color: #9ca3af;
}

.note-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.view-count {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #9ca3af;
}

.view-count svg {
  width: 16px;
  height: 16px;
}

/* Load more */
.load-more {
  text-align: center;
  margin-top: 32px;
}

.load-more-btn {
  padding: 14px 32px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.load-more-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .search-bar {
    flex-direction: column;
  }

  .notes-grid {
    grid-template-columns: 1fr;
  }
}
</style>
