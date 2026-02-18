/**
 * 知识图谱类型定义 (D3.js 可视化)
 */

export interface GraphNode {
  id: string | number;
  original_id?: number;
  name: string;
  type: 'note' | 'category' | 'tag';
  source?: 'sync' | 'manual';
  is_locked?: boolean;
  value: number;
  category?: string;
  tags?: string[];
  created_at: string;
}

export interface GraphLink {
  id: string | number;
  source: string | number;
  target: string | number;
  type: string;
  strength: number;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

// D3 simulation types - will be properly typed when D3 is implemented
export interface GraphNodeDatum {
  id: string | number;
  original_id?: number;
  name: string;
  type: 'note' | 'category' | 'tag';
  source?: 'sync' | 'manual';
  is_locked?: boolean;
  value: number;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
  vx?: number;
  vy?: number;
  index?: number;
}

export interface GraphLinkDatum {
  id: string | number;
  source: GraphNodeDatum;
  target: GraphNodeDatum;
  type: string;
  strength: number;
}
