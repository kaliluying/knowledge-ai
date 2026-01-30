/**
 * 模态框控制组合式函数
 */

import { ref, computed } from 'vue';

interface ModalState {
  isOpen: boolean;
  data: Record<string, unknown>;
}

export function useModal<T = Record<string, unknown>>() {
  const modals = ref<Map<string, ModalState>>(new Map());

  function open(modalId: string, data?: T) {
    modals.value.set(modalId, {
      isOpen: true,
      data: (data as Record<string, unknown>) || {},
    });
  }

  function close(modalId: string) {
    const modal = modals.value.get(modalId);
    if (modal) {
      modal.isOpen = false;
    }
  }

  function toggle(modalId: string) {
    const modal = modals.value.get(modalId);
    if (modal) {
      modal.isOpen = !modal.isOpen;
    } else {
      open(modalId);
    }
  }

  function setData(modalId: string, data: T) {
    const modal = modals.value.get(modalId);
    if (modal) {
      modal.data = data as Record<string, unknown>;
    } else {
      open(modalId, data);
    }
  }

  function getData(modalId: string): T | undefined {
    const modal = modals.value.get(modalId);
    return modal?.data as T;
  }

  function isOpen(modalId: string): boolean {
    return modals.value.get(modalId)?.isOpen || false;
  }

  return {
    modals,
    open,
    close,
    toggle,
    setData,
    getData,
    isOpen,
  };
}
