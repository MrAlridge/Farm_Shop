// src/utils/request.js
import axios from 'axios';
import { useUserStore } from '@/store/modules/user'; // Or your primary user store
// import { usePoorStore } from '@/store/modules/poor'; // If poor users have separate tokens
import { ElMessage } from 'element-plus';
import router from '@/router'; // Import router for redirection

const service = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Your Django backend API base URL
  timeout: 10000, // Request timeout
});

// 是否正在刷新token
let isRefreshing = false;
// 等待刷新token的请求队列
let requests = [];

// Request interceptor
service.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    // const poorStore = usePoorStore(); // Adjust if using a single token

    // Determine which token to use (adapt this logic if you have a unified auth)
    const token = userStore.token;

    if (token) {
      // Standard JWT approach
      config.headers['Authorization'] = `Bearer ${token}`;
      // If using Django's default TokenAuthentication
      // config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request Error:', error); // for debug
    return Promise.reject(error);
  }
);

// Response interceptor
service.interceptors.response.use(
  (response) => {
    // Directly return data if successful
    return response.data; // DRF typically wraps responses, often we just want the data
  },
  async (error) => {
    const userStore = useUserStore();
    
    if (error.response) {
      const { status } = error.response;
      const originalRequest = error.config;

      // token 失效的情况
      if (status === 401 && error.response.data.code === 'token_not_valid') {
        if (!isRefreshing) {
          isRefreshing = true;
          try {
            // 尝试刷新token
            const refreshSuccess = await userStore.refreshAccessToken();
            isRefreshing = false;

            if (refreshSuccess) {
              // 重新发送队列中的请求
              requests.forEach(cb => cb());
              requests = [];
              
              // 重试当前请求
              originalRequest.headers['Authorization'] = `Bearer ${userStore.token}`;
              return service(originalRequest);
            } else {
              // 刷新失败，清空队列
              requests.forEach(cb => cb(new Error('Token refresh failed')));
              requests = [];
              
              // 跳转到登录页
              router.push('/login');
              return Promise.reject(new Error('请重新登录'));
            }
          } catch (refreshError) {
            isRefreshing = false;
            // 刷新token失败，执行登出
            await userStore.logout();
            router.push('/login');
            return Promise.reject(refreshError);
          }
        } else {
          // 正在刷新token，将请求加入队列
          return new Promise((resolve, reject) => {
            requests.push((error) => {
              if (error) {
                reject(error);
              } else {
                originalRequest.headers['Authorization'] = `Bearer ${userStore.token}`;
                resolve(service(originalRequest));
              }
            });
          });
        }
      }
      
      // 其他错误处理
      switch (status) {
        case 403: // Forbidden
          ElMessage.error('权限不足，无法访问');
          break;
        case 404: // Not Found
           ElMessage.error('请求资源未找到');
           break;
        case 500:
           ElMessage.error('服务器内部错误');
           break;
        default:
          ElMessage.error(error.response.data.detail || '请求失败');
      }
    } else if (error.request) {
      // Request was made but no response received
      ElMessage.error('无法连接到服务器，请检查网络');
    } else {
      // Something happened in setting up the request
       ElMessage.error('请求发送失败');
    }
    
    ElMessage.error(error.message);
    return Promise.reject(error);
  }
);

export default service;