<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import * as d3 from 'd3';
import type { GraphNode, GraphLink, GraphNodeDatum, GraphLinkDatum } from '@/types';
import { useGraphStore } from '@/stores/graph';

interface Props {
  width?: number;
  height?: number;
  interactive?: boolean;
  showLabels?: boolean;
  nodeSizeRange?: [number, number];
  nodes?: GraphNode[];
  links?: GraphLink[];
  layout?: 'force' | 'circular' | 'grid';
}

const props = withDefaults(defineProps<Props>(), {
  width: 800,
  height: 600,
  interactive: true,
  showLabels: true,
  nodeSizeRange: () => [15, 40],
  nodes: undefined,
  links: undefined,
  layout: 'force',
});

const emit = defineEmits<{
  nodeClick: [node: GraphNode];
  nodeDragStart: [node: GraphNode];
  nodeDragEnd: [node: GraphNode];
  linkClick: [link: GraphLink];
  canvasClick: [];
}>();

const containerRef = ref<HTMLDivElement | null>(null);
const svgRef = ref<SVGSVGElement | null>(null);
const graphStore = useGraphStore();
const containerSize = ref({ width: props.width, height: props.height });

const nodes = computed(() => props.nodes ?? graphStore.nodes);
const links = computed(() => props.links ?? graphStore.links);
const isLoading = computed(() => graphStore.isLoading);

let simulation: d3.Simulation<GraphNodeDatum, GraphLinkDatum> | null = null;
let zoomBehavior: d3.ZoomBehavior<SVGSVGElement, unknown> | null = null;
const updatePositionsRef = ref<(() => void) | null>(null);
let resizeObserver: ResizeObserver | null = null;
let draggingNode: GraphNodeDatum | null = null;

const nodeColors = {
  note: '#8b5cf6',
  category: '#10b981',
  tag: '#f59e0b',
};

