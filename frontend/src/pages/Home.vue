<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useNotesStore, useAuthStore } from '@/stores';
import type { NoteListItem } from '@/types';

const router = useRouter();
const notesStore = useNotesStore();
const authStore = useAuthStore();

const recentNotes = ref<NoteListItem[]>([]);
const isLoading = ref(true);

onMounted(async () => {
  try {
    const notes = await notesStore.fetchRecentNotes(5);
    recentNotes.value = notes || [];
  } finally {
    isLoading.value = false;
  }
});

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString('zh-CN');
};

const navigateToNote = (id: number) => {
  router.push(`/notes/${id}`);
};

const navigateToCreate = () => {
  router.push('/notes/new');
};

const navigateToNotes = () => {
  router.push('/notes');
};
</script>

<template>
  <div class="home-page">
    <!-- Welcome section -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <div class="welcome-text">
          <h1>你好，{{ authStore.user?.username || '用户' }}！👋</h1>
          <p>欢迎回来，继续你的知识管理之旅</p>
        </div>
      </div>
      <button class="create-btn" @click="navigateToCreate">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        新建笔记
      </button>
    </div>

    <!-- Recent notes section -->
    <div class="section">
      <div class="section-header">
        <h2>最近笔记</h2>
        <button class="view-all-btn" @click="navigateToNotes">查看全部 →</button>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="loading-grid">
        <div v-for="n in 4" :key="n" class="skeleton-card">
          <div class="skeleton-title"></div>
          <div class="skeleton-meta"></div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="recentNotes.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3>暂无笔记</h3>
        <p>开始创建你的第一篇笔记吧</p>
        <button class="create-btn-small" @click="navigateToCreate">新建笔记</button>
      </div>

      <!-- Notes grid -->
      <div v-else class="notes-grid">
        <div
          v-for="note in recentNotes"
          :key="note.id"
          class="note-card"
          @click="navigateToNote(note.id)"
        >
          <div class="note-header">
            <span v-if="note.is_pinned" class="pinned-badge">置顶</span>
          </div>
          <h3 class="note-title">{{ note.title || '无标题' }}</h3>
          <div class="note-footer">
            <span class="note-date">{{ formatDate(note.updated_at) }}</span>
            <span v-if="note.category_name" class="category-tag">{{ note.category_name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="section">
      <h2>快捷入口</h2>
      <div class="actions-grid">
        <div class="action-card" @click="navigateToCreate">
          <div class="action-icon create">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <h3>新建笔记</h3>
          <p>创建一篇新的笔记</p>
        </div>

        <div class="action-card" @click="navigateToNotes">
          <div class="action-icon notes">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3>全部笔记</h3>
          <p>查看和管理所有笔记</p>
        </div>

        <router-link to="/categories" class="action-card link">
          <div class="action-icon category">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <h3>分类管理</h3>
          <p>组织和分类你的笔记</p>
        </router-link>

        <router-link to="/tags" class="action-card link">
          <div class="action-icon tag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <h3>标签管理</h3>
          <p>使用标签整理笔记</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

/* Welcome section */
.welcome-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 24px;
  margin-bottom: 32px;
  box-shadow: 0 10px 40px rgba(124, 58, 237, 0.3);
}

.welcome-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.welcome-icon svg {
  width: 36px;
  height: 36px;
  color: white;
}

.welcome-text h1 {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.welcome-text p {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.8);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  background: white;
  color: #7c3aed;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.3);
}

.create-btn svg {
  width: 20px;
  height: 20px;
}

/* Section */
.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
}

.view-all-btn {
  background: none;
  border: none;
  color: #8b5cf6;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.view-all-btn:hover {
  color: #7c3aed;
}

/* Loading skeleton */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.skeleton-card {
  background: #f8fafc;
  border-radius: 16px;
  padding: 20px;
  border: 2px solid #e5e7eb;
}

.skeleton-title {
  height: 24px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  margin-bottom: 12px;
  animation: skeleton 1.5s ease-in-out infinite;
}

.skeleton-meta {
  height: 16px;
  width: 60%;
  background: linear-gradient(90deg, #e5e7eb 25%, #f1f5f9 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  border-radius: 6px;
  animation: skeleton 1.5s ease-in-out infinite;
}

@keyframes skeleton {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 60px 40px;
  background: #f8fafc;
  border-radius: 16px;
  border: 2px dashed #e5e7eb;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: #f1f5f9;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
  color: #9ca3af;
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 24px;
}

.create-btn-small {
  padding: 12px 24px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.create-btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

/* Notes grid */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.note-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
}

.note-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  border-color: #8b5cf6;
}

.note-header {
  margin-bottom: 12px;
}

.pinned-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background: #fef3c7;
  color: #d97706;
  font-size: 12px;
  font-weight: 600;
  border-radius: 6px;
}

.note-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
  line-height: 1.4;
}

.note-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.note-date {
  font-size: 13px;
  color: #9ca3af;
}

.category-tag {
  padding: 4px 10px;
  background: #f3f4f6;
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
}

/* Actions grid */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.action-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 2px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
  display: block;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
}

.action-card.link:hover {
  border-color: #8b5cf6;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.action-icon svg {
  width: 28px;
  height: 28px;
}

.action-icon.create {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.action-icon.notes {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.action-icon.category {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.action-icon.tag {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  color: white;
}

.action-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 6px;
}

.action-card p {
  font-size: 13px;
  color: #9ca3af;
}

/* Responsive */
@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: 24px;
    padding: 24px;
  }

  .welcome-content {
    flex-direction: column;
  }

  .notes-grid,
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
