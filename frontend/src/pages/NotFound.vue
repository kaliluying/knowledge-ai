<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1>页面未找到</h1>
      <p>抱歉，您访问的页面不存在。</p>
      <button class="back-btn" @click="router.push('/')">
        返回首页
      </button>
    </div>
  </div>
</template>

<style scoped>
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8fafc;
}

.not-found-content {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 60px rgba(0, 0, 0, 0.1);
  max-width: 400px;
}

.error-code {
  font-size: 120px;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 16px;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

p {
  font-size: 15px;
  color: #9ca3af;
  margin-bottom: 32px;
}

.back-btn {
  padding: 14px 32px;
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(124, 58, 237, 0.5);
}
</style>
