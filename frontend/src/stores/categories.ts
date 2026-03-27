/**
 * 分类状态管理
 */

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { categoriesApi } from '@/api';
import type { Category, CategoryTreeItem, CreateCategoryParams, UpdateCategoryParams } from '@/types';

export const useCategoriesStore = defineStore('categories', () => {
  // 状态
  const categories = ref<Category[]>([]);
  const categoryTree = ref<CategoryTreeItem[]>([]);
  const currentCategory = ref<Category | null>(null);
  const isLoading = ref(false);

  // 方法
  async function fetchCategories() {
    isLoading.value = true;
    try {
      const response = await categoriesApi.getList();
      if (response?.data && Array.isArray(response.data)) {
        categories.value = response.data;
        return response.data;
      }
      return [];
    } catch {
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchCategoryTree() {
    isLoading.value = true;
    try {
      const response = await categoriesApi.getTree();
      if (response?.data && Array.isArray(response.data)) {
        categoryTree.value = response.data;
        return response.data;
      }
      return [];
    } catch (error) {
      console.error('fetchCategoryTree error:', error);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchCategoryDetail(id: number) {
    isLoading.value = true;
    try {
      const response = await categoriesApi.getDetail(id);
      if (response?.data && !Array.isArray(response.data)) {
        currentCategory.value = response.data;
        return response.data;
      }
      return null;
    } catch {
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function createCategory(data: CreateCategoryParams) {
    isLoading.value = true;
    try {
      const response = await categoriesApi.create(data);
      if (response?.data) {
        categories.value.push(response.data);
        // 刷新树
        await fetchCategoryTree();
        return { success: true, data: response.data };
      }
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function updateCategory(id: number, data: UpdateCategoryParams) {
    isLoading.value = true;
    try {
      const response = await categoriesApi.update(id, data);
      if (response?.data) {
        // 更新列表
        const index = categories.value.findIndex(c => c.id === id);
        if (index !== -1) {
          categories.value[index] = response.data;
        }

        // 更新当前分类
        if (currentCategory.value?.id === id) {
          currentCategory.value = response.data;
        }

        // 刷新树
        await fetchCategoryTree();
        return { success: true, data: response.data };
      }
      return { success: false };
    } catch (error) {
      console.error('更新分类失败:', error);
      return { success: false };
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteCategory(id: number) {
    isLoading.value = true;
    try {
      await categoriesApi.delete(id);
      categories.value = categories.value.filter(c => c.id !== id);
      if (currentCategory.value?.id === id) {
        currentCategory.value = null;
      }
      // 刷新树
      await fetchCategoryTree();
      return { success: true };
    } finally {
      isLoading.value = false;
    }
  }

  function clearCurrentCategory() {
    currentCategory.value = null;
  }

  function reset() {
    categories.value = [];
    categoryTree.value = [];
    currentCategory.value = null;
  }

  return {
    categories,
    categoryTree,
    currentCategory,
    isLoading,
    fetchCategories,
    fetchCategoryTree,
    fetchCategoryDetail,
    createCategory,
    updateCategory,
    deleteCategory,
    clearCurrentCategory,
    reset,
  };
});
