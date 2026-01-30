/**
 * 收藏 API
 */

import { api } from './index';
import type {
  Collection,
  CollectionListItem,
  CreateCollectionParams,
  PaginatedResponse,
} from '@/types';

interface CollectionListParams {
  page?: number;
  page_size?: number;
  search?: string;
  processed?: boolean;
  ordering?: string;
}

export const collectionsApi = {
  // 获取收藏列表
  async getList(params?: CollectionListParams) {
    const response = await api.get<PaginatedResponse<CollectionListItem>>('/collections/', {
      params: {
        page: params?.page || 1,
        page_size: params?.page_size || 20,
        search: params?.search,
        processed: params?.processed,
        ordering: params?.ordering,
      },
    });
    return response.data;
  },

  // 获取收藏详情
  async getDetail(id: number) {
    const response = await api.get<{ code: number; message: string; data: Collection }>(
      `/collections/${id}/`
    );
    return response.data;
  },

  // 创建收藏
  async create(data: CreateCollectionParams) {
    const response = await api.post<{ code: number; message: string; data: Collection }>(
      '/collections/',
      data
    );
    return response.data;
  },

  // 删除收藏
  async delete(id: number) {
    const response = await api.delete(`/collections/${id}/`);
    return response.data;
  },

  // 刷新收藏内容
  async refresh(id: number) {
    const response = await api.post<{ code: number; message: string; data: Collection }>(
      `/collections/${id}/refresh/`
    );
    return response.data;
  },

  // 最近收藏
  async getRecent(limit = 5) {
    const response = await api.get<{ code: number; message: string; data: CollectionListItem[] }>(
      '/collections/recent/',
      { params: { limit } }
    );
    return response.data;
  },
};
