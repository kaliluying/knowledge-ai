/**
 * 标签状态管理
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { tagsApi } from '@/api';
import type { Tag, TagListItem, CreateTagParams, UpdateTagParams } from '@/types';

export const useTagsStore = defineStore('tags', () => {
  // 状态
  const tags = ref<Tag[]>([]);
  const hotTags = ref<TagListItem[]>([]);
  const currentTag = ref<Tag | null>(null);
  const isLoading = ref(false);

  // 方法
  async function fetchTags() {
    isLoading.value = true;
    try {
      const response = await tagsApi.getList();
      // 标签列表返回格式 {code, message, data: [...]} 
      if (response?.data && Array.isArray(response.data)) {
        tags.value = response.data;
        return response.data;
      }
      return [];
    } catch {
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchHotTags(limit = 10) {
    try {
      const response = await tagsApi.getHot(limit);
      // response.data 是 {code, message, data: [...]}
      if (response?.data && Array.isArray(response.data)) {
        hotTags.value = response.data;
        return response.data;
      }
      return [];
    } catch {
      return [];
    }
  }

  async function searchTags(query: string) {
    try {
      const response = await tagsApi.search(query);
      // response.data 是 {code, message, data: [...]}
      if (response?.data && Array.isArray(response.data)) {
        return response.data;
      }
      return [];
    } catch {
      return [];
    }
  }

  async function fetchTagDetail(id: number) {
    isLoading.value = true;
    try {
      const response = await tagsApi.getDetail(id);
      // response.data 是 {code, message, data: Tag}
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        currentTag.value = response.data.data;
        return response.data.data;
      }
      return null;
    } catch {
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function createTag(data: CreateTagParams) {
    isLoading.value = true;
    try {
      const response = await tagsApi.create(data);
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        tags.value.push(response.data.data);
      }
      return { success: !!response?.data?.data, data: response?.data?.data };
    } catch {
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function bulkCreateTags(names: string[]) {
    isLoading.value = true;
    try {
      const response = await tagsApi.bulkCreate(names);
      // 刷新标签列表
      await fetchTags();
      return { success: true };
    } catch {
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function updateTag(id: number, data: UpdateTagParams) {
    isLoading.value = true;
    try {
      const response = await tagsApi.update(id, data);

      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        const index = tags.value.findIndex(t => t.id === id);
        if (index !== -1) {
          tags.value[index] = response.data.data;
        }

        if (currentTag.value?.id === id) {
          currentTag.value = response.data.data;
        }
      }

      return { success: !!response?.data?.data, data: response?.data?.data };
    } catch {
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteTag(id: number) {
    isLoading.value = true;
    try {
      await tagsApi.delete(id);
      tags.value = tags.value.filter(t => t.id !== id);
      if (currentTag.value?.id === id) {
        currentTag.value = null;
      }
      return { success: true };
    } finally {
      isLoading.value = false;
    }
  }

  function clearCurrentTag() {
    currentTag.value = null;
  }

  function reset() {
    tags.value = [];
    hotTags.value = [];
    currentTag.value = null;
  }

  return {
    tags,
    hotTags,
    currentTag,
    isLoading,
    fetchTags,
    fetchHotTags,
    searchTags,
    fetchTagDetail,
    createTag,
    bulkCreateTags,
    updateTag,
    deleteTag,
    clearCurrentTag,
    reset,
  };
});
