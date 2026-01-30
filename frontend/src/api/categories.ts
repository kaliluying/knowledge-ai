/**
 * 分类 API
 */

import { api } from './index';
import type { Category, CategoryTreeItem, CreateCategoryParams, UpdateCategoryParams } from '@/types';

export const categoriesApi = {
  // 获取分类列表
  async getList() {
    const response = await api.get<{ code: number; message: string; data: Category[] }>(
      '/categories/'
    );
    return response.data;
  },

  // 获取分类树
  async getTree() {
    const response = await api.get<{ code: number; message: string; data: CategoryTreeItem[] }>(
      '/categories/tree/'
    );
    return response.data;
  },

  // 获取一级分类
  async getRoot() {
    const response = await api.get<{ code: number; message: string; data: Category[] }>(
      '/categories/root/'
    );
    return response.data;
  },

  // 获取所有分类（扁平）
  async getAll() {
    const response = await api.get<{ code: number; message: string; data: Category[] }>(
      '/categories/all/'
    );
    return response.data;
  },

  // 获取分类详情
  async getDetail(id: number) {
    const response = await api.get<{ code: number; message: string; data: Category }>(
      `/categories/${id}/`
    );
    return response.data;
  },

  // 获取子分类
  async getChildren(id: number) {
    const response = await api.get<{ code: number; message: string; data: Category[] }>(
      `/categories/${id}/children/`
    );
    return response.data;
  },

  // 创建分类
  async create(data: CreateCategoryParams) {
    const response = await api.post<{ code: number; message: string; data: Category }>(
      '/categories/',
      data
    );
    return response.data;
  },

  // 更新分类
  async update(id: number, data: UpdateCategoryParams) {
    const response = await api.put<{ code: number; message: string; data: Category }>(
      `/categories/${id}/`,
      data
    );
    return response.data;
  },

  // 删除分类
  async delete(id: number) {
    const response = await api.delete(`/categories/${id}/`);
    return response.data;
  },
};
