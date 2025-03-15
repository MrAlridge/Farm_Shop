//src/api/index.js
import axios from 'axios';
// import store from '@/store' //改回直接导入

const instance = axios.create({
 baseURL: '/api', // 根据你的 API 路由设置
 timeout: 5000, // 设置超时时间
});

// 添加请求拦截器
instance.interceptors.request.use(
 async (config) => {
   // 在发送请求之前做些什么，例如添加 token
   let token = localStorage.getItem('token');
   if (token) {
        // 判断token是否过期
       const decodedToken = JSON.parse(atob(token.split('.')[1])); //简单解码
       const currentTime = Math.floor(Date.now() / 1000);
        if (decodedToken.exp && decodedToken.exp < currentTime) {
          // token = await store.dispatch('refreshToken')
        }
     config.headers.Authorization = `Bearer ${token}`;
   }
   return config;
 },
 (error) => {
   // 对请求错误做些什么
   return Promise.reject(error);
 }
);

// 添加响应拦截器
instance.interceptors.response.use(
 (response) => {
   // 对响应数据做点什么
   return response;
 },
  async (error) => { //改为async函数
   // 对响应错误做点什么
   if (error.response && error.response.status === 401) {
     // 处理未授权的情况，例如跳转到登录页
      // await store.dispatch('logout'); //退出登录
      window.location.href = '/login' //需要您提前配置好router
   }
  else if(error.response && error.response.status === 403){
     alert('权限不足');
  }
   return Promise.reject(error);
 }
);
export default  instance ;