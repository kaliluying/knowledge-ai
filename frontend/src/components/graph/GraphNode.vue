<script setup lang="ts">
import { computed } from 'vue';
import type { GraphNode } from '@/types';
import { useGraphStore } from '@/stores/graph';

interface Props {
  node: GraphNode;
  size?: number;
  selected?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 30,
  selected: false,
});

const emit = defineEmits<{
  click: [node: GraphNode];
  dragStart: [node: GraphNode];
  dragEnd: [node: GraphNode];
}>();

const graphStore = useGraphStore();

const isSelected = computed(() => 
  props.selected || graphStore.selectedNode?.id === props.node.id
);

const nodeColor = computed(() => {
  const colors: Record<string, string> = {
    note: '#8b5cf6',
    category: '#10b981',
    tag: '#f59e0b',
  };
  return colors[props.node.type] || '#8b5cf6';
});

const handleClick = () => {
  emit('click', props.node);
};

const handleDragStart = (e: DragEvent) => {
  e.dataTransfer?.setData('nodeId', String(props.node.id));
  emit('dragStart', props.node);
};

const handleDragEnd = () => {
  emit('dragEnd', props.node);
};
</script>

<template>
  <div
    class="graph-node"
    :class="{ selected: isSelected }"
    :style="{ '--node-color': nodeColor, '--node-size': `${size}px` }"
    @click="handleClick"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
  >
    <div class="node-circle">
      <span class="node-icon">
        {{ node.type === 'note' ? '📝' : node.type === 'category' ? '📁' : '🏷️' }}
      </span>
    </div>
    <span class="node-label">{{ node.name }}</span>
  </div>
</template>

<style scoped>
.graph-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.graph-node:hover {
  transform: scale(1.05);
}

.graph-node.selected .node-circle {
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3);
  border-color: var(--node-color);
}

.node-circle {
  width: var(--node-size);
  height: var(--node-size);
  border-radius: 50%;
  background: linear-gradient(135deg, var(--node-color) 0%, var(--node-color)dd 100%);
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.node-icon {
  font-size: calc(var(--node-size) * 0.5);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.node-label {
  font-size: 12px;
  color: #374151;
  font-weight: 500;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
}
</style>
