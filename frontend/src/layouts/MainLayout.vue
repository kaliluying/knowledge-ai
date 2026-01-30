<script setup lang="ts">
import Header from '@/components/layout/Header.vue';
import Sidebar from '@/components/layout/Sidebar.vue';
</script>

<template>
  <div class="app-layout">
    <Sidebar />
    <div class="main-area">
      <Header />
      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}
</style>
