/**
 * Vue Router 配置
 */

import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/pages/Register.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/pages/Home.vue'),
      },
      {
        path: 'notes',
        name: 'Notes',
        component: () => import('@/pages/notes/NoteList.vue'),
      },
      {
        path: 'notes/new',
        name: 'NoteCreate',
        component: () => import('@/pages/notes/NoteEditor.vue'),
      },
      {
        path: 'notes/:id',
        name: 'NoteDetail',
        component: () => import('@/pages/notes/NoteDetail.vue'),
      },
      {
        path: 'notes/:id/edit',
        name: 'NoteEdit',
        component: () => import('@/pages/notes/NoteEditor.vue'),
      },
      {
        path: 'categories',
        name: 'Categories',
        component: () => import('@/pages/categories/CategoryList.vue'),
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/pages/tags/TagList.vue'),
      },
      {
        path: 'graph',
        name: 'Graph',
        component: () => import('@/pages/graph/GraphView.vue'),
      },
      {
        path: 'collections',
        name: 'Collections',
        component: () => import('@/pages/collections/CollectionList.vue'),
      },
      {
        path: 'collections/add',
        name: 'CollectionAdd',
        component: () => import('@/pages/collections/CollectionAdd.vue'),
      },
      {
        path: 'collections/:id',
        name: 'CollectionDetail',
        component: () => import('@/pages/collections/CollectionDetail.vue'),
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/pages/settings/Settings.vue'),
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFound.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore();

  // 如果还未初始化，等待初始化完成
  if (!authStore.isInitialized) {
    await authStore.initAuth();
  }

  // 检查是否需要认证
  const hasValidAuth = authStore.user !== null && authStore.isAuthenticated;

  if (to.meta.requiresAuth && !hasValidAuth) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'Login' || to.name === 'Register') && hasValidAuth) {
    next({ name: 'Home' });
  } else {
    next();
  }
});

export default router;
