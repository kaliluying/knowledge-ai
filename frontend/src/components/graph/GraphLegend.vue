<script setup lang="ts">
interface LegendItem {
  type: string;
  label: string;
  icon: string;
  color: string;
}

const legendItems: LegendItem[] = [
  { type: 'note', label: '笔记', icon: '📝', color: '#8b5cf6' },
  { type: 'category', label: '分类', icon: '📁', color: '#10b981' },
  { type: 'tag', label: '标签', icon: '🏷️', color: '#f59e0b' },
];

interface Props {
  showCount?: boolean;
  counts?: Record<string, number>;
}

withDefaults(defineProps<Props>(), {
  showCount: false,
});
</script>

<template>
  <div class="graph-legend">
    <h4 class="legend-title">图例</h4>
    <ul class="legend-list">
      <li
        v-for="item in legendItems"
        :key="item.type"
        class="legend-item"
        :style="{ '--item-color': item.color }"
      >
        <span class="legend-icon">{{ item.icon }}</span>
        <span class="legend-label">{{ item.label }}</span>
        <span v-if="showCount && counts" class="legend-count">
          {{ counts[item.type] || 0 }}
        </span>
      </li>
    </ul>

    <div class="legend-hint">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 16v-4M12 8h.01" />
      </svg>
      <span>拖拽节点可移动</span>
    </div>
  </div>
</template>

<style scoped>
.graph-legend {
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.legend-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 12px 0;
}

.legend-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 50%;
  font-size: 14px;
}

.legend-label {
  flex: 1;
  font-size: 13px;
  color: #374151;
}

.legend-count {
  font-size: 12px;
  color: #9ca3af;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 10px;
}

.legend-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
  font-size: 12px;
  color: #9ca3af;
}

.legend-hint svg {
  width: 14px;
  height: 14px;
}
</style>
