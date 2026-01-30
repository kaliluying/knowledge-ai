/**
 * 知识图谱状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { graphApi } from '@/api';
import type { GraphNode, GraphLink } from '@/types';

interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export const useGraphStore = defineStore('graph', () => {
  // 状态
  const graphData = ref<GraphData>({ nodes: [], links: [] });
  const selectedNode = ref<GraphNode | null>(null);
  const relatedData = ref<GraphData | null>(null);
  const isLoading = ref(false);
  const isSimulationRunning = ref(false);

  // 计算属性
  const nodes = computed(() => graphData.value.nodes);
  const links = computed(() => graphData.value.links);
  const nodeCount = computed(() => nodes.value.length);
  const linkCount = computed(() => links.value.length);

  // 按类型分组节点
  const nodesByType = computed(() => {
    const result: Record<string, GraphNode[]> = {};
    nodes.value.forEach((node) => {
      const type = node.type || 'unknown';
      if (!result[type]) {
        result[type] = [];
      }
      result[type].push(node);
    });
    return result;
  });

  // 初始化示例数据
  function initSampleData() {
    const now = new Date().toISOString();
    const sampleNodes: GraphNode[] = [
      { id: 1, name: '笔记 1', type: 'note', value: 20, created_at: now },
      { id: 2, name: '笔记 2', type: 'note', value: 18, created_at: now },
      { id: 3, name: '标签: Python', type: 'tag', value: 16, created_at: now },
      { id: 4, name: '分类: 技术', type: 'category', value: 22, created_at: now },
      { id: 5, name: '标签: Vue', type: 'tag', value: 14, created_at: now },
    ];

    const sampleLinks: GraphLink[] = [
      { id: 1, source: 1, target: 3, type: 'related', strength: 1 },
      { id: 2, source: 1, target: 4, type: 'related', strength: 1 },
      { id: 3, source: 2, target: 3, type: 'related', strength: 1 },
      { id: 4, source: 1, target: 2, type: 'related', strength: 1 },
    ];

    graphData.value = { nodes: sampleNodes, links: sampleLinks };
  }

  // 获取图谱数据
  async function fetchGraphData() {
    isLoading.value = true;
    try {
      const response = await graphApi.getGraphData();
      if (response?.data) {
        graphData.value = response.data;
        return response.data;
      }
      return { nodes: [], links: [] };
    } catch (error) {
      console.error('获取图谱数据失败:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  // 获取相关节点
  async function fetchRelatedNodes(nodeId: number) {
    isLoading.value = true;
    try {
      const response = await graphApi.getRelatedNodes(nodeId);
      if (response?.data) {
        relatedData.value = response.data;
        return response.data;
      }
      return null;
    } catch (error) {
      console.error('获取相关节点失败:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  // 选择节点
  function selectNode(node: GraphNode | null) {
    selectedNode.value = node;
  }

  // 创建链接
  async function createLink(sourceId: number, targetId: number, type = 'related') {
    try {
      const response = await graphApi.createLink(sourceId, targetId, type);
      // response.data 是 {code, message, data: GraphLink}
      if (response?.data && !Array.isArray(response.data) && response.data.data) {
        const newLink = response.data.data;
        graphData.value.links.push(newLink);
        return { success: true, data: newLink };
      }
      return { success: false };
    } catch (error) {
      console.error('创建链接失败:', error);
      return { success: false };
    }
  }

  // 删除链接
  async function deleteLink(linkId: number) {
    try {
      await graphApi.deleteLink(linkId);
      graphData.value.links = links.value.filter(l => l.id !== linkId);
      return { success: true };
    } catch (error) {
      console.error('删除链接失败:', error);
      return { success: false };
    }
  }

  // 添加节点（用于本地更新）
  function addNode(node: GraphNode) {
    if (!nodes.value.find(n => n.id === node.id)) {
      graphData.value.nodes.push(node);
    }
  }

  // 添加链接（用于本地更新）
  function addLink(link: GraphLink) {
    if (!links.value.find(l => l.id === link.id)) {
      graphData.value.links.push(link);
    }
  }

  // 移除节点
  function removeNode(nodeId: number) {
    graphData.value.nodes = nodes.value.filter(n => n.id !== nodeId);
    graphData.value.links = links.value.filter(l => l.source !== nodeId && l.target !== nodeId);
  }

  // 开始模拟
  function startSimulation() {
    isSimulationRunning.value = true;
  }

  // 停止模拟
  function stopSimulation() {
    isSimulationRunning.value = false;
  }

  // 重置
  function reset() {
    graphData.value = { nodes: [], links: [] };
    selectedNode.value = null;
    relatedData.value = null;
    isLoading.value = false;
    isSimulationRunning.value = false;
  }

  function clearRelatedData() {
    relatedData.value = null;
  }

  return {
    graphData,
    selectedNode,
    relatedData,
    isLoading,
    isSimulationRunning,
    nodes,
    links,
    nodeCount,
    linkCount,
    nodesByType,
    initSampleData,
    fetchGraphData,
    fetchRelatedNodes,
    selectNode,
    createLink,
    deleteLink,
    addNode,
    addLink,
    removeNode,
    startSimulation,
    stopSimulation,
    reset,
    clearRelatedData,
  };
});
