<template>
    <div class="user-register">
      <h1>用户注册</h1>
      <form @submit.prevent="registerUser">
        <div>
          <label for="username">用户名:</label>
          <input type="text" id="username" v-model="username">
        </div>
        <div>
          <label for="password">密码:</label>
          <input type="password" id="password" v-model="password">
        </div>
        <div>
          <label for="user_type">用户类型:</label>
          <select id="user_type" v-model="user_type">
            <option value="poor_household">贫困户</option>
            <option value="admin">管理员</option>
            <option value="company">社会公司</option>
            <option value="volunteer">志愿者</option>
          </select>
        </div>
        <button type="submit">注册</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    name: 'UserRegisterView',
    setup() {
      const username = ref('');
      const password = ref('');
      const user_type = ref('poor_household'); // 默认用户类型为贫困户
  
      const registerUser = () => {
        // 在这里编写用户注册的逻辑，例如调用后端 API
        console.log('注册用户信息:', {
          username: username.value,
          password: password.value,
          user_type: user_type.value
        });
        //  TODO: 调用后端用户注册 API
      };
  
      return {
        username,
        password,
        user_type,
        registerUser
      };
    }
  });
  </script>
  
  <style scoped>
  .user-register {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .user-register h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .user-register div {
    margin-bottom: 10px;
  }
  
  .user-register label {
    display: inline-block;
    width: 80px;
    text-align: right;
    margin-right: 10px;
  }
  
  .user-register input,
  .user-register select {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 3px;
    width: 200px;
  }
  
  .user-register button {
    padding: 10px 20px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  </style>