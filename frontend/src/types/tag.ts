/**
 * 标签类型定义
 */

export interface Tag {
  id: number;
  name: string;
  slug: string;
  color: string;
  description: string | null;
  owner: number;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

export interface TagListItem {
  id: number;
  name: string;
  slug: string;
  color: string;
  usage_count: number;
}

export interface CreateTagParams {
  name: string;
  color?: string;
  description?: string;
}

export interface UpdateTagParams {
  name?: string;
  color?: string;
  description?: string;
}

export interface BulkCreateTagsParams {
  names: string[];
}
