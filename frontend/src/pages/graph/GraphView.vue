<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import GraphCanvas from '@/components/graph/GraphCanvas.vue';
import GraphControls from '@/components/graph/GraphControls.vue';
import GraphLegend from '@/components/graph/GraphLegend.vue';
import { useGraphStore } from '@/stores/graph';
import type { GraphNode } from '@/types';

const graphStore = useGraphStore();
const graphCanvasRef = ref<InstanceType<typeof GraphCanvas> | null>(null);

const searchQuery = ref('');
const selectedType = ref<string | null>(null);
const errorMessage = ref('');
const relatedError = ref('');
const subgraphMode = ref(false);
const currentLayout = ref<'force' | 'circular' | 'grid'>('force');

const nodes = computed(() => graphStore.nodes);
const links = computed(() => graphStore.links);
const relatedNodes = computed(() => graphStore.relatedData?.nodes ?? []);
const relatedLinks = computed(() => graphStore.relatedData?.links ?? []);
const isLoading = computed(() => graphStore.isLoading);
const selectedNode = computed(() => graphStore.selectedNode);

const activeNodes = computed(() => (subgraphMode.value ? relatedNodes.value : nodes.value));
const activeLinks = computed(() => (subgraphMode.value ? relatedLinks.value : links.value));

const filteredNodes = computed(() => {
  let result = activeNodes.value;
  if (selectedType.value) {
    result = result.filter(node => node.type === selectedType.value);
  }

  const keyword = searchQuery.value.trim().toLowerCase();
  if (keyword) {
    result = result.filter(node => node.name.toLowerCase().includes(keyword));
  }

  return result;
});

const filteredLinks = computed(() => {
  const nodeIds = new Set(filteredNodes.value.map(node => node.id));
  return activeLinks.value.filter(link => nodeIds.has(link.source) && nodeIds.has(link.target));
});

const stats = computed(() => ({
  nodes: filteredNodes.value.length,
  links: filteredLinks.value.length,
}));

const counts = computed(() => ({
  note: activeNodes.value.filter(node => node.type === 'note').length,
  category: activeNodes.value.filter(node => node.type === 'category').length,
  tag: activeNodes.value.filter(node => node.type === 'tag').length,
}));

const hasFilters = computed(() => Boolean(selectedType.value || searchQuery.value.trim()));

const fetchGraph = async () => {
  errorMessage.value = '';
  relatedError.value = '';
  subgraphMode.value = false;
  graphStore.clearRelatedData();
  graphStore.selectNode(null);
  try {
    await graphStore.fetchGraphData();
  } catch (error) {
    errorMessage.value = '图谱数据加载失败，请稍后重试';
  }
};

const clearFilters = () => {
  selectedType.value = null;
  searchQuery.value = '';
};

const handleFilterChange = (type: string | null) => {
  selectedType.value = type;
};

const handleLayoutChange = (layout: string) => {
  if (layout === 'force' || layout === 'circular' || layout === 'grid') {
    currentLayout.value = layout;
  }
};

const handleNodeClick = async (node: GraphNode) => {
  graphStore.selectNode(node);
  relatedError.value = '';
  subgraphMode.value = true;
  try {
    const data = await graphStore.fetchRelatedNodes(node.id);
    if (!data || data.nodes.length === 0) {
      relatedError.value = '该节点暂无关联数据';
    }
  } catch (error) {
    relatedError.value = '相关子图加载失败，请稍后重试';
    subgraphMode.value = false;
  }
};

const handleCanvasClick = () => {
  graphStore.selectNode(null);
};

const handleZoomIn = () => {
  graphCanvasRef.value?.zoomIn();
};

const handleZoomOut = () => {
  graphCanvasRef.value?.zoomOut();
};

const handleFitToView = () => {
  graphCanvasRef.value?.fitToView();
};

const handleReset = () => {
  graphCanvasRef.value?.resetZoom();
};

const resetToFullGraph = () => {
  relatedError.value = '';
  subgraphMode.value = false;
  graphStore.clearRelatedData();
};

onMounted(() => {
  fetchGraph();
});
</script>

