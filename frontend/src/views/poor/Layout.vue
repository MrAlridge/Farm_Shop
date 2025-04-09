<template>
  <div class="poor-layout">
    <el-container>
      <el-header>
        <nav-bar />
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="activeMenu"
            class="poor-menu"
            router
          >
            <el-menu-item index="/poor/dashboard">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/poor/policies">
              <el-icon><Document /></el-icon>
              <span>扶贫政策</span>
            </el-menu-item>
            <el-menu-item index="/poor/cases">
              <el-icon><Star /></el-icon>
              <span>成功案例</span>
            </el-menu-item>
            <el-menu-item index="/poor/applications">
              <el-icon><List /></el-icon>
              <span>我的申请</span>
            </el-menu-item>
            <el-menu-item index="/poor/notifications">
              <el-icon><Bell /></el-icon>
              <span>系统通知</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import {
  HomeFilled,
  Document,
  Star,
  List,
  Bell
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.poor-layout {
  height: 100vh;
}

.el-header {
  padding: 0;
  height: 60px;
}

.el-aside {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
}

.poor-menu {
  height: 100%;
  border-right: none;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style> 