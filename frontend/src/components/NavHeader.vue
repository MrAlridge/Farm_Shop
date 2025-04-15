<template>
  <header class="nav-header">
    <div class="header-content">
      <div class="logo">
        <router-link to="/">
          <!-- <img src="@/assets/logo.png" alt="扶贫商城" /> -->
          <span>扶贫商城</span>
        </router-link>
      </div>
      
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索商品"
          class="search-input"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>

      <div class="nav-actions">
        <el-button-group>
          <el-button @click="$emit('toggle-dark-mode')">
            <el-icon><Moon v-if="!isDark" /><Sunny v-else /></el-icon>
          </el-button>
          <el-button v-if="!isLoggedIn" @click="$router.push('/login')">
            登录
          </el-button>
          <el-button v-if="!isLoggedIn" @click="$router.push('/register')">
            注册
          </el-button>
          <el-dropdown v-if="isLoggedIn">
            <span class="user-info">
              <el-avatar :size="32" :src="userAvatar" />
              <span>{{ username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/user')">
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/orders')">
                  我的订单
                </el-dropdown-item>
                <el-dropdown-item @click="handleLogout">
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button @click="$router.push('/cart')">
            <el-icon><ShoppingCart /></el-icon>
            <span v-if="cartCount > 0" class="cart-count">{{ cartCount }}</span>
          </el-button>
        </el-button-group>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { useCartStore } from '@/store/modules/cart'
import { Search, Moon, Sunny, ShoppingCart } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const searchQuery = ref('')
const isDark = ref(false)

const isLoggedIn = computed(() => userStore.isLoggedIn)
const username = computed(() => userStore.username)
const userAvatar = computed(() => userStore.avatar)
const cartCount = computed(() => cartStore.totalItems)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-header {
  background-color: var(--background-color);
  border-bottom: 1px solid var(--border-color);
  padding: 10px 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-color);
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.logo span {
  font-size: 20px;
  font-weight: bold;
}

.search-bar {
  flex: 1;
  max-width: 500px;
  margin: 0 20px;
}

.search-input {
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.cart-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: var(--danger-color);
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 12px;
}

.el-button {
  position: relative;
}
</style> 