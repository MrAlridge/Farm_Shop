<template>
  <div class="social-layout">
    <el-container>
      <el-header>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="activeMenu"
            class="social-menu"
            router
          >
            <el-menu-item index="/social/project-publish">
              <el-icon><Plus /></el-icon>
              <span>发布帮扶</span>
            </el-menu-item>
            <el-menu-item index="/social/project-manage">
              <el-icon><List /></el-icon>
              <span>管理帮扶</span>
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
import {
  Plus,
  List
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.social-layout {
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

.social-menu {
  height: 100%;
  border-right: none;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style> 