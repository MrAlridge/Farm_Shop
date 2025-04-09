<template>
  <el-menu
    :default-active="activeIndex"
    class="nav-menu"
    mode="horizontal"
    :router="true"
    @select="handleSelect"
  >
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/products">商品列表</el-menu-item>
    <el-menu-item index="/cart">购物车</el-menu-item>
    <el-menu-item index="/orders">我的订单</el-menu-item>
    
    <!-- 贫困户导航 -->
    <el-sub-menu index="poor" v-if="isPoorUser">
      <template #title>扶贫专区</template>
      <el-menu-item index="/poor/dashboard">扶贫首页</el-menu-item>
      <el-menu-item index="/poor/policies">扶贫政策</el-menu-item>
      <el-menu-item index="/poor/cases">扶贫案例</el-menu-item>
      <el-menu-item index="/poor/applications">我的申请</el-menu-item>
    </el-sub-menu>

    <!-- 用户中心 -->
    <el-sub-menu index="user" class="user-menu">
      <template #title>
        <el-avatar :size="32" :src="userAvatar" />
        <span class="username">{{ username }}</span>
      </template>
      <el-menu-item index="/user/profile">个人中心</el-menu-item>
      <el-menu-item index="/user/address">收货地址</el-menu-item>
      <el-menu-item index="/user/security">安全设置</el-menu-item>
      <el-menu-item @click="handleLogout">退出登录</el-menu-item>
    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { usePoorStore } from '@/store/modules/poor'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const poorStore = usePoorStore()

const activeIndex = ref('/')

const username = computed(() => {
  return userStore.userInfo?.username || poorStore.userInfo?.username || '未登录'
})

const userAvatar = computed(() => {
  return userStore.userInfo?.avatar || poorStore.userInfo?.avatar || ''
})

const isPoorUser = computed(() => {
  return poorStore.isLoggedIn
})

const handleSelect = (key) => {
  activeIndex.value = key
}

const handleLogout = async () => {
  try {
    if (isPoorUser.value) {
      await poorStore.logout()
    } else {
      await userStore.logout()
    }
    ElMessage.success('退出登录成功')
    router.push('/login')
  } catch (error) {
    ElMessage.error('退出登录失败')
  }
}
</script>

<style scoped>
.nav-menu {
  border-bottom: solid 1px var(--el-menu-border-color);
  padding: 0 20px;
}

.user-menu {
  float: right;
  margin-left: auto;
}

.username {
  margin-left: 8px;
  font-size: 14px;
}

:deep(.el-menu-item) {
  height: 60px;
  line-height: 60px;
}

:deep(.el-sub-menu__title) {
  height: 60px;
  line-height: 60px;
}
</style> 