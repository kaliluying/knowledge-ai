/**
 * 附件状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { attachmentsApi } from '@/api';
import type { Attachment, AttachmentListItem, CreateAttachmentParams } from '@/types';

interface AttachmentListParams {
  page?: number;
  pageSize?: number;
  count?: number;
  note?: number;
  type?: string;
  order?: string;
}

export const useAttachmentsStore = defineStore('attachments', () => {
  const attachments = ref<AttachmentListItem[]>([]);
  const currentAttachment = ref<Attachment | null>(null);
  const isLoading = ref(false);
  const pagination = ref({
    page: 1,
    pageSize: 20,
    count: 0,
  });
  const filters = ref<AttachmentListParams>({});

  const hasMore = computed(() => pagination.value.count > attachments.value.length);
  const imageAttachments = computed(() => attachments.value.filter((a) => a.file_type === 'image'));
  const documentAttachments = computed(() => attachments.value.filter((a) => a.file_type === 'document'));

  async function fetchAttachments(params?: AttachmentListParams) {
    isLoading.value = true;
    try {
      const response = await attachmentsApi.getList({
        ...filters.value,
        ...params,
        page: params?.page || pagination.value.page,
        page_size: params?.pageSize || pagination.value.pageSize,
      });

      const results = response?.data || [];
      if (params?.page === 1 || !params?.page) {
        attachments.value = results;
      } else {
        attachments.value.push(...results);
      }

      pagination.value = {
        page: params?.page || 1,
        pageSize: results.length,
        count: response?.count || 0,
      };

      return response;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchAttachmentDetail(id: number) {
    isLoading.value = true;
    try {
      const response = await attachmentsApi.getDetail(id);
      // response.data 是 {code, message, data: Attachment}
      if (response?.data?.data) {
        currentAttachment.value = response.data.data;
        return response.data.data;
      }
      return null;
    } catch {
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  async function uploadAttachment(data: CreateAttachmentParams) {
    isLoading.value = true;
    try {
      const response = await attachmentsApi.upload(data);
      // response.data 是 {code, message, data: Attachment}
      const newAttachment = response?.data?.data;
      if (newAttachment) {
        attachments.value.unshift(newAttachment);
      }
      return { success: !!newAttachment, data: newAttachment };
    } catch {
      return { success: false, data: null };
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteAttachment(id: number) {
    isLoading.value = true;
    try {
      await attachmentsApi.delete(id);
      attachments.value = attachments.value.filter(a => a.id !== id);
      if (currentAttachment.value?.id === id) {
        currentAttachment.value = null;
      }
      return { success: true };
    } finally {
      isLoading.value = false;
    }
  }

  async function bulkDeleteAttachments(ids: number[]) {
    isLoading.value = true;
    try {
      await attachmentsApi.bulkDelete(ids);
      attachments.value = attachments.value.filter(a => !ids.includes(a.id));
      return { success: true };
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchRecentAttachments(limit = 10) {
    try {
      const response = await attachmentsApi.getRecent(limit);
      return response?.data?.data || [];
    } catch {
      return [];
    }
  }

  function setFilters(newFilters: AttachmentListParams) {
    filters.value = newFilters;
    pagination.value.page = 1;
  }

  function clearCurrentAttachment() {
    currentAttachment.value = null;
  }

  function reset() {
    attachments.value = [];
    currentAttachment.value = null;
    pagination.value = { page: 1, pageSize: 20, count: 0 };
    filters.value = {};
  }

  return {
    attachments,
    currentAttachment,
    isLoading,
    pagination,
    filters,
    hasMore,
    imageAttachments,
    documentAttachments,
    fetchAttachments,
    fetchAttachmentDetail,
    uploadAttachment,
    deleteAttachment,
    bulkDeleteAttachments,
    fetchRecentAttachments,
    setFilters,
    clearCurrentAttachment,
    reset,
  };
});
