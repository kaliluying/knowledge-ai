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
let resizeObserver: ResizeObserver | null = null;
let linksSelection: d3.Selection<SVGLineElement, GraphLinkDatum, SVGGElement, unknown> | null = null;
let nodesSelection: d3.Selection<SVGGElement, GraphNodeDatum, SVGGElement, unknown> | null = null;
let nodeData: GraphNodeDatum[] = [];
const nodePositions = new Map<string | number, { x: number; y: number }>();
let _isDragging = false;
let _dragMoved = false;
let _draggingNodeId: string | number | null = null;

const nodeColors: Record<string, string> = {
  note: '#8b5cf6',
  category: '#10b981',
  tag: '#f59e0b',
};

const nodeBorderColors: Record<string, string> = {
  sync: '#ffffff',
  manual: '#ef4444',
};

function updatePositions() {
  if (!linksSelection || !nodesSelection) return;

  nodeData.forEach(node => {
    if (node.x !== undefined && node.y !== undefined) {
      nodePositions.set(node.id, { x: node.x, y: node.y });
    }
  });

  // 更新线段
  linksSelection
    .attr('x1', d => (d.source as GraphNodeDatum).x ?? 0)
    .attr('y1', d => (d.source as GraphNodeDatum).y ?? 0)
    .attr('x2', d => (d.target as GraphNodeDatum).x ?? 0)
    .attr('y2', d => (d.target as GraphNodeDatum).y ?? 0);

  // 更新节点：跳过被拖拽的节点（保留 drag 设置的位置）
  nodesSelection.each(function(d) {
    if (d.id === _draggingNodeId) {
      return; // 跳过被拖拽的节点
    }
    d3.select(this).attr('transform', `translate(${d.x ?? 0},${d.y ?? 0})`);
  });
}

const initializeSimulation = () => {
  if (!svgRef.value) return;

  const width = containerRef.value?.clientWidth || props.width;
  const height = containerRef.value?.clientHeight || props.height;
  containerSize.value = { width, height };

  simulation?.stop();
  simulation = null;
  linksSelection = null;
  nodesSelection = null;

  if (nodes.value.length === 0) {
    d3.select(svgRef.value).selectAll('*').remove();
    nodePositions.clear();
    return;
  }

  const minSize = props.nodeSizeRange[0];
  const maxSize = props.nodeSizeRange[1];

  nodeData = nodes.value.map(node => {
    const saved = nodePositions.get(node.id);
    return {
      ...node,
      x: saved?.x,
      y: saved?.y,
      value: minSize + (node.value / 100) * (maxSize - minSize),
    };
  });

  const linkData: GraphLinkDatum[] = links.value.map(link => {
    const source = nodeData.find(n => n.id === link.source);
    const target = nodeData.find(n => n.id === link.target);
    if (!source || !target) return null;
    return { ...link, source, target };
  }).filter(Boolean) as GraphLinkDatum[];

  const centerX = width / 2;
  const centerY = height / 2;

  const svg = d3.select(svgRef.value);
  svg.selectAll('*').remove();

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

  const container = svg.append('g').attr('class', 'graph-container');

  const linkGroup = container.append('g').attr('class', 'links');
  linksSelection = linkGroup.selectAll('line')
    .data(linkData)
    .enter()
    .append('line')
    .attr('class', 'link')
    .attr('stroke', '#9ca3af')
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.6);

  const nodeGroup = container.append('g').attr('class', 'nodes');

  nodesSelection = nodeGroup.selectAll('g')
    .data(nodeData)
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('role', 'button')
    .attr('aria-label', d => `node-${d.id}`)
    .style('cursor', props.interactive ? 'pointer' : 'default')
    .style('touch-action', 'none');

  const dragBehavior = d3.drag<SVGGElement, GraphNodeDatum>()
    .on('start', function(event, d) {
      event.sourceEvent.stopPropagation();
      _isDragging = true;
      _dragMoved = false;
      _draggingNodeId = d.id;
      if (!event.active && simulation) simulation.alphaTarget(0.02).restart();
      d.fx = d.x;
      d.fy = d.y;
      emit('nodeDragStart', d as unknown as GraphNode);
    })
    .on('drag', function(event, d) {
      _dragMoved = true;
      d.fx = event.x;
      d.fy = event.y;
      // 手动更新 DOM
      d3.select(this).attr('transform', `translate(${event.x},${event.y})`);
    })
    .on('end', function(event, d) {
      if (!event.active && simulation) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
      _draggingNodeId = null;
      if (_dragMoved) {
        setTimeout(() => { _isDragging = false; }, 100);
      } else {
        _isDragging = false;
      }
      emit('nodeDragEnd', d as unknown as GraphNode);
    });

  nodesSelection.call(dragBehavior);

  nodesSelection.append('circle')
    .attr('r', d => d.value)
    .attr('fill', d => nodeColors[d.type] || '#8b5cf6')
    .attr('stroke', d => nodeBorderColors[d.source || 'sync'] || '#fff')
    .attr('stroke-width', d => d.source === 'manual' ? 3 : 2);

  if (props.showLabels) {
    nodesSelection.append('text')
      .attr('dy', d => d.value + 15)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#374151')
      .text(d => d.name.length > 10 ? d.name.substring(0, 10) + '...' : d.name);
  }

  if (props.interactive && nodesSelection && linksSelection) {
    nodesSelection.on('click', (event, d) => {
      if (_isDragging) return;
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
      .alphaDecay(0.02)
      .velocityDecay(0.3)
      .force('link', d3.forceLink<GraphNodeDatum, GraphLinkDatum>(linkData)
        .id(d => d.id)
        .distance(120)
        .strength(0.8))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(centerX, centerY).strength(0.05))
      .force('collision', d3.forceCollide<GraphNodeDatum>()
        .radius(d => (d.value || 20) + 15)
        .strength(1)
        .iterations(3));

    simulation.on('tick', () => {
      updatePositions();
    });
  } else {
    simulation?.stop();
    simulation = null;
    applyStaticLayout(props.layout);
    updatePositions();
  }

  zoomBehavior = d3.zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.1, 4])
    .filter((event) => {
      if (event.type === 'mousedown' || event.type === 'pointerdown') {
        const target = event.target as Element;
        if (target?.closest?.('.node')) return false;
      }
      return !event.button;
    })
    .on('zoom', (event) => {
      container.attr('transform', event.transform);
    });

  svg.call(zoomBehavior);
};

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

watch([() => nodes.value.length, () => links.value.length, () => props.layout], () => {
  initializeSimulation();
});

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
