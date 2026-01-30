/**
 * 分类类型定义 (树形结构)
 */

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  color: string;
  icon: string | null;
  parent: number | null;
  parent_id?: number | null;
  owner: number;
  is_active: boolean;
  sort_order: number;
  level: number;
  children_count?: number;
  notes_count?: number;
  created_at: string;
  updated_at: string;
}

export interface CategoryTreeItem extends Omit<Category, 'children'> {
  children: CategoryTreeItem[];
  value: number;
  label: string;
}

export interface CreateCategoryParams {
  name: string;
  description?: string;
  color?: string;
  icon?: string;
  parent_id?: number;
  sort_order?: number;
}

export interface UpdateCategoryParams {
  name?: string;
  description?: string;
  color?: string;
  icon?: string;
  parent?: number;
  is_active?: boolean;
  sort_order?: number;
}
