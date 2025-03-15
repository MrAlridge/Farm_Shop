<template>
    <div>
      <h2>用户信息</h2>
      <p v-if="user">
        用户名：{{ user.username }}<br>
        邮箱：{{ user.email }}<br>
        用户类型: {{user.user_type}}
      </p>
      <p v-else>
        请先登录
      </p>
    </div>
  </template>
  
  <script>
  import api from '@/api';
  
  export default {
    data() {
      return {
        user: null,
      };
    },
    async created() {
      await this.getUserInfo();
    },
    methods: {
      async getUserInfo() {
        try {
          const response = await api.get('/users/userinfo/'); // 假设这是获取用户信息的 API
          this.user = response.data;
        } catch (error) {
          console.error('获取用户信息失败', error);
        }
      },
    },
  };
  </script>