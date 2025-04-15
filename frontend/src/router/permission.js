import router from './index'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'

// 不需要登录就可以访问的路由
const publicRoutes = ['/login', '/register', '/404']

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 检查用户是否已登录
  if (userStore.isLoggedIn) {
    if (to.path === '/login') {
      // 已登录用户访问登录页，重定向到首页
      next('/')
    } else {
      // 检查用户信息是否已加载
      if (!userStore.userInfo.id) {
        try {
          await userStore.fetchUserInfo()
        } catch (error) {
          console.error('获取用户信息失败:', error)
        }
      }

      // 检查路由权限
      if (to.meta.requiresAuth) {
        const userType = userStore.userType
        const allowedTypes = to.meta.allowedUserTypes || []

        if (allowedTypes.length === 0 || allowedTypes.includes(userType)) {
          next()
        } else {
          ElMessage.error('您没有权限访问该页面')
          next('/403')
        }
      } else {
        next()
      }
    }
  } else {
    // 未登录用户
    if (publicRoutes.includes(to.path)) {
      next()
    } else {
      ElMessage.warning('请先登录')
      next(`/login?redirect=${to.path}`)
    }
  }
}) 