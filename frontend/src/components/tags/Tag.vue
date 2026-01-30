<script setup lang="ts">
import type { Tag } from '@/types';

interface Props {
  tag: Tag;
  size?: 'sm' | 'md' | 'lg';
  removable?: boolean;
  clickable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  removable: false,
  clickable: false,
});

const emit = defineEmits<{
  remove: [tag: Tag];
  click: [tag: Tag];
}>();

const sizeClasses = {
  sm: 'tag-sm',
  md: 'tag-md',
  lg: 'tag-lg',
};

const handleClick = () => {
  if (props.clickable) {
    emit('click', props.tag);
  }
};

const handleRemove = (e: Event) => {
  e.stopPropagation();
  emit('remove', props.tag);
};
</script>

<template>
  <span
    class="tag"
    :class="[sizeClasses[size], { clickable }]"
    :style="{ backgroundColor: tag.color + '20', color: tag.color }"
    @click="handleClick"
  >
    {{ tag.name }}
    <button
      v-if="removable"
      class="remove-btn"
      @click="handleRemove"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 6L6 18M6 6l12 12" />
      </svg>
    </button>
  </span>
</template>

<style scoped>
.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s;
}

.tag-sm {
  padding: 2px 8px;
  font-size: 11px;
}

.tag-md {
  padding: 4px 10px;
  font-size: 12px;
}

.tag-lg {
  padding: 6px 14px;
  font-size: 14px;
}

.clickable {
  cursor: pointer;
}

.clickable:hover {
  filter: brightness(0.95);
}

.remove-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

.remove-btn svg {
  width: 10px;
  height: 10px;
}

.tag-sm .remove-btn svg {
  width: 8px;
  height: 8px;
}

.tag-lg .remove-btn svg {
  width: 12px;
  height: 12px;
}
</style>
