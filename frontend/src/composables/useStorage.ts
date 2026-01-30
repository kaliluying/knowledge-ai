/**
 * 本地存储组合式函数
 */

import { ref, watch } from 'vue';

export function useStorage<T>(key: string, defaultValue: T) {
  const storedValue = localStorage.getItem(key);
  const data = ref<T>(storedValue ? JSON.parse(storedValue) : defaultValue);

  // 监听变化并同步到 localStorage
  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue));
  }, { deep: true });

  // 设置值
  function set(value: T) {
    data.value = value;
  }

  // 获取值
  function get(): T {
    return data.value;
  }

  // 移除值
  function remove() {
    localStorage.removeItem(key);
    data.value = defaultValue;
  }

  // 清空所有相关存储
  function clear() {
    remove();
  }

  return {
    data,
    set,
    get,
    remove,
    clear,
  };
}

// 简单的键值对存储
export function useLocalStorage() {
  function set(key: string, value: unknown) {
    localStorage.setItem(key, JSON.stringify(value));
  }

  function get<T>(key: string, defaultValue?: T): T | undefined {
    const item = localStorage.getItem(key);
    if (item) {
      return JSON.parse(item) as T;
    }
    return defaultValue;
  }

  function remove(key: string) {
    localStorage.removeItem(key);
  }

  function has(key: string): boolean {
    return localStorage.getItem(key) !== null;
  }

  function clear() {
    localStorage.clear();
  }

  return {
    set,
    get,
    remove,
    has,
    clear,
  };
}

// 会话存储
export function useSessionStorage() {
  function set(key: string, value: unknown) {
    sessionStorage.setItem(key, JSON.stringify(value));
  }

  function get<T>(key: string, defaultValue?: T): T | undefined {
    const item = sessionStorage.getItem(key);
    if (item) {
      return JSON.parse(item) as T;
    }
    return defaultValue;
  }

  function remove(key: string) {
    sessionStorage.removeItem(key);
  }

  function clear() {
    sessionStorage.clear();
  }

  return {
    set,
    get,
    remove,
    clear,
  };
}
