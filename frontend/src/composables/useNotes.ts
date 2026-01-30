/**
 * 笔记操作组合式函数
 */

import { computed } from 'vue';
import { useNotesStore } from '@/stores/notes';
import { useRouter } from 'vue-router';
import type { Note, CreateNoteParams, NoteFilters } from '@/types';

export function useNotes() {
  const notesStore = useNotesStore();
  const router = useRouter();

  // 状态
  const notes = computed(() => notesStore.notes);
  const currentNote = computed(() => notesStore.currentNote);
  const isLoading = computed(() => notesStore.isLoading);
  const hasMore = computed(() => notesStore.hasMore);
  const pagination = computed(() => notesStore.pagination);

  // 方法
  async function fetchNotes(params?: NoteFilters) {
    return notesStore.fetchNotes(params);
  }

  async function fetchNoteDetail(id: number) {
    return notesStore.fetchNoteDetail(id);
  }

  async function createNote(data: CreateNoteParams) {
    const result = await notesStore.createNote(data);
    if (result.success) {
      router.push(`/notes/${result.data.id}`);
    }
    return result;
  }

  async function updateNote(id: number, data: Partial<CreateNoteParams>) {
    return notesStore.updateNote(id, data);
  }

  async function deleteNote(id: number) {
    const result = await notesStore.deleteNote(id);
    if (result.success) {
      router.push('/notes');
    }
    return result;
  }

  async function archiveNote(id: number) {
    return notesStore.archiveNote(id);
  }

  async function searchNotes(keyword: string) {
    return notesStore.searchNotes(keyword);
  }

  async function fetchRecentNotes(limit = 10) {
    return notesStore.fetchRecentNotes(limit);
  }

  function setFilters(filters: NoteFilters) {
    notesStore.setFilters(filters);
  }

  function clearCurrentNote() {
    notesStore.clearCurrentNote();
  }

  return {
    notes,
    currentNote,
    isLoading,
    hasMore,
    pagination,
    fetchNotes,
    fetchNoteDetail,
    createNote,
    updateNote,
    deleteNote,
    archiveNote,
    searchNotes,
    fetchRecentNotes,
    setFilters,
    clearCurrentNote,
  };
}
