<template>
  <div v-if="loading" class="loading-overlay">
    <div class="loading-content">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p class="loading-text">{{ loadingText }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { Loading } from '@element-plus/icons-vue'

const store = useStore()

const loading = computed(() => store.state.loading)
const loadingText = computed(() => store.state.loadingText || '加载中...')
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-icon {
  font-size: 48px;
  color: #409eff;
  animation: rotate 2s linear infinite;
}

.loading-text {
  margin-top: 16px;
  color: #606266;
  font-size: 16px;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 