/**
 * 知识图谱 API
 */

import { api } from './index';
import type { GraphData, GraphNode, GraphLink } from '@/types';

export const graphApi = {
  // 获取完整图谱数据
  async getGraphData(mode: 'hybrid' | 'sync_only' | 'manual_only' = 'hybrid') {
    const response = await api.get<{ code: number; message: string; data: GraphData }>(
      '/graph/graph/',
      { params: { mode } }
    );
    return response.data;
  },

  // 获取指定节点的相关节点
  async getRelatedNodes(nodeId: string | number) {
    const response = await api.get<{ code: number; message: string; data: { nodes: GraphNode[]; links: GraphLink[] } }>(
      `/graph/related/${nodeId}/`
    );
    return response.data;
  },

  // 创建链接
  async createLink(sourceId: number, targetId: number, type = 'related') {
    const response = await api.post<{ code: number; message: string; data: GraphLink }>(
      '/graph/links/',
      { source: sourceId, target: targetId, link_type: type }
    );
    return response.data;
  },

  // 删除链接
  async deleteLink(linkId: number) {
    const response = await api.delete(`/graph/links/${linkId}/`);
    return response.data;
  },
};
