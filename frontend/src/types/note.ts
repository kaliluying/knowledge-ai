/**
 * 笔记类型定义 (Markdown 编辑器)
 */

import type { Category } from './category';
import type { Tag } from './tag';

// TipTap JSON content (legacy, for backward compatibility)
export interface TipTapNode {
  type: string;
  content?: TipTapNode[];
  text?: string;
  marks?: TipTapMark[];
  attrs?: Record<string, unknown>;
}

export interface TipTapMark {
  type: string;
  attrs?: Record<string, unknown>;
}

export interface Note {
  id: number;
  title: string;
  slug: string;
  content: string; // Markdown content
  plain_text: string;
  cover_image: string | null;
  category: Category | null;
  category_id: number | null;
  tags: Tag[];
  tag_ids: number[];
  owner: number;
  is_pinned: boolean;
  is_archived: boolean;
  view_count: number;
  word_count: number;
  reading_time: number;
  created_at: string;
  updated_at: string;
  archived_at: string | null;
}

export interface NoteListItem {
  id: number;
  title: string;
  slug: string;
  cover_image: string | null;
  plain_text: string | null;
  category_name: string | null;
  tag_names: string[];
  is_pinned: boolean;
  is_archived: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export interface CreateNoteParams {
  title: string;
  content: string;
  cover_image?: string;
  category_id?: number;
  tag_ids?: number[];
  is_pinned?: boolean;
}

export interface UpdateNoteParams {
  title?: string;
  content?: string;
  cover_image?: string;
  category_id?: number;
  tag_ids?: number[];
  is_pinned?: boolean;
}

export interface NoteFilters {
  archived?: boolean;
  category?: number;
  tag?: number;
  order?: string;
  page?: number;
  page_size?: number;
}
