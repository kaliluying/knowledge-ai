<script setup lang="ts">
import type { NoteListItem } from '@/types';

interface Props {
  note: NoteListItem;
  highlight?: string;
  showActions?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  highlight: '',
  showActions: true,
});

const emit = defineEmits<{
  open: [id: number];
  edit: [id: number];
  archive: [id: number];
  remove: [id: number];
  togglePin: [id: number];
}>();

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

const getPreview = (plainText: string | null, maxLength = 120): string => {
  if (!plainText) return '';
  const text = plainText.replace(/\s+/g, ' ').trim();
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
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

const handleOpen = () => emit('open', props.note.id);
const handleEdit = () => emit('edit', props.note.id);
const handleArchive = () => emit('archive', props.note.id);
const handleRemove = () => emit('remove', props.note.id);
const handleTogglePin = () => emit('togglePin', props.note.id);

const preview = getPreview(props.note.plain_text, 120);
</script>

<template>
  <div class="note-card" @click="handleOpen">
    <div class="note-header">
      <span v-if="note.is_pinned" class="pinned-badge">置顶</span>
      <button
        v-if="showActions"
        class="note-pin"
        :class="{ pinned: note.is_pinned }"
        @click.stop="handleTogglePin"
        title="置顶"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 17v5M9 11V7a3 3 0 0 1 6 0v4" />
          <path d="M5 11h14l-1.5 6h-11z" />
        </svg>
      </button>
    </div>

    <h3 class="note-title">
      <span v-for="(segment, index) in highlightSegments(note.title || '无标题', highlight)" :key="index">
        <mark v-if="segment.match">{{ segment.text }}</mark>
        <span v-else>{{ segment.text }}</span>
      </span>
    </h3>

    <p v-if="preview" class="note-preview">
      <span v-for="(segment, index) in highlightSegments(preview, highlight)" :key="index">
        <mark v-if="segment.match">{{ segment.text }}</mark>
        <span v-else>{{ segment.text }}</span>
      </span>
    </p>

    <div class="note-tags">
      <span v-if="note.category_name" class="category-tag">{{ note.category_name }}</span>
      <span v-for="tag in note.tag_names" :key="tag" class="tag">
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

    <div v-if="showActions" class="note-actions">
      <button class="action-btn" @click.stop="handleEdit" title="编辑">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
      </button>
      <button class="action-btn" @click.stop="handleArchive" title="归档">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="21 8 21 21 3 21 3 8" />
          <rect x="1" y="3" width="22" height="5" />
          <line x1="10" y1="12" x2="14" y2="12" />
        </svg>
      </button>
      <button class="action-btn danger" @click.stop="handleRemove" title="删除">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6" />
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.note-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.note-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border-color: #8b5cf6;
}

.note-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.pinned-badge {
  background: #fef3c7;
  color: #f59e0b;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
}

.note-pin {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  color: #9ca3af;
  border-radius: 8px;
  transition: all 0.2s;
}

.note-pin:hover {
  color: #f59e0b;
  background: #fef3c7;
}

.note-pin.pinned {
  color: #f59e0b;
}

.note-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
  line-height: 1.4;
}

.note-preview {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 16px;
}

.note-preview mark,
.note-title mark {
  background: #fef3c7;
  color: #f59e0b;
  padding: 0 2px;
  border-radius: 4px;
}

.note-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.category-tag {
  background: #ede9fe;
  color: #7c3aed;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
}

.tag {
  background: #f3f4f6;
  color: #6b7280;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 12px;
}

.note-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.note-date {
  font-size: 12px;
  color: #9ca3af;
}

.note-stats {
  display: flex;
  gap: 12px;
}

.view-count {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #9ca3af;
}

.view-count svg {
  width: 14px;
  height: 14px;
}

.note-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  opacity: 0;
  transition: opacity 0.2s;
}

.note-card:hover .note-actions {
  opacity: 1;
}

.action-btn {
  flex: 1;
  padding: 8px;
  border: none;
  background: #f9fafb;
  color: #6b7280;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #e5e7eb;
  color: #111827;
}

.action-btn.danger:hover {
  background: #fee2e2;
  color: #ef4444;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}
</style>