<template>
  <div class="graph-page">
    <div class="page-header">
      <div class="header-title">
        <h1>知识图谱</h1>
        <p>可视化展示你的知识网络</p>
      </div>

      <div class="header-actions">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
          <input v-model="searchQuery" type="text" placeholder="搜索节点" />
        </div>
        <button class="ghost-btn" @click="fetchGraph" :disabled="isLoading">刷新</button>
      </div>
    </div>

    <div v-if="errorMessage" class="error-banner">
      <span>{{ errorMessage }}</span>
      <button class="link-btn" @click="fetchGraph">重试</button>
    </div>

    <div v-if="subgraphMode" class="subgraph-banner">
      <span>已聚焦到：{{ selectedNode?.name || '节点' }}</span>
      <button class="link-btn" @click="resetToFullGraph">返回全图</button>
    </div>

    <div v-if="relatedError && subgraphMode" class="subgraph-hint">
      {{ relatedError }}
    </div>

    <div class="toolbar">
      <GraphControls
        :show-filter="true"
        :active-type="selectedType"
        :active-layout="currentLayout"
        @zoom-in="handleZoomIn"
        @zoom-out="handleZoomOut"
        @fit-to-view="handleFitToView"
        @reset="handleReset"
        @filter-change="handleFilterChange"
        @layout-change="handleLayoutChange"
      />

      <div v-if="hasFilters" class="filter-summary">
        <span>当前筛选：{{ stats.nodes }} 节点 / {{ stats.links }} 连接</span>
        <button class="link-btn" @click="clearFilters">清除</button>
      </div>
    </div>

    <div class="graph-layout">
      <div class="graph-main">
        <GraphCanvas
          ref="graphCanvasRef"
          :nodes="filteredNodes"
          :links="filteredLinks"
          :layout="currentLayout"
          @node-click="handleNodeClick"
          @canvas-click="handleCanvasClick"
        />
      </div>

      <aside class="graph-side">
        <GraphLegend :show-count="true" :counts="counts" />

        <div class="node-panel">
          <template v-if="selectedNode">
            <h3>节点信息</h3>
            <div class="node-row">
              <span class="label">名称</span>
              <span class="value">{{ selectedNode.name }}</span>
            </div>
            <div class="node-row">
              <span class="label">类型</span>
              <span class="value">{{ selectedNode.type }}</span>
            </div>
            <div v-if="selectedNode.category" class="node-row">
              <span class="label">分类</span>
              <span class="value">{{ selectedNode.category }}</span>
            </div>
            <div v-if="selectedNode.tags && selectedNode.tags.length" class="node-row">
              <span class="label">标签</span>
              <span class="value">{{ selectedNode.tags.join('、') }}</span>
            </div>
          </template>
          <template v-else>
            <h3>节点信息</h3>
            <p class="node-empty">点击节点查看详情</p>
          </template>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.graph-page {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.header-title h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 4px;
}

.header-title p {
  font-size: 14px;
  color: #9ca3af;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 12px;
  background: white;
  border: 1px solid #e5e7eb;
  min-width: 220px;
}

.search-box svg {
  width: 16px;
  height: 16px;
  color: #9ca3af;
}

.search-box input {
  border: none;
  outline: none;
  font-size: 14px;
  color: #374151;
  width: 100%;
}

.ghost-btn {
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
}

.ghost-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toolbar {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 12px;
  background: #f9fafb;
  color: #6b7280;
  font-size: 13px;
}

.graph-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 20px;
  align-items: start;
}

.graph-main {
  background: white;
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  padding: 16px;
}

.graph-side {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.node-panel {
  background: white;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.node-panel h3 {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.node-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #4b5563;
}

.node-row .label {
  color: #9ca3af;
}

.node-empty {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
}

.error-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #991b1b;
  border-radius: 12px;
  font-size: 13px;
}

.subgraph-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #e0f2fe;
  border: 1px solid #bae6fd;
  color: #0369a1;
  border-radius: 12px;
  font-size: 13px;
}

.subgraph-hint {
  padding: 8px 14px;
  background: #fef9c3;
  border: 1px solid #fde68a;
  color: #92400e;
  border-radius: 12px;
  font-size: 12px;
}

.link-btn {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .graph-layout {
    grid-template-columns: 1fr;
  }

  .graph-main {
    padding: 12px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    width: 100%;
  }

  .search-box {
    flex: 1;
  }
}
</style>
