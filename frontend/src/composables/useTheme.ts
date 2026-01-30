/**
 * 主题切换组合式函数
 */

import { ref, computed, watch, onMounted } from 'vue';

type Theme = 'light' | 'dark';

interface ThemeConfig {
  label: string;
  icon: string;
}

const THEME_STORAGE_KEY = 'app-theme';
const DEFAULT_THEME: Theme = 'light';

const themeConfig: Record<Theme, ThemeConfig> = {
  light: {
    label: '亮色',
    icon: '☀️',
  },
  dark: {
    label: '暗色',
    icon: '🌙',
  },
};

export function useTheme() {
  const currentTheme = ref<Theme>(DEFAULT_THEME);
  const isDark = computed(() => currentTheme.value === 'dark');

  // 从 localStorage 读取主题
  function loadTheme(): Theme {
    if (typeof window === 'undefined') return DEFAULT_THEME;
    
    try {
      const saved = localStorage.getItem(THEME_STORAGE_KEY);
      if (saved && (saved === 'light' || saved === 'dark')) {
        return saved;
      }
    } catch {
      // 忽略错误
    }
    
    // 检查系统偏好
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    return DEFAULT_THEME;
  }

  // 保存主题到 localStorage
  function saveTheme(theme: Theme) {
    try {
      localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch {
      // 忽略错误
    }
  }

  // 应用主题到 DOM
  function applyTheme(theme: Theme) {
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', theme);
    }
  }

  // 切换主题
  function toggleTheme() {
    const newTheme = isDark.value ? 'light' : 'dark';
    setTheme(newTheme);
  }

  // 设置主题
  function setTheme(theme: Theme) {
    currentTheme.value = theme;
    saveTheme(theme);
    applyTheme(theme);
  }

  // 跟随系统主题
  function useSystemTheme() {
    if (typeof window === 'undefined' || !window.matchMedia) return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      const theme = e.matches ? 'dark' : 'light';
      setTheme(theme);
    };

    mediaQuery.addEventListener('change', handleChange);

    // 初始化
    setTheme(mediaQuery.matches ? 'dark' : 'light');

    // 返回清理函数
    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }

  // 初始化
  onMounted(() => {
    currentTheme.value = loadTheme();
    applyTheme(currentTheme.value);
  });

  // 监听变化
  watch(currentTheme, (theme) => {
    applyTheme(theme);
  });

  return {
    currentTheme,
    isDark,
    themeConfig,
    toggleTheme,
    setTheme,
    useSystemTheme,
  };
}
