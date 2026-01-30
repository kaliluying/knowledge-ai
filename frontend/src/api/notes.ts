/**
 * 笔记 API
 */

import { api } from './index';
import type {
  Note,
  NoteListItem,
  CreateNoteParams,
  UpdateNoteParams,
  PaginatedResponse,
} from '@/types';

interface NoteListParams {
  page?: number;
  page_size?: number;
  archived?: boolean;
  category?: number;
  tag?: number;
  ordering?: string;
}

export const notesApi = {
  // 获取笔记列表
  async getList(params?: NoteListParams) {
    const response = await api.get<PaginatedResponse<NoteListItem>>('/notes/', {
      params: {
        page: params?.page || 1,
        page_size: params?.page_size || 20,
        archived: params?.archived ? 'true' : 'false',
        category: params?.category,
        tag: params?.tag,
        ordering: params?.ordering,
      },
    });
    return response.data;
  },

  // 获取笔记详情
  async getDetail(id: number) {
    const response = await api.get<{ code: number; message: string; data: Note }>(
      `/notes/${id}/`
    );
    return response.data;
  },

  // 创建笔记
  async create(data: CreateNoteParams) {
    const response = await api.post<{ code: number; message: string; data: Note }>(
      '/notes/',
      data
    );
    return response.data;
  },

  // 更新笔记
  async update(id: number, data: UpdateNoteParams) {
    const response = await api.put<{ code: number; message: string; data: Note }>(
      `/notes/${id}/`,
      data
    );
    return response.data;
  },

  // 删除笔记
  async delete(id: number) {
    const response = await api.delete(`/notes/${id}/`);
    return response.data;
  },

  // 归档笔记
  async archive(id: number) {
    const response = await api.post(`/notes/${id}/archive/`);
    return response.data;
  },

  // 取消归档
  async unarchive(id: number) {
    const response = await api.post(`/notes/${id}/unarchive/`);
    return response.data;
  },

  // 置顶/取消置顶
  async togglePin(id: number) {
    const response = await api.post(`/notes/${id}/pin/`);
    return response.data;
  },

  // 搜索笔记
  async search(query: string, page = 1, pageSize = 20) {
    const response = await api.get<PaginatedResponse<NoteListItem>>('/notes/search/', {
      params: { q: query, page, page_size: pageSize },
    });
    return response.data;
  },

  // 最近笔记
  async getRecent(limit = 10) {
    const response = await api.get<{ code: number; message: string; data: NoteListItem[] }>(
      '/notes/recent/',
      { params: { limit } }
    );
    return response.data;
  },

  // 已归档笔记
  async getArchived(page = 1, pageSize = 20) {
    const response = await api.get<PaginatedResponse<NoteListItem>>('/notes/archived/', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  // 获取笔记内容
  async getContent(id: number) {
    const response = await api.get<{ code: number; message: string; data: { content: Note['content'] } }>(
      `/notes/${id}/content/`
    );
    return response.data;
  },

  // 增加浏览次数
  async incrementView(id: number) {
    const response = await api.post(`/notes/${id}/increment-view/`);
    return response.data;
  },

  // 获取笔记建议（用于内部链接选择器）
  async getSuggestions(query: string = '', limit: number = 20) {
    const response = await api.get<{ code: number; message: string; data: { id: number; title: string }[] }>(
      '/notes/suggestions/',
      { params: { q: query, limit } }
    );
    return response.data;
  },
};
