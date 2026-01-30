<template>
  <div class="note-grid">
    <div
      v-for="note in notes"
      :key="note.id"
      class="note-card-grid"
      @click="handleNoteClick(note)"
    >
      <div class="note-card-header">
        <h3 class="note-title">{{ note.title }}</h3>
        <button
          class="note-pin"
          :class="{ pinned: note.is_pinned }"
          @click.stop="togglePin(note)"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 17v5M9 11V7a3 3 0 0 1 6 0v4" />
            <path d="M5 11h14l-1.5 6h-11z" />
          </svg>
        </button>
      </div>
      
      <div class="note-preview" v-text="getPreview(note)"></div>
      
      <div class="note-meta">
        <span class="note-date">{{ formatDate(note.updated_at) }}</span>
        <div class="note-tags" v-if="note.tags?.length">
          <span
            v-for="tag in note.tags.slice(0, 3)"
            :key="tag.id"
            class="tag-dot"
            :style="{ background: tag.color || '#6b7280' }"
          />
          <span v-if="note.tags.length > 3" class="more-tags">
            +{{ note.tags.length - 3 }}
          </span>
        </div>
      </div>
      
      <div class="note-actions">
        <button class="action-btn" @click.stop="editNote(note)" title="编辑">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
        </button>
        <button class="action-btn" @click.stop="archiveNote(note)" title="归档">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="21 8 21 21 3 21 3 8" />
            <rect x="1" y="3" width="22" height="5" />
            <line x1="10" y1="12" x2="14" y2="12" />
          </svg>
        </button>
        <button class="action-btn danger" @click.stop="deleteNote(note)" title="删除">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
          </svg>
        </button>
      </div>
    </div>
    
    <Empty
      v-if="notes.length === 0"
      message="暂无笔记"
      description="创建您的第一篇笔记吧"
      actionText="新建笔记"
      actionRoute="/notes/new"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { formatDistanceToNow } from 'date-fns'
import { useNotesStore } from '@/stores/notes'
import Empty from '@/components/common/Empty.vue'
import type { Note } from '@/types/note'

interface Props {
  notes: Note[]
}

const props = defineProps<Props>()
const router = useRouter()
const notesStore = useNotesStore()

function handleNoteClick(note: Note) {
  router.push(`/notes/${note.id}`)
}

function editNote(note: Note) {
  router.push(`/notes/${note.id}/edit`)
}

async function togglePin(note: Note) {
  await notesStore.togglePin(note.id)
}

async function archiveNote(note: Note) {
  await notesStore.archiveNote(note.id)
}

async function deleteNote(note: Note) {
  if (confirm('确定要删除这篇笔记吗？')) {
    await notesStore.deleteNote(note.id)
  }
}

function getPreview(note: Note): string {
  if (note.plain_text) {
    return note.plain_text.slice(0, 150) + (note.plain_text.length > 150 ? '...' : '')
  }
  return ''
}

function formatDate(date: string): string {
  return formatDistanceToNow(new Date(date), { addSuffix: true, locale: 'zh_CN' })
}
</script>

<style lang="scss" scoped>
.note-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.note-card-grid {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: #3b82f6;
    
    .note-actions {
      opacity: 1;
    }
  }
}

.note-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.note-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.note-pin {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: #f3f4f6;
    color: #f59e0b;
  }
  
  &.pinned {
    color: #f59e0b;
  }
}

.note-preview {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  flex: 1;
  overflow: hidden;
  margin-bottom: 1rem;
}

.note-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid #f3f4f6;
}

.note-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.note-tags {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.tag-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.more-tags {
  font-size: 0.75rem;
  color: #9ca3af;
}

.note-actions {
  display: flex;
  gap: 0.25rem;
  margin-top: 0.75rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background: #f9fafb;
  color: #6b7280;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: #e5e7eb;
    color: #111827;
  }
  
  &.danger:hover {
    background: #fee2e2;
    color: #ef4444;
  }
}
</style>
