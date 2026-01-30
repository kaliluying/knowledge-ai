/**
 * 布局状态管理
 */

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export type Theme = 'light' | 'dark';
export type SidebarState = 'expanded' | 'collapsed';

export type LayoutState = {
  sidebarCollapsed: boolean;
  theme: Theme;
  showSidebar: boolean;
  headerHeight: number;
  sidebarWidth: {
    expanded: number;
    collapsed: number;
  };
}

export const useLayoutStore = defineStore('layout', () => {
  // 状态
  const sidebarCollapsed = ref(false);
  const theme = ref<Theme>('light');
  const showSidebar = ref(true);
  const headerHeight = ref(64);
  const isMobile = ref(false);

  const sidebarWidth = {
    expanded: 260,
    collapsed: 72,
  };

  // 计算属性
  const currentSidebarWidth = computed(() =>
    sidebarCollapsed.value ? sidebarWidth.collapsed : sidebarWidth.expanded
  );

  const mainContentStyle = computed(() => ({
    paddingLeft: showSidebar.value ? `${currentSidebarWidth.value}px` : '0',
    marginTop: `${headerHeight.value}px`,
  }));

  const isDarkMode = computed(() => theme.value === 'dark');

  // 从 localStorage 恢复设置
  function loadSettings() {
    if (typeof window === 'undefined') return;

    const savedTheme = localStorage.getItem('theme') as Theme | null;
    const savedSidebar = localStorage.getItem('sidebarCollapsed');
    const savedShowSidebar = localStorage.getItem('showSidebar');

    if (savedTheme && (savedTheme === 'light' || savedTheme === 'dark')) {
      theme.value = savedTheme;
    }

    if (savedSidebar !== null) {
      sidebarCollapsed.value = savedSidebar === 'true';
    }

    if (savedShowSidebar !== null) {
      showSidebar.value = savedShowSidebar === 'true';
    }

    // 检测移动设备
    checkIsMobile();
  }

  // 检测是否为移动设备
  function checkIsMobile() {
    if (typeof window === 'undefined') return;
    isMobile.value = window.innerWidth < 768;
  }

  // 切换侧边栏
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value;
    saveSettings();
  }

  // 展开侧边栏
  function expandSidebar() {
    sidebarCollapsed.value = false;
    saveSettings();
  }

  // 折叠侧边栏
  function collapseSidebar() {
    sidebarCollapsed.value = true;
    saveSettings();
  }

  // 切换主题
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
    saveSettings();
    applyTheme();
  }

  // 设置主题
  function setTheme(newTheme: Theme) {
    theme.value = newTheme;
    saveSettings();
    applyTheme();
  }

  // 切换侧边栏显示
  function toggleSidebarVisibility() {
    showSidebar.value = !showSidebar.value;
    saveSettings();
  }

  // 显示侧边栏
  function showSidebarMenu() {
    showSidebar.value = true;
    saveSettings();
  }

  // 隐藏侧边栏
  function hideSidebarMenu() {
    showSidebar.value = false;
    saveSettings();
  }

  // 应用主题到 HTML
  function applyTheme() {
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark', isDarkMode.value);
    }
  }

  // 保存设置到 localStorage
  function saveSettings() {
    if (typeof window === 'undefined') return;
    localStorage.setItem('theme', theme.value);
    localStorage.setItem('sidebarCollapsed', String(sidebarCollapsed.value));
    localStorage.setItem('showSidebar', String(showSidebar.value));
  }

  // 初始化
  function init() {
    loadSettings();
    applyTheme();

    if (typeof window !== 'undefined') {
      window.addEventListener('resize', checkIsMobile);
    }
  }

  // 重置
  function reset() {
    sidebarCollapsed.value = false;
    theme.value = 'light';
    showSidebar.value = true;
    saveSettings();
    applyTheme();
  }

  return {
    // 状态
    sidebarCollapsed,
    theme,
    showSidebar,
    headerHeight,
    isMobile,
    sidebarWidth,
    // 计算属性
    currentSidebarWidth,
    mainContentStyle,
    isDarkMode,
    // 方法
    loadSettings,
    checkIsMobile,
    toggleSidebar,
    expandSidebar,
    collapseSidebar,
    toggleTheme,
    setTheme,
    toggleSidebarVisibility,
    showSidebarMenu,
    hideSidebarMenu,
    applyTheme,
    saveSettings,
    init,
    reset,
  };
});
