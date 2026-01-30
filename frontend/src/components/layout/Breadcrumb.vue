<template>
  <nav class="breadcrumb" aria-label="面包屑导航">
    <ol class="breadcrumb-list">
      <li
        v-for="(item, index) in items"
        :key="index"
        class="breadcrumb-item"
        :class="{ 'active': index === items.length - 1 }"
      >
        <router-link
          v-if="index < items.length - 1 && item.to"
          :to="item.to"
          class="breadcrumb-link"
        >
          <span class="breadcrumb-icon" v-if="item.icon">
            <component :is="item.icon" />
          </span>
          {{ item.label }}
        </router-link>
        <span v-else class="breadcrumb-text">
          <span class="breadcrumb-icon" v-if="item.icon">
            <component :is="item.icon" />
          </span>
          {{ item.label }}
        </span>
        <span v-if="index < items.length - 1" class="breadcrumb-separator">/</span>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
interface BreadcrumbItem {
  label: string
  to?: string
  icon?: string
}

interface Props {
  items: BreadcrumbItem[]
}

defineProps<Props>()
</script>

<style lang="scss" scoped>
.breadcrumb {
  padding: 0.75rem 0;
  font-size: 0.875rem;
}

.breadcrumb-list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  
  &.active {
    color: #111827;
    font-weight: 500;
  }
}

.breadcrumb-link {
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s;
  
  &:hover {
    color: #3b82f6;
  }
}

.breadcrumb-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.breadcrumb-icon {
  display: inline-flex;
  width: 1rem;
  height: 1rem;
}

.breadcrumb-separator {
  color: #d1d5db;
}
</style>
