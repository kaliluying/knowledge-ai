/**
 * 标签操作组合式函数
 */

import { computed } from 'vue';
import { useTagsStore } from '@/stores/tags';
import type { CreateTagParams } from '@/types';

export function useTags() {
  const tagsStore = useTagsStore();

  // 状态
  const tags = computed(() => tagsStore.tags);
  const hotTags = computed(() => tagsStore.hotTags);
  const isLoading = computed(() => tagsStore.isLoading);

  // 方法
  async function fetchTags() {
    return tagsStore.fetchTags();
  }

  async function fetchHotTags(limit = 10) {
    return tagsStore.fetchHotTags(limit);
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
    hotTags,
    isLoading,
    fetchTags,
    fetchHotTags,
    createTag,
    updateTag,
    deleteTag,
  };
}
