/**
 * 标签 API
 */

import { api } from './index';
import type { Tag, TagListItem, CreateTagParams, UpdateTagParams } from '@/types';

export const tagsApi = {
  // 获取标签列表
  async getList() {
    const response = await api.get<{ code: number; message: string; data: Tag[] }>(
      '/tags/'
    );
    return response.data;
  },

  // 获取热门标签
  async getHot(limit = 10) {
    const response = await api.get<{ code: number; message: string; data: TagListItem[] }>(
      '/tags/hot/',
      { params: { limit } }
    );
    return response.data;
  },

  // 搜索标签
  async search(query: string) {
    const response = await api.get<{ code: number; message: string; data: TagListItem[] }>(
      '/tags/search/',
      { params: { q: query } }
    );
    return response.data;
  },

  // 获取所有标签
  async getAll() {
    const response = await api.get<{ code: number; message: string; data: TagListItem[] }>(
      '/tags/all/'
    );
    return response.data;
  },

  // 获取标签详情
  async getDetail(id: number) {
    const response = await api.get<{ code: number; message: string; data: Tag }>(
      `/tags/${id}/`
    );
    return response.data;
  },

  // 创建标签
  async create(data: CreateTagParams) {
    const response = await api.post<{ code: number; message: string; data: Tag }>(
      '/tags/',
      data
    );
    return response.data;
  },

  // 批量创建标签
  async bulkCreate(names: string[]) {
    const response = await api.post<{
      code: number;
      message: string;
      data: { created: TagListItem[]; existing: TagListItem[] };
    }>('/tags/bulk_create/', { names });
    return response.data;
  },

  // 更新标签
  async update(id: number, data: UpdateTagParams) {
    const response = await api.put<{ code: number; message: string; data: Tag }>(
      `/tags/${id}/`,
      data
    );
    return response.data;
  },

  // 删除标签
  async delete(id: number) {
    const response = await api.delete(`/tags/${id}/`);
    return response.data;
  },
};
