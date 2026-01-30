/**
 * 标签操作组合式函数
 */

import { computed } from 'vue';
import { useTagsStore } from '@/stores/tags';
import type { Tag, CreateTagParams, TagFilters } from '@/types';

export function useTags() {
  const tagsStore = useTagsStore();

  // 状态
  const tags = computed(() => tagsStore.tags);
  const popularTags = computed(() => tagsStore.popularTags);
  const isLoading = computed(() => tagsStore.isLoading);

  // 方法
  async function fetchTags(params?: TagFilters) {
    return tagsStore.fetchTags(params);
  }

  async function fetchPopularTags(limit = 10) {
    return tagsStore.fetchPopularTags(limit);
  }

  async function createTag(data: CreateTagParams) {
    return tagsStore.createTag(data);
  }

  async function updateTag(id: number, data: Partial<CreateTagParams>) {
    return tagsStore.updateTag(id, data);
  }

  async function deleteTag(id: number) {
    return tagsStore.deleteTag(id);
  }

  return {
    tags,
    popularTags,
    isLoading,
    fetchTags,
    fetchPopularTags,
    createTag,
    updateTag,
    deleteTag,
  };
}
