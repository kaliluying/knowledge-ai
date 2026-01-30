/**
 * 收藏状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { collectionsApi } from '@/api';
import type { Collection, CollectionListItem, CreateCollectionParams, CollectionFilters } from '@/types';

export const useCollectionsStore = defineStore('collections', () => {
  // 状态
  const collections = ref<CollectionListItem[]>([]);
  const currentCollection = ref<Collection | null>(null);
  const isLoading = ref(false);
  const pagination = ref({
    page: 1,
    pageSize: 20,
    count: 0,
  });
  const filters = ref<CollectionFilters>({});

  // 计算属性
  const hasMore = computed(() => pagination.value.count > collections.value.length);
  const processedCollections = computed(() => collections.value.filter(c => c.is_processed));
  const unprocessedCollections = computed(() => collections.value.filter(c => !c.is_processed));

  // 方法
  async function fetchCollections(params?: CollectionFilters) {
    isLoading.value = true;
    try {
      const response = await collectionsApi.getList({
        ...filters.value,
        ...params,
        page: params?.page || pagination.value.page,
        page_size: params?.page_size || pagination.value.pageSize,
      });

      if (params?.page === 1 || !params?.page) {
        collections.value = response.results || [];
      } else {
        collections.value.push(...(response.results || []));
      }

      pagination.value = {
        page: params?.page || 1,
        pageSize: response.results?.length || 0,
        count: response.count || 0,
      };

      return response;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchCollectionDetail(id: number) {
    isLoading.value = true;
    try {
      const response = await collectionsApi.getDetail(id);
      // response.data 是 {code, message, data: Collection}
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        currentCollection.value = response.data.data;
        return response.data.data;
      }
      return null;
    } catch {
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function createCollection(data: CreateCollectionParams) {
    isLoading.value = true;
    try {
      const response = await collectionsApi.create(data);
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        collections.value.unshift(response.data.data);
      }
      return { success: !!response?.data?.data, data: response?.data?.data || null, message: '' };
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { message?: string } } };
      return { success: false, data: null as unknown as CollectionListItem, message: axiosError.response?.data?.message || '添加收藏失败' };
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteCollection(id: number) {
    isLoading.value = true;
    try {
      await collectionsApi.delete(id);
      collections.value = collections.value.filter(c => c.id !== id);
      if (currentCollection.value?.id === id) {
        currentCollection.value = null;
      }
      return { success: true };
    } finally {
      isLoading.value = false;
    }
  }

  async function refreshCollection(id: number) {
    try {
      const response = await collectionsApi.refresh(id);
      // response.data 是 {code, message, data: Collection}
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        const refreshedData = response.data.data;
        // 更新列表中的收藏
        const index = collections.value.findIndex(c => c.id === id);
        if (index !== -1) {
          collections.value[index] = refreshedData;
        }
        // 更新当前收藏
        if (currentCollection.value?.id === id) {
          currentCollection.value = refreshedData;
        }
        return { success: true, data: refreshedData };
      }
      return { success: false };
    } catch {
      return { success: false };
    }
  }

  async function fetchRecentCollections(limit = 5) {
    try {
      const response = await collectionsApi.getRecent(limit);
      // response.data 就是数组
      if (response?.data && Array.isArray(response.data)) {
        return response.data;
      }
      return [];
    } catch {
      return [];
    }
  }

  function setFilters(newFilters: CollectionFilters) {
    filters.value = newFilters;
    pagination.value.page = 1;
  }

  function clearCurrentCollection() {
    currentCollection.value = null;
  }

  function reset() {
    collections.value = [];
    currentCollection.value = null;
    pagination.value = { page: 1, pageSize: 20, count: 0 };
    filters.value = {};
  }

  return {
    collections,
    currentCollection,
    isLoading,
    pagination,
    filters,
    hasMore,
    processedCollections,
    unprocessedCollections,
    fetchCollections,
    fetchCollectionDetail,
    createCollection,
    deleteCollection,
    refreshCollection,
    fetchRecentCollections,
    setFilters,
    clearCurrentCollection,
    reset,
  };
});
