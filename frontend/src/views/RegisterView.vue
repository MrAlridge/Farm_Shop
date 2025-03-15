<template>
    <div>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input type="text" v-model="username" placeholder="Username" required>
         <input type="email" v-model="email" placeholder="Email" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <select v-model="user_type" required>
            <option value="social">社会人士</option>
            <option value="poor">贫困户</option>
             <option value="admin">管理员</option>
        </select>
        <button type="submit">Register</button>
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
        email: '',
        password: '',
        user_type: 'social',
        error: null
      };
    },
    methods: {
      async register() {
           try {
          const response = await api.post('/users/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          user_type: this.user_type
        });
          // 注册成功，跳转到登录页面
          this.$router.push('/login');
      }
      catch(error) {
          if (error.response && error.response.data) {
            const errorData = error.response.data;
               if(errorData.email){
                this.error = errorData.email[0]
              }
              else if (errorData.detail) {
                  this.error = errorData.detail;
              }
              else{
                 let errorMessages = [];
              for (const field in errorData) {
                errorMessages.push(`${field}: ${errorData[field].join(', ')}`);
              }
              this.error = errorMessages.join('; ');
              }
            }
            else{
               this.error = '无法连接到服务器';
            }
       }
      }
    }
  };
  </script>