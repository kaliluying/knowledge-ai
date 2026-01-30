<script setup lang="ts">
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores';
import { onMounted } from 'vue';

const authStore = useAuthStore();

onMounted(() => {
  authStore.initAuth();
});
</script>

<template>
  <RouterView />
</template>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>
