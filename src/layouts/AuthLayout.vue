<!-- 认证布局组件 -->
<!-- layouts/AuthLayout.vue -->

<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-logo">
        <img src="../assets/logo.png" alt="ScoreX Logo" />
        <h1>ScoreX 查分星</h1>
      </div>
      <div class="auth-card">
        <router-view />
      </div>
      <div class="auth-footer">
        <p>© {{ currentYear }} ScoreX 查分星 - 为中学生提供优质高效的考试服务</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 当前年份
const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.auth-logo {
  text-align: center;
  margin-bottom: 24px;
}

.auth-logo img {
  width: 64px;
  height: 64px;
}

.auth-logo h1 {
  margin-top: 12px;
  font-size: 24px;
  color: #333;
}

.auth-card {
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  color: #666;
  font-size: 14px;
}
</style>
