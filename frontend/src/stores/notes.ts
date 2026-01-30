/**
 * 笔记状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { notesApi } from '@/api';
import type { Note, NoteListItem, CreateNoteParams, UpdateNoteParams, NoteFilters } from '@/types';

export const useNotesStore = defineStore('notes', () => {
  // 状态
  const notes = ref<NoteListItem[]>([]);
  const currentNote = ref<Note | null>(null);
  const isLoading = ref(false);
  const pagination = ref({
    page: 1,
    pageSize: 20,
    count: 0,
  });
  const filters = ref<NoteFilters>({});

  // 计算属性
  const hasMore = computed(() => pagination.value.count > notes.value.length);
  const pinnedNotes = computed(() => notes.value.filter(n => n && n.is_pinned));
  const unpinnedNotes = computed(() => notes.value.filter(n => n && !n.is_pinned));

  // 方法
  async function fetchNotes(params?: NoteFilters) {
    isLoading.value = true;
    try {
      const response = await notesApi.getList({
        ...filters.value,
        ...params,
        page: params?.page || pagination.value.page,
        page_size: params?.page_size || pagination.value.pageSize,
      });

      // 确保 results 是数组
      const results = Array.isArray(response.results) ? response.results : [];

      if (params?.page === 1 || !params?.page) {
        notes.value = results;
      } else {
        notes.value.push(...results);
      }

      pagination.value = {
        page: params?.page || 1,
        pageSize: results.length,
        count: response.count,
      };

      return response;
    } catch (error) {
      console.error('Failed to fetch notes:', error);
      notes.value = [];
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchNoteDetail(id: number) {
    isLoading.value = true;
    try {
      const response = await notesApi.getDetail(id);
      // response 是 {code, message, data: Note}
      if (response?.data) {
        currentNote.value = response.data;
        return response.data;
      }
      return null;
    } catch {
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function createNote(data: CreateNoteParams) {
    isLoading.value = true;
    try {
      const response = await notesApi.create(data);
      // response 已经是 {code, message, data: Note} 格式
      const newNote = response?.data;
      if (newNote && newNote.id) {
        notes.value.unshift(newNote);
      }
      return { success: !!newNote, data: newNote };
    } catch (error) {
      console.error('Failed to create note:', error);
      return { success: false, message: '创建失败' };
    } finally {
      isLoading.value = false;
    }
  }

  async function updateNote(id: number, data: UpdateNoteParams) {
    isLoading.value = true;
    try {
      const response = await notesApi.update(id, data);
      const updatedNote = response?.data;

      // 更新列表中的笔记
      const index = notes.value.findIndex(n => n && n.id === id);
      if (index !== -1 && updatedNote) {
        notes.value[index] = updatedNote;
      }

      // 更新当前笔记
      if (currentNote.value?.id === id && updatedNote) {
        currentNote.value = updatedNote;
      }

      return { success: true, data: updatedNote };
    } catch (error) {
      console.error('Failed to update note:', error);
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteNote(id: number) {
    isLoading.value = true;
    try {
      await notesApi.delete(id);
      notes.value = notes.value.filter(n => n && n.id !== id);
      if (currentNote.value?.id === id) {
        currentNote.value = null;
      }
      return { success: true };
    } catch (error) {
      console.error('Failed to delete note:', error);
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function archiveNote(id: number) {
    try {
      await notesApi.archive(id);
      notes.value = notes.value.filter(n => n && n.id !== id);
      if (currentNote.value?.id === id) {
        currentNote.value = null;
      }
      return { success: true };
    } catch (error) {
      console.error('Failed to archive note:', error);
      return { success: false };
    }
  }

  async function unarchiveNote(id: number) {
    try {
      const response = await notesApi.unarchive(id);
      const unarchivedNote = response?.data;
      if (unarchivedNote) {
        notes.value.unshift(unarchivedNote);
      }
      return { success: !!unarchivedNote };
    } catch (error) {
      console.error('Failed to unarchive note:', error);
      return { success: false };
    }
  }

  async function togglePin(id: number) {
    try {
      const response = await notesApi.togglePin(id);
      const pinData = response?.data;
      const note = notes.value.find(n => n && n.id === id);
      if (note && pinData) {
        note.is_pinned = pinData.is_pinned;
        // 重新排序
        notes.value.sort((a, b) => {
          if (!a || !b) return 0;
          if (a.is_pinned !== b.is_pinned) return b.is_pinned ? 1 : -1;
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
        });
      }
      return { success: !!pinData };
    } catch (error) {
      console.error('Failed to toggle pin:', error);
      return { success: false };
    }
  }

  async function incrementView(id: number) {
    try {
      await notesApi.incrementView(id);
    } catch (error) {
      console.error('Failed to increment view:', error);
    }
  }

  async function searchNotes(query: string) {
    isLoading.value = true;
    try {
      const response = await notesApi.search(query);
      return response;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchRecentNotes(limit = 10): Promise<NoteListItem[]> {
    try {
      const response = await notesApi.getRecent(limit);
      // response.data 就是数组
      if (response?.data && Array.isArray(response.data)) {
        return response.data;
      }
      return [];
    } catch {
      return [];
    }
  }

  function setFilters(newFilters: NoteFilters) {
    filters.value = newFilters;
    pagination.value.page = 1;
  }

  function clearCurrentNote() {
    currentNote.value = null;
  }

  function setCurrentNote(note: Note | null) {
    currentNote.value = note;
  }

  function reset() {
    notes.value = [];
    currentNote.value = null;
    pagination.value = { page: 1, pageSize: 20, count: 0 };
    filters.value = {};
  }

  return {
    notes,
    currentNote,
    isLoading,
    pagination,
    filters,
    hasMore,
    pinnedNotes,
    unpinnedNotes,
    fetchNotes,
    fetchNoteDetail,
    createNote,
    updateNote,
    deleteNote,
    archiveNote,
    unarchiveNote,
    togglePin,
    incrementView,
    searchNotes,
    fetchRecentNotes,
    setFilters,
    clearCurrentNote,
    setCurrentNote,
    reset,
  };
});
