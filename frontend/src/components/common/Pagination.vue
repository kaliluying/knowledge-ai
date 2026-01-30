<script setup lang="ts">
interface Props {
  currentPage: number;
  pageSize: number;
  total: number;
  maxButtons?: number;
}

const props = withDefaults(defineProps<Props>(), {
  maxButtons: 5,
});

const emit = defineEmits<{
  'update:currentPage': [page: number];
  'update:pageSize': [size: number];
  change: [page: number, pageSize: number];
}>();

const totalPages = computed(() => Math.ceil(props.total / props.pageSize));

const pageNumbers = computed(() => {
  const pages: number[] = [];
  const maxButtons = props.maxButtons;
  let start = Math.max(1, props.currentPage - Math.floor(maxButtons / 2));
  let end = Math.min(totalPages.value, start + maxButtons - 1);

  if (end - start + 1 < maxButtons) {
    start = Math.max(1, end - maxButtons + 1);
  }

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  return pages;
});

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value && page !== props.currentPage) {
    emit('update:currentPage', page);
    emit('change', page, props.pageSize);
  }
};

const changePageSize = (e: Event) => {
  const target = e.target as HTMLSelectElement;
  const size = parseInt(target.value, 10);
  emit('update:pageSize', size);
  emit('update:currentPage', 1);
  emit('change', 1, size);
};

const pageSizeOptions = [10, 20, 50, 100];
</script>

<template>
  <div class="pagination">
    <div class="pagination-info">
      显示 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, total) }} 条
      <span class="total">共 {{ total }} 条</span>
    </div>

    <div class="pagination-controls">
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <button
        v-for="page in pageNumbers"
        :key="page"
        class="page-btn"
        :class="{ active: page === currentPage }"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>

      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="goToPage(currentPage + 1)"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <div class="pagination-options">
      <select :value="pageSize" class="page-size-select" @change="changePageSize">
        <option v-for="size in pageSizeOptions" :key="size" :value="size">
          每页 {{ size }} 条
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  gap: 20px;
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

.pagination-info .total {
  color: #9ca3af;
  margin-left: 8px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
  color: #1f2937;
}

.page-btn.active {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn svg {
  width: 16px;
  height: 16px;
}

.pagination-options {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-size-select {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #1f2937;
  background: white;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.page-size-select:focus {
  border-color: #8b5cf6;
}

@media (max-width: 768px) {
  .pagination {
    flex-direction: column;
    gap: 16px;
  }

  .pagination-controls {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
