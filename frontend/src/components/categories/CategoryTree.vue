<script setup lang="ts">
import { ref, computed, onMounted, defineComponent, h } from 'vue';
import type { PropType } from 'vue';
import type { CategoryTreeItem } from '@/types';
import { useCategoriesStore } from '@/stores/categories';

interface Props {
  selectedId?: number | null;
  expandable?: boolean;
  showIcon?: boolean;
  showCount?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  selectedId: null,
  expandable: true,
  showIcon: true,
  showCount: false,
});

const emit = defineEmits<{
  select: [category: CategoryTreeItem];
  toggle: [category: CategoryTreeItem];
}>();

const categoriesStore = useCategoriesStore();
const expandedIds = ref<Set<number>>(new Set());
const loading = ref(true);

const categoryTree = computed(() => categoriesStore.categoryTree);

onMounted(async () => {
  await categoriesStore.fetchCategoryTree();
  loading.value = false;
});

const isExpanded = (id: number) => expandedIds.value.has(id);

const toggleExpand = (category: CategoryTreeItem) => {
  if (isExpanded(category.id)) {
    expandedIds.value.delete(category.id);
  } else {
    expandedIds.value.add(category.id);
  }
  emit('toggle', category);
};

const selectCategory = (category: CategoryTreeItem) => {
  emit('select', category);
};



const TreeNode = defineComponent({
  name: 'TreeNode',
  props: {
    category: {
      type: Object as PropType<CategoryTreeItem>,
      required: true,
    },
    selectedId: {
      type: Number as PropType<number | null>,
      default: null,
    },
    expandedIds: {
      type: Set as PropType<Set<number>>,
      required: true,
    },
    level: {
      type: Number,
      default: 0,
    },
    expandable: {
      type: Boolean,
      default: true,
    },
    showIcon: {
      type: Boolean,
      default: true,
    },
    showCount: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['select', 'toggle'],
  setup(props, { emit }) {
    const isExpanded = computed(() => props.expandedIds.has(props.category.id));
    const hasChildren = computed(() => props.category.children && props.category.children.length > 0);

    const toggleExpand = () => {
      emit('toggle', props.category);
    };

    const selectCategory = () => {
      emit('select', props.category);
    };

    const getIndent = (level: number) => {
      return level * 20;
    };

    return (): any => {
      const indent = getIndent(props.level);

      return h('li', { class: 'tree-node' }, [
        h('div', {
          class: ['node-content', { selected: props.selectedId === props.category.id }],
          style: { paddingLeft: `${indent + 12}px` },
          onClick: selectCategory,
        }, [
          // 展开/折叠按钮
          h('span', {
            class: 'expand-btn',
            onClick: (e: Event) => {
              e.stopPropagation();
              if (props.expandable && hasChildren.value) {
                toggleExpand();
              }
            },
          }, [
            hasChildren.value
              ? h('svg', {
                  viewBox: '0 0 24 24',
                  fill: 'none',
                  stroke: 'currentColor',
                  strokeWidth: 2,
                  class: ['arrow-icon', { expanded: isExpanded.value }],
                }, [h('path', { d: 'M9 5l7 7-7 7' })])
              : h('span', { class: 'no-children' }),
          ]),
          // 图标
          props.showIcon
            ? h('span', { class: 'node-icon', style: { color: props.category.color } }, props.category.icon || '📁')
            : null,
          // 名称
          h('span', { class: 'node-name' }, props.category.name),
          // 数量
          props.showCount && props.category.notes_count
            ? h('span', { class: 'node-count' }, `(${props.category.notes_count})`)
            : null,
        ]),
        // 子节点
        hasChildren.value && isExpanded.value
          ? h('ul', { class: 'children-list' },
              props.category.children!.map(child =>
                h(TreeNode, {
                  key: child.id,
                  category: child,
                  selectedId: props.selectedId,
                  expandedIds: props.expandedIds,
                  level: props.level + 1,
                  expandable: props.expandable,
                  showIcon: props.showIcon,
                  showCount: props.showCount,
                  onSelect: (c: CategoryTreeItem) => emit('select', c),
                  onToggle: (c: CategoryTreeItem) => emit('toggle', c),
                })
              )
            )
          : null,
      ]);
    };
  },
});
</script>

<template>
  <div class="category-tree">
    <div v-if="loading" class="tree-loading">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>

    <div v-else-if="categoryTree.length === 0" class="tree-empty">
      暂无分类
    </div>

    <ul v-else class="tree-list">
      <TreeNode
        v-for="category in categoryTree"
        :key="category.id"
        :category="category"
        :selected-id="selectedId"
        :expanded-ids="expandedIds"
        :level="0"
        :expandable="expandable"
        :show-icon="showIcon"
        :show-count="showCount"
        @select="selectCategory"
        @toggle="toggleExpand"
      />
    </ul>
  </div>
</template>



<style scoped>
.category-tree {
  width: 100%;
  max-height: 400px;
  overflow-y: auto;
}

.tree-loading,
.tree-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px 20px;
  color: #9ca3af;
  font-size: 14px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e5e7eb;
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.tree-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tree-node {
  margin: 2px 0;
}

.node-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.node-content:hover {
  background: #f3f4f6;
}

.node-content.selected {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
}

.expand-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.arrow-icon {
  width: 14px;
  height: 14px;
  color: #9ca3af;
  transition: transform 0.2s;
}

.arrow-icon.expanded {
  transform: rotate(90deg);
}

.no-children {
  width: 14px;
}

.node-icon {
  font-size: 16px;
}

.node-name {
  flex: 1;
  font-size: 14px;
  color: #1f2937;
}

.node-count {
  font-size: 12px;
  color: #9ca3af;
}

.children-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