const initializeSimulation = () => {
  if (!svgRef.value) return;

  const width = containerRef.value?.clientWidth || props.width;
  const height = containerRef.value?.clientHeight || props.height;
  containerSize.value = { width, height };

  simulation?.stop();
  simulation = null;

  if (nodes.value.length === 0) {
    d3.select(svgRef.value).selectAll('*').remove();
    simulation?.stop();
    return;
  }

  const minSize = props.nodeSizeRange[0];
  const maxSize = props.nodeSizeRange[1];

  // 准备数据
  const nodeData: GraphNodeDatum[] = nodes.value.map(node => ({
    ...node,
    value: minSize + (node.value / 100) * (maxSize - minSize),
  }));

  const linkData: GraphLinkDatum[] = links.value.map(link => {
    const source = nodeData.find(n => n.id === link.source);
    const target = nodeData.find(n => n.id === link.target);
    if (!source || !target) {
      return null;
    }
    return {
      ...link,
      source,
      target,
    };
  }).filter(Boolean) as GraphLinkDatum[];

  const centerX = width / 2;
  const centerY = height / 2;

  // 创建 SVG 内容
  const svg = d3.select(svgRef.value);
  svg.selectAll('*').remove();

  // 创建箭头标记
  svg.append('defs').selectAll('marker')
    .data(['end'])
    .enter()
    .append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#9ca3af');

  // 创建连线
  const linkGroup = svg.append('g').attr('class', 'links');
  const linksSelection = linkGroup.selectAll('line')
    .data(linkData)
    .enter()
    .append('line')
    .attr('class', 'link')
    .attr('stroke', '#9ca3af')
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.6);
    // .attr('marker-end', 'url(#arrow)'); // 移除箭头

  // 创建节点组
  const nodeGroup = svg.append('g').attr('class', 'nodes');
  const nodesSelection = nodeGroup.selectAll('g')
    .data(nodeData)
    .enter()
    .append('g')
    .attr('class', 'node')
    .style('cursor', props.interactive ? 'pointer' : 'default')
    .call(d3.drag<SVGGElement, GraphNodeDatum>()
      .on('start', dragStarted)
      .on('drag', dragged)
      .on('end', dragEnded));

  // 节点圆
  nodesSelection.append('circle')
    .attr('r', d => d.value)
    .attr('fill', d => nodeColors[d.type] || '#8b5cf6')
    .attr('stroke', '#fff')
    .attr('stroke-width', 2);

  // 节点标签
  if (props.showLabels) {
    nodesSelection.append('text')
      .attr('dy', d => d.value + 15)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#374151')
      .text(d => d.name.length > 10 ? d.name.substring(0, 10) + '...' : d.name);
  }

  // 点击事件
  if (props.interactive) {
    nodesSelection.on('click', (event, d) => {
      event.stopPropagation();
      emit('nodeClick', d as unknown as GraphNode);
      graphStore.selectNode(d as unknown as GraphNode);
    });

    linksSelection.on('click', (event, d) => {
      event.stopPropagation();
      emit('linkClick', d as unknown as GraphLink);
    });

    svg.on('click', () => {
      emit('canvasClick');
      graphStore.selectNode(null);
    });
  }

  const updatePositions = () => {
    linksSelection
      .attr('x1', d => (d.source as GraphNodeDatum).x || 0)
      .attr('y1', d => (d.source as GraphNodeDatum).y || 0)
      .attr('x2', d => (d.target as GraphNodeDatum).x || 0)
      .attr('y2', d => (d.target as GraphNodeDatum).y || 0);

    nodesSelection.attr('transform', d => {
      const x = d.x || 0;
      const y = d.y || 0;
      return `translate(${x},${y})`;
    });
  };

  updatePositionsRef.value = updatePositions;

  const applyStaticLayout = (layout: 'circular' | 'grid') => {
    const count = nodeData.length;
    if (count === 0) return;

    if (layout === 'circular') {
      const radius = Math.min(width, height) * 0.35;
      const step = (Math.PI * 2) / count;
      nodeData.forEach((node, index) => {
        const angle = step * index;
        node.x = centerX + radius * Math.cos(angle);
        node.y = centerY + radius * Math.sin(angle);
      });
      return;
    }

    const columns = Math.max(2, Math.ceil(Math.sqrt(count)));
    const rows = Math.ceil(count / columns);
    const xSpacing = width / (columns + 1);
    const ySpacing = height / (rows + 1);

    nodeData.forEach((node, index) => {
      const row = Math.floor(index / columns);
      const col = index % columns;
      node.x = xSpacing * (col + 1);
      node.y = ySpacing * (row + 1);
    });
  };

  if (props.layout === 'force') {
    simulation = d3.forceSimulation<GraphNodeDatum>(nodeData)
      .alphaDecay(0.02)  // 更慢衰减，拖动时更流畅
      .velocityDecay(0.3)  // 减少速度衰减，跟手
      .force('link', d3.forceLink<GraphNodeDatum, GraphLinkDatum>(linkData)
        .id(d => d.id)
        .distance(120)
        .strength(0.3))  // 减弱链接力
      .force('charge', d3.forceManyBody().strength(-150))  // 减弱排斥力
      .force('center', d3.forceCenter(centerX, centerY).strength(0.05))  // 减弱中心力
      .force('collision', d3.forceCollide()
        .radius(d => (d.value || 20) + 15)
        .strength(0.5));  // 减弱碰撞力

    // 添加边界约束力，防止节点飞出容器
    const padding = 60;
    simulation.force('box', () => {
      nodeData.forEach(node => {
        // 拖动中的节点不应用边界约束
        if (node === draggingNode) return;
        if (node.x === undefined || node.y === undefined) return;

        // 约束 x 坐标（柔和处理）
        if (node.x < padding) {
          node.x = padding + (node.x - padding) * 0.1;
        } else if (node.x > width - padding) {
          node.x = width - padding + (node.x - (width - padding)) * 0.1;
        }

        // 约束 y 坐标（柔和处理）
        if (node.y < padding) {
          node.y = padding + (node.y - padding) * 0.1;
        } else if (node.y > height - padding) {
          node.y = height - padding + (node.y - (height - padding)) * 0.1;
        }
      });
    });

    simulation.on('tick', updatePositions);
  } else {
    simulation?.stop();
    simulation = null;
    applyStaticLayout(props.layout);
    updatePositions();
  }

  // 添加缩放
  zoomBehavior = d3.zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {
      svg.selectAll('g').attr('transform', event.transform);
    });

  svg.call(zoomBehavior);
};

