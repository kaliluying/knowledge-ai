/**
 * 收藏类型定义
 */

export interface Collection {
  id: number;
  title: string;
  description: string;
  url: string;
  domain: string;
  favicon: string | null;
  image: string | null;
  content: string;
  html_content: string;
  is_processed: boolean;
  word_count: number;
  reading_time: number;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export interface CollectionListItem {
  id: number;
  title: string;
  description: string;
  url: string;
  domain: string;
  favicon: string | null;
  image: string | null;
  is_processed: boolean;
  word_count: number;
  reading_time: number;
  created_at: string;
}

export interface CreateCollectionParams {
  url: string;
  title?: string;
  description?: string;
  favicon?: string;
  image?: string;
}

export interface CollectionFilters {
  search?: string;
  processed?: boolean;
  order?: string;
  page?: number;
  page_size?: number;
}
