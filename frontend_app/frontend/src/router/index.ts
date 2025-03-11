import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserRegisterView from '../views/UserRegisterView.vue' // 导入 UserRegisterView 组件
import UserLoginView from '@/views/UserLoginView.vue'
import ProductList from '@/components/ProductList.vue'
import ProductEdit from '@/components/ProductEdit.vue'
import ProductCreate from '@/components/ProductCreate.vue'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register', //  注册页面的路径
      name: 'register', //  路由名称，可以用于编程式导航
      component: UserRegisterView //  映射到 UserRegisterView 组件
    },
    {
      path: '/login',
      name: 'login',
      component: UserLoginView
    },
    {
      path: '/products',
      name: 'product',
      component: ProductList
    },
    {
      path: '/products/:id/edit',
      name: 'product-edit',
      component: ProductEdit,
      props: true
    },
    {
      path: '/products/create',
      name: 'product-create',
      component: ProductCreate
    },
    // ... 其他路由
  ]
})

export default router