function dragStarted(event: d3.D3DragEvent<SVGGElement, GraphNodeDatum, GraphNodeDatum>, d: GraphNodeDatum) {
  if (!event.active && simulation) {
    simulation.alphaTarget(0.5).restart();
  }
  // 保存原始位置
  d.fx = event.x;
  d.fy = event.y;
  d.x = event.x;
  d.y = event.y;
  draggingNode = d;
  emit('nodeDragStart', d as unknown as GraphNode);
}

function dragged(event: d3.D3DragEvent<SVGGElement, GraphNodeDatum, GraphNodeDatum>, d: GraphNodeDatum) {
  // 实时跟随鼠标
  d.fx = event.x;
  d.fy = event.y;
  d.x = event.x;
  d.y = event.y;

  // 保持 simulation 活跃
  if (simulation) {
    simulation.alpha(1).restart();
  }

  // 立即更新视图
  if (updatePositionsRef.value) {
    updatePositionsRef.value();
  }
}

function dragEnded(event: d3.D3DragEvent<SVGGElement, GraphNodeDatum, GraphNodeDatum>, d: GraphNodeDatum) {
  if (!event.active && simulation) {
    simulation.alphaTarget(0);
  }
  if (simulation) {
    d.fx = null;
    d.fy = null;
  }
  draggingNode = null;
  emit('nodeDragEnd', d as unknown as GraphNode);
}

const resetZoom = () => {
  if (svgRef.value && zoomBehavior) {
    d3.select(svgRef.value).transition().duration(750).call(
      zoomBehavior.transform,
      d3.zoomIdentity
    );
  }
};

const fitToView = () => {
  if (!svgRef.value) return;
  
  const svg = d3.select(svgRef.value);
  const bounds = svg.node()?.getBBox();
  
  if (bounds) {
    const fullWidth = containerSize.value.width || props.width;
    const fullHeight = containerSize.value.height || props.height;
    const width = bounds.width;
    const height = bounds.height;
    const midX = bounds.x + width / 2;
    const midY = bounds.y + height / 2;

    if (width === 0 || height === 0) return;

    const scale = 0.9 / Math.max(width / fullWidth, height / fullHeight);
    const translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

    svg.transition().duration(750).call(
      zoomBehavior!.transform,
      d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
    );
  }
};

const zoomIn = () => {
  if (svgRef.value && zoomBehavior) {
    d3.select(svgRef.value).transition().duration(250).call(
      zoomBehavior.scaleBy,
      1.2
    );
  }
};

const zoomOut = () => {
  if (svgRef.value && zoomBehavior) {
    d3.select(svgRef.value).transition().duration(250).call(
      zoomBehavior.scaleBy,
      0.8
    );
  }
};

onMounted(() => {
  if (containerRef.value) {
    resizeObserver = new ResizeObserver(() => {
      initializeSimulation();
    });
    resizeObserver.observe(containerRef.value);
  }
  initializeSimulation();
});

watch([nodes, links, () => props.layout], () => {
  initializeSimulation();
}, { deep: true });

onUnmounted(() => {
  resizeObserver?.disconnect();
  simulation?.stop();
});

defineExpose({
  resetZoom,
  fitToView,
  zoomIn,
  zoomOut,
});
</script>

<template>
  <div ref="containerRef" class="graph-canvas">
    <svg
      ref="svgRef"
      :width="containerSize.width || width"
      :height="containerSize.height || height"
      class="graph-svg"
    ></svg>

    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>

    <div v-if="nodes.length === 0 && !isLoading" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 2a10 10 0 0 1 10 10" />
        <path d="M12 12L12 22" />
      </svg>
      <p>暂无图谱数据</p>
    </div>
  </div>
</template>

<style scoped>
.graph-canvas {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 16px;
  overflow: hidden;
}

.graph-svg {
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.8);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #9ca3af;
}

.empty-state svg {
  width: 64px;
  height: 64px;
}

.empty-state p {
  font-size: 14px;
}
</style>
