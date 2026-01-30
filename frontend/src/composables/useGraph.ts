/**
 * 知识图谱操作组合式函数
 */

import { computed } from 'vue';
import { useGraphStore } from '@/stores/graph';
import type { GraphNode, GraphLink } from '@/types';

export function useGraph() {
  const graphStore = useGraphStore();

  // 状态
  const nodes = computed(() => graphStore.nodes);
  const links = computed(() => graphStore.links);
  const isLoading = computed(() => graphStore.isLoading);
  const selectedNode = computed(() => graphStore.selectedNode);

  // 方法
  async function fetchGraphData() {
    return graphStore.fetchGraphData();
  }

  async function fetchRelatedNodes(nodeId: number) {
    return graphStore.fetchRelatedNodes(nodeId);
  }

  function selectNode(node: GraphNode | null) {
    graphStore.selectNode(node);
  }

  function clearGraph() {
    graphStore.reset();
  }

  return {
    nodes,
    links,
    isLoading,
    selectedNode,
    fetchGraphData,
    fetchRelatedNodes,
    selectNode,
    clearGraph,
  };
}
