import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView,
    meta: { requiresAuth: true }, // 需要登录
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView,
  },
 {
    path: '/register',
    name: 'RegisterView',
    component: RegisterView,
  },
  // ... 其他路由
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach(async (to, from, next) => { //改为async函数
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      const token = localStorage.getItem('token');
       if (!token) {
        //const { default: store } = await import('@/store'); //如果需要store中的数据，动态导入
        next({
          path: '/login',
          query: { redirect: to.fullPath }, // 保存用户要访问的页面
        });
      } else {

        next();
      }
    } else {
      next(); // 不需要登录，直接放行
    }
  });
export default router;