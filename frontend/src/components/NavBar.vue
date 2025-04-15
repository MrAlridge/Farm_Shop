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
    <el-sub-menu index="poor" v-if="isPoorUser">
      <template #title>扶贫专区</template>
      <el-menu-item index="/poor/dashboard">扶贫首页</el-menu-item>
      <el-menu-item index="/poor/policies">扶贫政策</el-menu-item>
      <el-menu-item index="/poor/cases">扶贫案例</el-menu-item>
      <el-menu-item index="/poor/applications" v-if="isPoorUser">我的申请</el-menu-item>
      </el-sub-menu>

    <el-sub-menu index="user" class="user-menu" v-if="isLoggedIn">
      <template #title>
        <el-avatar :size="32" :src="userAvatar" />
        <span class="username">{{ username }}</span>
      </template>
      <el-menu-item index="/user/profile">个人中心</el-menu-item>
      <el-menu-item index="/orders">我的订单</el-menu-item>
      <el-menu-item index="/user/address">收货地址</el-menu-item>
      <el-menu-item index="/user/security">安全设置</el-menu-item>
      <el-menu-item @click="handleLogout">退出登录</el-menu-item>
    </el-sub-menu>

    <div class="auth-buttons" v-else>
      <el-button type="primary" @click="handleLogin">登录</el-button>
      <el-button @click="handleRegister">注册</el-button>
    </div>
  </el-menu>
</template>

<script setup>
import { ref, computed, watch } from 'vue' // 引入 watch
import { useRouter } from 'vue-router'
// 假设 store 已正确设置和导入
import { useUserStore } from '@/store/modules/user' // Pinia 示例
// import { usePoorStore } from '@/store/modules/poor' // Pinia 示例
// import { useStore } from 'vuex' // 或者 Pinia 的 useStore
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
// const poorStore = usePoorStore()

// 根据当前路由初始化 activeIndex
const activeIndex = ref(router.currentRoute.value.path)

// 计算显示用户名
const username = computed(() => {
  return userStore.username || '未登录'
})

// 计算用户头像 URL，提供默认头像
const userAvatar = computed(() => {
  // const defaultAvatar = '/images/avatars/default.png'; // 默认头像路径示例
  return userStore.avatar || ''
})

// 判断当前登录用户是否为贫困户
const isPoorUser = computed(() => {
  // 可以基于 poorStore 登录状态，或者 userStore 中的用户类型字段
  return userStore.userType === 'poor';
})

// 判断是否有用户登录（普通或贫困户）
const isLoggedIn = computed(() => {
  return userStore.token !== ''
})

// 处理菜单选择事件
const handleSelect = (key) => {
  // 如果使用了 :router="true"，通常不需要手动更新 activeIndex
  // 但如果需要其他逻辑，可以在这里处理
  // activeIndex.value = key
}

// 处理退出登录逻辑
const handleLogout = async () => {
  try {
    // 判断调用哪个 store 的 logout action
    // if (poorStore.isLoggedIn.value) {
    //   await poorStore.logout()
    // } else if (userStore.isLoggedIn.value) {
      
    // }
    await userStore.logout()
    ElMessage.success('退出登录成功')
    // 退出后跳转到登录页
    router.push('/login').then(() => {
      // 可选：如果状态未正确清除，强制刷新页面
      window.location.reload();
    });
  } catch (error) {
    console.error("退出登录失败:", error);
    ElMessage.error(error.message || '退出登录失败')
  }
}

// 处理点击登录按钮
const handleLogin = () => {
  router.push('/login')
}

// 处理点击注册按钮
const handleRegister = () => {
  router.push('/register')
}

// 监听路由变化以更新 activeIndex
watch(() => router.currentRoute.value.path, (newPath) => {
  activeIndex.value = newPath;
}, { immediate: true }); // immediate: true 确保初始加载时也执行

console.log('isPoorUser',isPoorUser.value)
console.log('isLoggedIn',isLoggedIn.value)

</script>

<style scoped>
.nav-menu {
  display: flex; /* 使用 flexbox 以便更好地对齐 */
  align-items: center; /* 垂直居中项目 */
  border-bottom: solid 1px var(--el-menu-border-color);
  padding: 0 20px; /* 导航栏左右内边距 */
  height: 60px; /* 确保导航栏高度一致 */
}

/* 将用户菜单和认证按钮推到右侧 */
.user-menu, .auth-buttons {
  margin-left: auto; /* flexbox 中实现右对齐的关键属性 */
}

.username {
  margin-left: 8px; /* 用户名与头像间距 */
  font-size: 14px;
  display: inline-block; /* 确保与头像良好对齐 */
  vertical-align: middle; /* 垂直居中 */
}

.el-avatar {
  vertical-align: middle; /* 垂直居中头像 */
}


/* 确保菜单项和子菜单标题遵守导航栏高度 */
:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 60px !important; /* 如有必要，覆盖默认样式 */
  line-height: 60px !important;
  display: inline-flex; /* 有助于垂直对齐 */
  align-items: center; /* 垂直居中 */
  border-bottom: none; /* 移除默认的下边框 */
}

/* 调整子菜单标题的内边距以获得更好的间距 */
:deep(.el-sub-menu__title) {
  padding: 0 10px; /* 根据需要调整 */
}


.auth-buttons {
  display: flex; /* 使用 flex 布局 */
  align-items: center; /* 垂直居中按钮 */
  gap: 10px; /* 按钮之间的间距 */
  /* 移除了 padding: 0 20px; 因为父元素已有内边距 */
}

/* 确保子菜单本身没有额外的下边框 */
.el-menu--horizontal > .el-sub-menu.user-menu {
  border-bottom: none;
}

/* 确保头像和用户名在标题内垂直居中 */
.el-sub-menu.user-menu :deep(.el-sub-menu__title) {
    display: inline-flex;
    align-items: center;
}
</style>
