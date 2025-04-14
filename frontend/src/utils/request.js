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
  (error) => {
    console.error('Response Error:', error.response || error.message); // for debug
    let message = error.message;
    if (error.response) {
      // Backend returned an error response
      const data = error.response.data;
      message = data?.detail || // DRF standard error
                (typeof data === 'object' ? Object.values(data).flat().join('; ') : '请求失败'); // Handle validation errors etc.

      switch (error.response.status) {
        case 401: // Unauthorized
          ElMessage.error('认证失败，请重新登录');
          // Clear token and redirect to login
          const userStore = useUserStore();
          userStore.logout(); // Assuming logout clears token etc.
          // Determine login route based on context if needed, otherwise default
          router.push({ name: 'Login', query: { redirect: router.currentRoute.value.fullPath } });
          break;
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
          ElMessage.error(message || `请求错误: ${error.response.status}`);
      }
    } else if (error.request) {
      // Request was made but no response received
      message = '无法连接到服务器，请检查网络';
      ElMessage.error(message);
    } else {
      // Something happened in setting up the request
       ElMessage.error('请求发送失败');
    }
    
    ElMessage.error(message);
  }
);

export default service;