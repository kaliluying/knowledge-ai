/**
 * 附件类型定义
 */

export interface Attachment {
  id: number;
  name: string;
  file: string;
  file_type: 'image' | 'document' | 'video' | 'audio' | 'other';
  mime_type: string;
  size: number;
  size_formatted: string;
  extension: string;
  note: number | null;
  created_at: string;
}

export interface AttachmentListItem {
  id: number;
  name: string;
  file: string;
  file_type: 'image' | 'document' | 'video' | 'audio' | 'other';
  size: number;
  size_formatted: string;
  created_at: string;
}

export interface CreateAttachmentParams {
  file: File;
  name?: string;
  note?: number;
}

export interface AttachmentFilters {
  note?: number;
  type?: string;
  order?: string;
}
