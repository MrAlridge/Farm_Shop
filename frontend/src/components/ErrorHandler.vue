<template>
  <el-dialog
    v-model="visible"
    title="错误提示"
    width="30%"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false">
    <div class="error-content">
      <el-icon class="error-icon"><Warning /></el-icon>
      <p class="error-message">{{ errorMessage }}</p>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="handleClose">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useStore } from 'vuex'
import { Warning } from '@element-plus/icons-vue'

const store = useStore()
const visible = ref(false)

const errorMessage = computed(() => store.state.error?.message || '发生未知错误')

const handleClose = () => {
  visible.value = false
  store.commit('SET_ERROR', null)
}

// 监听错误状态
watch(() => store.state.error, (error) => {
  if (error) {
    visible.value = true
  }
}, { immediate: true })
</script>

<style scoped>
.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.error-icon {
  font-size: 48px;
  color: #f56c6c;
  margin-bottom: 20px;
}

.error-message {
  text-align: center;
  color: #606266;
  line-height: 1.5;
}
</style> 