// src/utils/request.js
import axios from 'axios';
import { ElMessage } from 'element-plus';
import router from '@/router';
import { useUserStore } from '@/store/modules/user';

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    const userStore = useUserStore();
    const token = userStore.token;
    
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data;
  },
  async error => {
    const userStore = useUserStore();
    
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 如果是刷新token的请求失败，直接登出
          if (error.config.url.includes('/token/refresh/')) {
            await userStore.logout();
            router.push('/login');
            return Promise.reject(error);
          }
          
          // 尝试刷新token
          try {
            const success = await userStore.refreshAccessToken();
            if (success) {
              // 重试原始请求
              const config = error.config;
              config.headers['Authorization'] = `Bearer ${userStore.token}`;
              return service(config);
            } else {
              await userStore.logout();
              router.push('/login');
            }
          } catch (refreshError) {
            await userStore.logout();
            router.push('/login');
          }
          break;
          
        case 403:
          ElMessage.error('没有权限执行此操作');
          break;
          
        case 404:
          ElMessage.error('请求的资源不存在');
          break;
          
        case 500:
          ElMessage.error('服务器错误，请稍后重试');
          break;
          
        default:
          ElMessage.error(error.response.data?.detail || '请求失败');
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接');
    } else {
      ElMessage.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

export default service;