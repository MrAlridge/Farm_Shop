import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
// 不再需要单独导入 poorStore 进行认证检查
// import { usePoorStore } from '@/store/modules/poor'

// --- 路由定义 ---
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页'
      // 允许所有用户访问，无需特殊 meta
    }
  },
  {
    path: '/login', // 统一登录入口
    name: 'Login',
    component: () => import('@/views/Login.vue'), // 使用统一的登录组件
    meta: {
      title: '登录',
      requiresGuest: true // 只允许未登录用户访问
    }
  },
  {
    path: '/register', // 统一注册入口
    name: 'Register',
    component: () => import('@/views/Register.vue'), // 使用统一的注册组件
    meta: {
      title: '注册',
      requiresGuest: true // 只允许未登录用户访问
    }
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('@/views/Products.vue'),
    meta: {
      title: '商品列表'
      // 允许所有用户访问
    }
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail.vue'),
    meta: {
      title: '商品详情'
      // 允许所有用户访问
    }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('@/views/Cart.vue'),
    meta: {
      title: '购物车',
      requiresAuth: true // 需要登录才能访问
      // allowedUserTypes: ['social'] // 示例：如果只有社会用户能访问购物车
    }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('@/views/Orders.vue'),
    meta: {
      title: '我的订单',
      requiresAuth: true // 需要登录
      // allowedUserTypes: ['social'] // 示例：如果只有社会用户能看订单
    }
  },
  {
    path: '/orders/:id',
    name: 'OrderDetail',
    component: () => import('@/views/OrderDetail.vue'),
    meta: {
      title: '订单详情',
      requiresAuth: true
    }
  },
  {
    path: '/user',
    name: 'UserCenterLayout', // 建议给布局路由一个清晰的名字
    component: () => import('@/views/UserCenter.vue'), // 用户中心布局
    redirect: { name: 'UserProfile' }, // 默认重定向到个人资料页
    meta: {
      title: '个人中心',
      requiresAuth: true // 需要登录
    },
    children: [
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('@/views/user/Profile.vue'),
        meta: { title: '个人资料' }
      },
      {
        path: 'address',
        name: 'UserAddress',
        component: () => import('@/views/user/Address.vue'),
        meta: { title: '收货地址'/*, allowedUserTypes: ['social']*/ } // 示例：如果只有社会用户有地址
      },
      {
        path: 'security',
        name: 'UserSecurity',
        component: () => import('@/views/user/Security.vue'),
        meta: { title: '安全设置' }
      }
    ]
  },
  {
    path: '/poverty-info',
    name: 'PovertyInfo',
    component: () => import('@/views/PovertyInfo.vue'), // 修正了 component 引用
    meta: {
      title: '扶贫信息'
      // 公开页面，无需登录
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/Search.vue'),
    meta: {
        title: '搜索结果'
    }
  },
  {
    path: '/blog/:id',
    name: 'BlogDetail',
    component: () => import('@/views/BlogDetail.vue'),
    meta: {
      title: '博客详情'
    }
  },
  // --- 贫困户专属功能区 ---
  {
    path: '/poor',
    name: 'PoorLayout',
    component: () => import('@/views/poor/Layout.vue'), // 贫困户功能区布局
    redirect: { name: 'PoorDashboard' }, // 默认重定向到仪表盘
    meta: {
        requiresAuth: true, // 需要登录
        allowedUserTypes: ['poor'] // *** 关键：只允许 'poor' 类型的用户访问 ***
    },
    children: [
      // 移除了 poor/login 和 poor/register
      {
        path: 'dashboard',
        name: 'PoorDashboard',
        component: () => import('@/views/poor/Dashboard.vue'),
        meta: { title: '扶贫工作台' }
      },
      {
        path: 'policies',
        name: 'PoorPolicies',
        component: () => import('@/views/poor/Policies.vue'),
        meta: { title: '扶贫政策' }
      },
      {
        path: 'cases',
        name: 'PoorCases',
        component: () => import('@/views/poor/Cases.vue'),
        meta: { title: '扶贫案例' }
      },
      {
        path: 'applications',
        name: 'PoorApplications',
        component: () => import('@/views/poor/Applications.vue'),
        meta: { title: '我的申请' }
      },
      {
        path: 'notifications',
        name: 'PoorNotifications',
        component: () => import('@/views/poor/Notifications.vue'),
        meta: { title: '通知消息' }
      },
      {
        path: 'product/publish',
        name: 'PoorProductPublish',
        component: () => import('@/views/poor/ProductPublish.vue'),
        meta: { title: '发布农产品' }
      },
      {
        path: 'shipping',
        name: 'PoorShipping',
        component: () => import('@/views/poor/Shipping.vue'),
        meta: { title: '发货管理' }
      },
      {
        path: 'assistance-projects',
        name: 'PoorAssistanceProjects',
        component: () => import('@/views/poor/AssistanceProjects.vue'),
        meta: { title: '帮扶项目' }
      },
      {
        path: 'project-detail/:id',
        name: 'PoorProjectDetail',
        component: () => import('@/views/poor/ProjectDetail.vue'),
        meta: { title: '项目详情' }
      }
      // ... 其他贫困户专属页面
    ]
  },
  // --- 社会力量帮扶专区 ---
  {
    path: '/social',
    name: 'SocialLayout',
    component: () => import('@/views/social/Layout.vue'),
    redirect: { name: 'ProjectManagement' },
    meta: {
      requiresAuth: true,
      allowedUserTypes: ['social']
    },
    children: [
      {
        path: '',
        redirect: '/social/project-manage'
      },
      {
        path: 'project-publish',
        name: 'ProjectPublish',
        component: () => import('@/views/social/ProjectPublish.vue'),
        meta: {
          title: '发布帮扶',
          requiresAuth: true,
          allowedUserTypes: ['social']
        }
      },
      {
        path: 'project-manage',
        name: 'ProjectManagement',
        component: () => import('@/views/social/ProjectManagement.vue'),
        meta: {
          title: '管理帮扶',
          requiresAuth: true,
          allowedUserTypes: ['social']
        }
      },
      {
        path: 'project-detail/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/social/ProjectDetail.vue'),
        meta: { title: '项目详情' }
      },
      {
        path: 'project-edit/:id',
        name: 'ProjectEdit',
        component: () => import('@/views/social/ProjectPublish.vue'),
        meta: { title: '编辑帮扶项目' }
      }
    ]
  },
  // --- 404 Not Found ---
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: {
        title: '页面未找到'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 路由切换时滚动到顶部
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// --- 全局前置守卫 ---
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  // 尝试在每次路由切换前获取用户信息（如果 token 存在但 userInfo 不存在）
  // 这有助于处理页面刷新后状态丢失的情况
  if (userStore.token && !userStore.userId) {
      console.log("Guard: Token exists but user info missing, attempting to fetch...");
      await userStore.fetchUserInfo(); // 等待用户信息获取完成
  }

  const isLoggedIn = userStore.isLoggedIn;
  const userType = userStore.userType;

  console.log(`Navigating to: ${to.path}`);
  console.log(`Route Meta:`, to.meta);
  console.log(`User LoggedIn: ${isLoggedIn}, UserType: ${userType}`);

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 扶贫助农平台` : '扶贫助农平台';

  // --- 权限检查逻辑 ---

  // 1. 检查是否是只允许 Guest 访问的页面 (如 Login, Register)
  if (to.meta.requiresGuest) {
    if (isLoggedIn) {
      console.log(`Guard: User logged in, redirecting from guest page ${to.path}`);
      // 根据用户类型重定向到不同的首页
      const redirectTarget = userType === 'poor' ? { name: 'PoorDashboard' } : { name: 'Home' };
      next(redirectTarget);
      return; // 阻止后续检查
    } else {
      // 未登录，允许访问 Guest 页面
      next();
      return;
    }
  }

  // 2. 检查是否需要登录认证
  if (to.meta.requiresAuth) {
    if (!isLoggedIn) {
       console.log(`Guard: Auth required for ${to.path}, redirecting to Login`);
       next({ name: 'Login', query: { redirect: to.fullPath } }); // 保存原始目标路径以便登录后跳转回来
       return; // 阻止后续检查
    }
    // --- 如果已登录，进行用户类型检查 ---
    if (to.meta.allowedUserTypes && Array.isArray(to.meta.allowedUserTypes)) {
       if (!to.meta.allowedUserTypes.includes(userType)) {
           console.log(`Guard: User type (${userType}) not allowed for ${to.path}. Allowed: ${to.meta.allowedUserTypes}. Redirecting.`);
           // 用户类型不匹配，可以重定向到首页或无权限页面
           ElMessage.warning('您没有权限访问此页面'); // 提示用户
           next({ name: 'Home' }); // 重定向到首页
           return; // 阻止后续检查
       }
       // 用户类型匹配，继续
    }
    // --- 如果不需要特定用户类型，或者类型匹配，则允许访问 ---
    console.log(`Guard: Access granted to ${to.path} for user type ${userType}`);
    next();
    return;
  }

  // --- 如果路由既不需要登录也不限制 Guest ---
  // (例如公共页面 Home, Products, PovertyInfo)
  console.log(`Guard: Public route ${to.path}, access granted.`);
  next();
});

export default router
