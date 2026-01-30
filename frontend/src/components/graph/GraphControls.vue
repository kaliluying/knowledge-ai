<script setup lang="ts">
import { ref, watch } from 'vue';
import { useGraphStore } from '@/stores/graph';

interface Props {
  showZoom?: boolean;
  showFit?: boolean;
  showFilter?: boolean;
  activeType?: string | null;
  activeLayout?: string;
}

const props = withDefaults(defineProps<Props>(), {
  showZoom: true,
  showFit: true,
  showFilter: true,
  activeType: null,
  activeLayout: 'force',
});

const emit = defineEmits<{
  zoomIn: [];
  zoomOut: [];
  fitToView: [];
  reset: [];
  filterChange: [type: string | null];
  layoutChange: [layout: string];
}>();

const graphStore = useGraphStore();

const selectedType = ref<string | null>(null);
const layoutOptions = ['force', 'circular', 'grid'];
const selectedLayout = ref('force');

selectedType.value = props.activeType ?? null;
selectedLayout.value = props.activeLayout ?? 'force';

watch(() => props.activeType, (value) => {
  selectedType.value = value ?? null;
});

watch(() => props.activeLayout, (value) => {
  selectedLayout.value = value ?? 'force';
});

const typeOptions = [
  { value: null, label: '全部' },
  { value: 'note', label: '笔记', icon: '📝' },
  { value: 'category', label: '分类', icon: '📁' },
  { value: 'tag', label: '标签', icon: '🏷️' },
];

const zoomIn = () => emit('zoomIn');
const zoomOut = () => emit('zoomOut');
const fitToView = () => emit('fitToView');
const resetView = () => emit('reset');

const handleTypeChange = (type: string | null) => {
  selectedType.value = type;
  emit('filterChange', type);
};

const handleLayoutChange = (layout: string) => {
  selectedLayout.value = layout;
  emit('layoutChange', layout);
};
</script>

<template>
  <div class="graph-controls">
    <!-- 缩放控制 -->
    <div v-if="showZoom" class="control-group">
      <button class="control-btn" title="放大" @click="zoomIn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35M11 8v6M8 11h6" />
        </svg>
      </button>
      <button class="control-btn" title="缩小" @click="zoomOut">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35M8 11h6" />
        </svg>
      </button>
    </div>

    <!-- 视图控制 -->
    <div v-if="showFit" class="control-group">
      <button class="control-btn" title="适应视图" @click="fitToView">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3" />
        </svg>
      </button>
      <button class="control-btn" title="重置视图" @click="resetView">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
          <path d="M3 3v5h5" />
        </svg>
      </button>
    </div>

    <!-- 筛选 -->
    <div v-if="showFilter" class="control-group">
      <div class="filter-pills">
        <button
          v-for="type in typeOptions"
          :key="type.value ?? 'all'"
          class="filter-pill"
          :class="{ active: selectedType === type.value }"
          @click="handleTypeChange(type.value)"
        >
          {{ type.icon }} {{ type.label }}
        </button>
      </div>
    </div>

    <!-- 布局选择 -->
    <div class="control-group">
      <select v-model="selectedLayout" class="layout-select" @change="handleLayoutChange($event.target.value)">
        <option v-for="layout in layoutOptions" :key="layout" :value="layout">
          {{ layout === 'force' ? '力导向' : layout === 'circular' ? '环形' : '网格' }}
        </option>
      </select>
    </div>

    <!-- 统计信息 -->
    <div class="stats">
      <span class="stat-item">
        <strong>{{ graphStore.nodeCount }}</strong> 节点
      </span>
      <span class="stat-item">
        <strong>{{ graphStore.linkCount }}</strong> 链接
      </span>
    </div>
  </div>
</template>

<style scoped>
.graph-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.control-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  background: #f3f4f6;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:hover {
  background: #e5e7eb;
  color: #1f2937;
}

.control-btn svg {
  width: 18px;
  height: 18px;
}

.filter-pills {
  display: flex;
  gap: 4px;
}

.filter-pill {
  padding: 6px 12px;
  border: none;
  border-radius: 20px;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-pill:hover {
  background: #e5e7eb;
}

.filter-pill.active {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.layout-select {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  background: white;
  cursor: pointer;
  outline: none;
}

.layout-select:focus {
  border-color: #8b5cf6;
}

.stats {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.stat-item {
  font-size: 13px;
  color: #6b7280;
}

.stat-item strong {
  color: #1f2937;
  font-weight: 600;
}

@media (max-width: 768px) {
  .graph-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats {
    margin-left: 0;
    margin-top: 8px;
  }
}
</style>
