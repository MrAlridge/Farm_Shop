<template>
    <div>
      <h2>用户列表 (仅管理员)</h2>
      <ul v-if="users.length > 0">
        <li v-for="user in users" :key="user.id">
          {{ user.username }} - {{ user.email }} - {{user.user_type}}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import api from '@/api';
  
  export default {
    data() {
      return {
        users: [],
      };
    },
    async created() {
        if (localStorage.getItem('user_type')!=='admin') { //提前进行判断
           alert("权限不足");
            this.$router.push('/'); //返回首页
           return;
       }
      await this.getUsers();
    },
    methods: {
      async getUsers() {
        try {
          const response = await api.get('/users/users/');
          this.users = response.data.results;
        } catch (error) {
          console.error('获取用户列表失败', error);
        }
      },
    },
  };
  </script>