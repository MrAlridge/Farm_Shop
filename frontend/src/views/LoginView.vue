<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="Username">
        <input type="password" v-model="password" placeholder="Password">
        <button type="submit">Login</button>
      </form>
      <p v-if="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  /* eslint-disable */
  import api from '@/api'; //引入Axios实例
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        error: null,
      };
    },
    methods: {
      async login() {
        try {
          const response = await api.post('/users/token/', { // 替换为你的登录 API 路径
            username: this.username,
            password: this.password,
          });
  
          const token = response.data.access;  //根据Django Simple JWT设置
            const refresh = response.data.refresh;
  
          // 存储 token
          localStorage.setItem('token', token);
          localStorage.setItem('refresh',refresh);
  
          // 跳转到首页或其他页面
          this.$router.push('/');
        } catch (error) {
            if (error.response && error.response.data) {
            // 获取详细错误信息
            const errorData = error.response.data;
  
            if (errorData.detail) {
              this.error = errorData.detail; // 显示通用错误信息
            } else {
              // 显示字段特定错误信息
              let errorMessages = [];
              for (const field in errorData) {
                errorMessages.push(`${field}: ${errorData[field].join(', ')}`);
              }
              this.error = errorMessages.join('; ');
            }
            } else {
            // 处理没有响应的错误（例如网络错误）
            this.error = '无法连接到服务器';
           }
          }
      },
    },
  };
  </script>