<script setup>
import { ref, onMounted } from 'vue'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import NavHeader from '@/components/NavHeader.vue'
import NavFooter from '@/components/NavFooter.vue'
import NavMenu from './components/NavMenu.vue'
import ErrorHandler from './components/ErrorHandler.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'

const isDarkMode = ref(false)

// 检查系统主题偏好
onMounted(() => {
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDarkMode.value = true
  }
})

// 切换暗色模式
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.classList.toggle('dark')
}
</script>

<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container" :class="{ 'dark-mode': isDarkMode }">
      <el-container>
        <el-header>
          <nav-header @toggle-dark-mode="toggleDarkMode" />
        </el-header>
        <el-main>
          <router-view />
        </el-main>
        <el-footer>
          <nav-footer />
        </el-footer>
      </el-container>
    </div>
  </el-config-provider>
</template>

<style>
:root {
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  --text-color: #303133;
  --text-color-secondary: #606266;
  --border-color: #DCDFE6;
  --background-color: #F5F7FA;
}

.dark-mode {
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  --text-color: #E5EAF3;
  --text-color-secondary: #A3A6AD;
  --border-color: #4C4D4F;
  --background-color: #1A1A1A;
}

.app-container {
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  transition: all 0.3s ease;
}

.el-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.el-header {
  padding: 0;
  height: auto;
}

.el-main {
  min-height: calc(100vh - 120px);
  padding: 20px 0;
}

.el-footer {
  padding: 20px 0;
  text-align: center;
  color: var(--text-color-secondary);
  border-top: 1px solid var(--border-color);
}

/* 全局样式 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 为路由视图添加顶部边距，避免被导航栏遮挡 */
.router-view {
  margin-top: 60px;
  min-height: calc(100vh - 60px);
  padding: 20px;
}

/* 当显示侧边栏时，调整主内容区域的左边距 */
.router-view.with-sidebar {
  margin-left: 200px;
  width: calc(100% - 200px);
}
</style>
