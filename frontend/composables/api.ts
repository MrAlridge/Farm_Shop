// composables/api.ts
import axios from 'axios';
import { Product } from '@/components/types';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // 你的 Django API 地址
  headers: {
    'Content-Type': 'application/json',
    // 如果需要认证，可以在这里添加 Authorization header
    // 'Authorization': `Bearer ${token}`
  },
});

export const fetchProducts = async (): Promise<Product[]> => {
  try {
    const response = await api.get('products/');
    return response.data;
  } catch (error) {
    handleApiError(error);
    throw error; // 或者返回一个空数组或错误对象
  }
};

export const fetchProductDetails = async (id: number): Promise<Product> => {
  try {
    const response = await api.get(`products/${id}/`);
    return response.data;
  } catch (error) {
    handleApiError(error);
    throw error; // 抛出错误，以便调用者可以处理
  }
};

// 购物车和用户认证的 API 请求也写在这里...

// 错误处理函数 (可选，但强烈推荐)
const handleApiError = (error: any) => {
  if (axios.isAxiosError(error)) {
    // Axios 错误 (网络错误、超时等)
    if (error.response) {
      // 服务器返回了错误状态码 (4xx, 5xx)
      console.error('Server Error:', error.response.status, error.response.data);
      // 可以根据 error.response.status 来显示不同的错误消息
    } else {
      // 请求发送了，但没有收到响应 (例如，网络问题)
      console.error('Network Error:', error.message);
    }
  } else {
    // 其他类型的错误
    console.error('An unexpected error occurred:', error);
  }
};