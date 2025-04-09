import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { usePoorStore } from '@/store/modules/poor'

// 路由懒加载
const Home = () => import('../views/Home.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Products = () => import('../views/Products.vue')
const ProductDetail = () => import('../views/ProductDetail.vue')
const Cart = () => import('../views/Cart.vue')
const Orders = () => import('../views/Orders.vue')
const UserCenter = () => import('../views/UserCenter.vue')
const PovertyInfo = () => import('../views/PovertyInfo.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      requiresGuest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: {
      title: '注册',
      requiresGuest: true
    }
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/Products.vue'),
    meta: {
      title: '商品列表'
    }
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail.vue'),
    meta: {
      title: '商品详情'
    }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/Cart.vue'),
    meta: {
      title: '购物车',
      requiresAuth: true
    }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/Orders.vue'),
    meta: {
      title: '我的订单',
      requiresAuth: true
    }
  },
  {
    path: '/user',
    name: 'UserCenter',
    component: () => import('@/views/UserCenter.vue'),
    meta: {
      title: '个人中心',
      requiresAuth: true
    },
    children: [
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('@/views/user/Profile.vue')
      },
      {
        path: 'address',
        name: 'UserAddress',
        component: () => import('@/views/user/Address.vue')
      },
      {
        path: 'security',
        name: 'UserSecurity',
        component: () => import('@/views/user/Security.vue')
      }
    ]
  },
  {
    path: '/poverty-info',
    name: 'PovertyInfo',
    component: PovertyInfo,
    meta: {
      title: '扶贫信息'
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/Search.vue')
  },
  {
    path: '/poor',
    name: 'Poor',
    component: () => import('@/views/poor/Layout.vue'),
    meta: { requiresPoorAuth: true },
    children: [
      {
        path: 'login',
        name: 'PoorLogin',
        component: () => import('@/views/poor/Login.vue')
      },
      {
        path: 'register',
        name: 'PoorRegister',
        component: () => import('@/views/poor/Register.vue')
      },
      {
        path: 'dashboard',
        name: 'PoorDashboard',
        component: () => import('@/views/poor/Dashboard.vue')
      },
      {
        path: 'policies',
        name: 'PoorPolicies',
        component: () => import('@/views/poor/Policies.vue')
      },
      {
        path: 'cases',
        name: 'PoorCases',
        component: () => import('@/views/poor/Cases.vue')
      },
      {
        path: 'applications',
        name: 'PoorApplications',
        component: () => import('@/views/poor/Applications.vue')
      },
      {
        path: 'notifications',
        name: 'PoorNotifications',
        component: () => import('@/views/poor/Notifications.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const poorStore = usePoorStore()

  // 设置页面标题
  document.title = to.meta.title || '扶贫助农平台'

  // 需要普通用户认证的路由
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }

  // 需要贫困户认证的路由
  if (to.meta.requiresPoorAuth && !poorStore.isLoggedIn) {
    next('/poor/login')
    return
  }

  // 需要登录但未登录
  if (to.meta.requiresAuth && !localStorage.getItem('token')) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  // 需要未登录但已登录
  else if (to.meta.requiresGuest && localStorage.getItem('token')) {
    next({ name: 'Home' })
  }
  else {
    next()
  }
})

export default router 