/**
 * 分类操作组合式函数
 */

import { computed } from 'vue';
import { useCategoriesStore } from '@/stores/categories';
import type { Category, CreateCategoryParams } from '@/types';

export function useCategories() {
  const categoriesStore = useCategoriesStore();

  // 状态
  const categories = computed(() => categoriesStore.categories);
  const categoryTree = computed(() => categoriesStore.categoryTree);
  const currentCategory = computed(() => categoriesStore.currentCategory);
  const isLoading = computed(() => categoriesStore.isLoading);

  // 方法
  async function fetchCategories() {
    return categoriesStore.fetchCategories();
  }

  async function fetchCategoryTree() {
    return categoriesStore.fetchCategoryTree();
  }

  async function createCategory(data: CreateCategoryParams) {
    return categoriesStore.createCategory(data);
  }

  async function updateCategory(id: number, data: Partial<CreateCategoryParams>) {
    return categoriesStore.updateCategory(id, data);
  }

  async function deleteCategory(id: number) {
    return categoriesStore.deleteCategory(id);
  }

  function setCurrentCategory(category: Category | null) {
    categoriesStore.setCurrentCategory(category);
  }

  return {
    categories,
    categoryTree,
    currentCategory,
    isLoading,
    fetchCategories,
    fetchCategoryTree,
    createCategory,
    updateCategory,
    deleteCategory,
    setCurrentCategory,
  };
}
