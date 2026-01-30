/**
 * 附件 API
 */

import { api } from './index';
import type { Attachment, AttachmentListItem, CreateAttachmentParams } from '@/types';

interface AttachmentListParams {
  page?: number;
  page_size?: number;
  note?: number;
  type?: string;
  order?: string;
}

export const attachmentsApi = {
  // 上传附件
  async upload(data: CreateAttachmentParams) {
    const formData = new FormData();
    formData.append('file', data.file);
    if (data.name) {
      formData.append('name', data.name);
    }
    if (data.note) {
      formData.append('note', data.note.toString());
    }

    const response = await api.post<{ code: number; message: string; data: Attachment }>(
      '/attachments/',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  // 获取附件列表
  async getList(params?: AttachmentListParams) {
    const response = await api.get<{ code: number; message: string; data: AttachmentListItem[]; count: number }>(
      '/attachments/',
      {
        params: {
          page: params?.page || 1,
          page_size: params?.page_size || 20,
          note: params?.note,
          type: params?.type,
          ordering: params?.order,
        },
      }
    );
    return response.data;
  },

  // 获取附件详情
  async getDetail(id: number) {
    const response = await api.get<{ code: number; message: string; data: Attachment }>(
      `/attachments/${id}/`
    );
    return response.data;
  },

  // 删除附件
  async delete(id: number) {
    const response = await api.delete(`/attachments/${id}/`);
    return response.data;
  },

  // 最近附件
  async getRecent(limit = 10) {
    const response = await api.get<{ code: number; message: string; data: AttachmentListItem[] }>(
      '/attachments/recent/',
      { params: { limit } }
    );
    return response.data;
  },

  // 批量删除
  async bulkDelete(ids: number[]) {
    const response = await api.delete('/attachments/bulk_delete/', { data: { ids } });
    return response.data;
  },
};
