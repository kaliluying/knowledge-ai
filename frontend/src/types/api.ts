/**
 * API 响应类型定义
 */

export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data?: T;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  code: number;
  message: string;
  errors?: Record<string, string[]>;
}

/**
 * 通用列表查询参数
 */
export interface ListQueryParams {
  page?: number;
  page_size?: number;
  search?: string;
  ordering?: string;
}

/**
 * 笔记列表查询参数
 */
export interface NoteListQueryParams extends ListQueryParams {
  archived?: string;
  category?: string;
  tag?: string;
}

/**
 * 标签搜索查询参数
 */
export interface TagSearchQueryParams extends ListQueryParams {
  q: string;
}
