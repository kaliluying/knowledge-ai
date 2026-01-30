<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';

interface NavItem {
  name: string;
  path: string;
  icon: string;
}

const route = useRoute();
const router = useRouter();

const navItems: NavItem[] = [
  { name: '首页', path: '/', icon: 'home' },
  { name: '笔记', path: '/notes', icon: 'notes' },
  { name: '分类', path: '/categories', icon: 'category' },
  { name: '标签', path: '/tags', icon: 'tag' },
  { name: '图谱', path: '/graph', icon: 'graph' },
];

const isActive = (path: string) => {
  if (path === '/') return route.path === '/';
  return route.path.startsWith(path);
};

const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<template>
  <aside class="app-sidebar">
    <!-- Logo -->
    <div class="sidebar-logo" @click="navigateTo('/')">
      <div class="logo-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      </div>
      <span class="logo-text">Knowledge</span>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li v-for="item in navItems" :key="item.path">
          <button
            class="nav-item"
            :class="{ active: isActive(item.path) }"
            @click="navigateTo(item.path)"
          >
            <span class="nav-icon">
              <!-- Home -->
              <svg v-if="item.icon === 'home'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <!-- Notes -->
              <svg v-else-if="item.icon === 'notes'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <!-- Category -->
              <svg v-else-if="item.icon === 'category'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <!-- Tag -->
              <svg v-else-if="item.icon === 'tag'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <!-- Graph -->
              <svg v-else-if="item.icon === 'graph'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </span>
            <span class="nav-name">{{ item.name }}</span>
          </button>
        </li>
      </ul>
    </nav>

    <!-- Bottom section -->
    <div class="sidebar-bottom">
      <button
        class="nav-item"
        :class="{ active: route.path === '/settings' }"
        @click="navigateTo('/settings')"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </span>
        <span class="nav-name">设置</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  border-bottom: 1px solid #f3f4f6;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-logo:hover {
  background: #f8fafc;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
}

.logo-icon svg {
  width: 22px;
  height: 22px;
  color: white;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.nav-item:hover {
  background: #f8fafc;
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
}

.nav-icon {
  width: 22px;
  height: 22px;
  color: #9ca3af;
  flex-shrink: 0;
}

.nav-item.active .nav-icon {
  color: #8b5cf6;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-name {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
}

.nav-item.active .nav-name {
  color: #8b5cf6;
  font-weight: 600;
}

/* Bottom */
.sidebar-bottom {
  padding: 12px;
  border-top: 1px solid #f3f4f6;
}
</style>
