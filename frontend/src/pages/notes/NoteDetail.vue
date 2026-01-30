<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useNotesStore } from '@/stores';
import { marked } from 'marked';

const router = useRouter();
const route = useRoute();
const notesStore = useNotesStore();

const note = ref<any>(null);
const isLoading = ref(true);
const isDeleting = ref(false);

const noteId = parseInt(route.params.id as string);

onMounted(async () => {
  try {
    note.value = await notesStore.fetchNoteDetail(noteId);
    // 增加浏览次数
    if (note.value) {
      await notesStore.incrementView(noteId);
      note.value.view_count = (note.value.view_count || 0) + 1;
    }
  } catch (e) {
    router.push('/notes');
  } finally {
    isLoading.value = false;
  }
});

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN');
};

const navigateToEdit = () => {
  router.push(`/notes/${noteId}/edit`);
};

const handleDelete = async () => {
  if (!confirm('确定要删除这篇笔记吗？此操作不可恢复。')) return;

  isDeleting.value = true;
  try {
    await notesStore.deleteNote(noteId);
    router.push('/notes');
  } catch (e) {
    alert('删除失败');
  } finally {
    isDeleting.value = false;
  }
};

const handleArchive = async () => {
  try {
    await notesStore.archiveNote(noteId);
    router.push('/notes');
  } catch (e) {
    alert('归档失败');
  }
};

// Parse markdown content to HTML
const parsedContent = computed(() => {
  if (!note.value?.content) return '';
  return marked(note.value.content, {
    breaks: true,
    gfm: true,
  });
});
</script>

<template>
  <div class="note-detail-page">
    <!-- Loading -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- Note content -->
    <div v-else-if="note" class="note-content">
      <!-- Header -->
      <div class="detail-header">
        <button class="back-btn" @click="router.back()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 19l-7-7 7-7" />
          </svg>
          返回
        </button>
        <div class="header-actions">
          <button class="action-btn secondary" @click="handleArchive">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            归档
          </button>
          <button class="action-btn danger" @click="handleDelete" :disabled="isDeleting">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            删除
          </button>
          <button class="action-btn primary" @click="navigateToEdit">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            编辑
          </button>
        </div>
      </div>

      <!-- Title -->
      <h1 class="note-title">{{ note.title || '无标题' }}</h1>

      <!-- Meta info -->
      <div class="note-meta">
        <div class="meta-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ formatDate(note.created_at) }}</span>
        </div>
        <div class="meta-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <span>{{ note.view_count }} 次阅读</span>
        </div>
        <div class="meta-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>{{ note.word_count || 0 }} 字 · {{ note.reading_time || 0 }} 分钟阅读</span>
        </div>
      </div>

      <!-- Category and Tags -->
      <div class="note-tags">
        <span v-if="note.category_name" class="category-tag">{{ note.category_name }}</span>
        <span
          v-for="(tag, index) in (note.tag_names || [])"
          :key="index"
          class="tag"
        >
          {{ tag }}
        </span>
      </div>

      <!-- Content (rendered markdown) -->
      <div class="note-content-body" v-html="parsedContent"></div>
    </div>
  </div>
</template>

<style scoped>
.note-detail-page {
  max-width: 900px;
  margin: 0 auto;
}

/* Loading */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 20px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #9ca3af;
  font-size: 14px;
}

/* Detail header */
.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

.action-btn.primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(124, 58, 237, 0.5);
}

.action-btn.secondary {
  background: white;
  border-color: #e5e7eb;
  color: #6b7280;
}

.action-btn.secondary:hover {
  border-color: #8b5cf6;
  color: #8b5cf6;
}

.action-btn.danger {
  background: white;
  border-color: #fecaca;
  color: #dc2626;
}

.action-btn.danger:hover {
  background: #fef2f2;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Title */
.note-title {
  font-size: 36px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 20px;
  line-height: 1.3;
}

/* Meta */
.note-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #9ca3af;
}

.meta-item svg {
  width: 18px;
  height: 18px;
}

/* Tags */
.note-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 32px;
}

.category-tag {
  padding: 6px 14px;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
}

.tag {
  padding: 6px 14px;
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
}

/* Note content body */
.note-content-body {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 2px solid #e5e7eb;
  min-height: 400px;
  color: #374151;
  line-height: 1.7;
}

.note-content-body :deep(h1) {
  font-size: 2em;
  font-weight: 700;
  margin: 1em 0 0.5em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
}

.note-content-body :deep(h2) {
  font-size: 1.5em;
  font-weight: 600;
  margin: 1em 0 0.5em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
}

.note-content-body :deep(h3) {
  font-size: 1.25em;
  font-weight: 600;
  margin: 1em 0 0.5em;
  color: #1f2937;
}

.note-content-body :deep(p) {
  margin: 0.75em 0;
}

.note-content-body :deep(a) {
  color: #8b5cf6;
  text-decoration: none;
}

.note-content-body :deep(a:hover) {
  text-decoration: underline;
}

.note-content-body :deep(code) {
  background: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  color: #f97316;
}

.note-content-body :deep(pre) {
  background: #1f2937;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1em 0;
}

.note-content-body :deep(pre code) {
  background: transparent;
  padding: 0;
  color: #e5e7eb;
}

.note-content-body :deep(ul),
.note-content-body :deep(ol) {
  padding-left: 2em;
  margin: 0.75em 0;
}

.note-content-body :deep(blockquote) {
  border-left: 4px solid #8b5cf6;
  padding-left: 1em;
  margin: 1em 0;
  color: #6b7280;
}

.note-content-body :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 2em 0;
}

.note-content-body :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}

.note-content-body :deep(th),
.note-content-body :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 8px 12px;
  text-align: left;
}

.note-content-body :deep(th) {
  background: #f9fafb;
  font-weight: 600;
}

.note-content-body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 1em 0;
}

/* Responsive */
@media (max-width: 768px) {
  .detail-header {
    flex-direction: column;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .note-title {
    font-size: 28px;
  }

  .note-meta {
    gap: 16px;
  }

  .note-content-body {
    padding: 20px;
  }
}
</style>
