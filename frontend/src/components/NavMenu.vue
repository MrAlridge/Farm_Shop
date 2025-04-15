<template>
  <div class="nav-menu">
    <!-- 顶部导航栏 -->
    <el-header class="header">
      <div class="logo">
        <!-- <img src="/images/logo.png" alt="Logo"> -->
        <span>扶贫电商平台</span>
      </div>
      
      <div class="nav-items">
        <el-menu
          mode="horizontal"
          :router="true"
          :default-active="activeMenu">
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/products">商品列表</el-menu-item>
          <el-menu-item index="/poverty-info">扶贫信息</el-menu-item>
        </el-menu>
      </div>
      
      <div class="user-actions">
        <template v-if="isLoggedIn">
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32" :src="userInfo.avatar" />
              <span class="username">{{ userInfo.username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToUserCenter">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item @click="goToOrders">
                  <el-icon><List /></el-icon>我的订单
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-badge :value="cartCount" :hidden="cartCount === 0" class="cart-badge">
            <el-button type="text" @click="goToCart">
              <el-icon><ShoppingCart /></el-icon>
            </el-button>
          </el-badge>
        </template>
        <template v-else>
          <el-button type="primary" @click="goToLogin">登录</el-button>
          <el-button @click="goToRegister">注册</el-button>
        </template>
      </div>
    </el-header>
    
    <!-- 侧边栏菜单 -->
    <el-aside width="200px" class="aside" v-if="showSidebar">
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        :router="true">
        <el-menu-item index="/user">
          <el-icon><User /></el-icon>
          <span>个人资料</span>
        </el-menu-item>
        <el-menu-item index="/user/address">
          <el-icon><Location /></el-icon>
          <span>收货地址</span>
        </el-menu-item>
        <el-menu-item index="/user/security">
          <el-icon><Lock /></el-icon>
          <span>安全设置</span>
        </el-menu-item>
        <el-menu-item index="/orders">
          <el-icon><List /></el-icon>
          <span>我的订单</span>
        </el-menu-item>
        <el-menu-item index="/user/favorites">
          <el-icon><Star /></el-icon>
          <span>我的收藏</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  ShoppingCart,
  List,
  SwitchButton,
  Location,
  Lock,
  Star
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const store = useStore()

// 计算属性
const isLoggedIn = computed(() => store.state.user.isLoggedIn)
const userInfo = computed(() => store.state.user.userInfo)
const cartCount = computed(() => store.state.cart.count)
const activeMenu = computed(() => route.path)
const showSidebar = computed(() => route.path.startsWith('/user'))

// 方法
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToUserCenter = () => {
  router.push('/user')
}

const goToOrders = () => {
  router.push('/orders')
}

const goToCart = () => {
  router.push('/cart')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    store.dispatch('user/logout')
    ElMessage.success('退出成功')
    router.push('/login')
  }).catch(() => {})
}
</script>

<style scoped>
.nav-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.logo span {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.nav-items {
  flex: 1;
  margin: 0 40px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  color: #606266;
}

.cart-badge {
  margin-left: 10px;
}

.aside {
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  background-color: #fff;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 8px;
}
</style> 