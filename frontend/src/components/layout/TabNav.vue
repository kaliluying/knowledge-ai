<template>
  <div class="tab-nav">
    <div class="tab-list" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-item"
        :class="{ 'active': modelValue === tab.id, 'disabled': tab.disabled }"
        role="tab"
        :aria-selected="modelValue === tab.id"
        :aria-controls="`panel-${tab.id}`"
        :disabled="tab.disabled"
        @click="selectTab(tab.id)"
      >
        <span class="tab-icon" v-if="tab.icon">
          <component :is="tab.icon" />
        </span>
        <span class="tab-label">{{ tab.label }}</span>
        <span class="tab-badge" v-if="tab.badge">{{ tab.badge }}</span>
      </button>
    </div>
    <div
      class="tab-indicator"
      :style="indicatorStyle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'

interface Tab {
  id: string
  label: string
  icon?: string
  badge?: number | string
  disabled?: boolean
}

interface Props {
  modelValue: string
  tabs: Tab[]
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const activeTabRef = ref<HTMLElement | null>(null)

const indicatorStyle = computed(() => {
  if (!activeTabRef.value) return {}
  
  return {
    left: `${activeTabRef.value.offsetLeft}px`,
    width: `${activeTabRef.value.offsetWidth}px`
  }
})

function selectTab(tabId: string) {
  const tab = props.tabs.find(t => t.id === tabId)
  if (tab && !tab.disabled) {
    emit('update:modelValue', tabId)
  }
}

watch(() => props.modelValue, () => {
  updateActiveTabRef()
})

function updateActiveTabRef() {
  nextTick(() => {
    activeTabRef.value = document.querySelector(`.tab-item.active`) as HTMLElement
  })
}

onMounted(updateActiveTabRef)
</script>

<style lang="scss" scoped>
.tab-nav {
  position: relative;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}

.tab-list {
  display: flex;
  gap: 0.25rem;
  padding: 0 1rem;
  overflow-x: auto;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s, background-color 0.2s;
  white-space: nowrap;
  
  &:hover:not(.disabled) {
    color: #111827;
    background: #f9fafb;
  }
  
  &.active {
    color: #3b82f6;
  }
  
  &.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.tab-icon {
  display: inline-flex;
  width: 1rem;
  height: 1rem;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 1.25rem;
  height: 1.25rem;
  padding: 0 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
  background: #ef4444;
  color: #fff;
  border-radius: 9999px;
}

.tab-indicator {
  position: absolute;
  bottom: -1px;
  height: 2px;
  background: #3b82f6;
  transition: left 0.2s ease, width 0.2s ease;
}
</style>
