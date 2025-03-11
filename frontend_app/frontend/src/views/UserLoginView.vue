<template>
    <div class="login-container">
      <h1>用户登录</h1>
      <form @submit.prevent="login">  <div class="form-item">
          <label for="username">用户名/邮箱:</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名或邮箱">
        </div>
        <div class="form-item">
          <label for="password">密码:</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码">
        </div>
        <div class="form-item error-message" v-if="errorMessage">
          {{ errorMessage }}
        </div>
        <div class="form-item">
          <button type="submit">登录</button>
        </div>
        <div class="form-item register-link">
          <router-link to="/register">没有账号？去注册</router-link>  </div>
      </form>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    login() {
      this.errorMessage = ''; // 清空错误信息

      fetch('/api/login', {  //  替换为你的后端登录 API 地址
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
      .then(response => {
        if (!response.ok) {
          //  处理错误响应
          return response.json().then(errorData => {
            throw new Error(errorData.message || '登录失败'); //  假设后端返回 { message: '错误信息' }
          });
        }
        return response.json(); //  解析 JSON 格式的成功响应
      })
      .then(data => {
        //  登录成功，后端返回的数据 (例如 token)
        console.log('登录成功:', data);
        //  **存储 token (例如 localStorage)**
        localStorage.setItem('authToken', data.token); //  假设后端返回 { token: '...' }
        //  **跳转到主页面 (使用 vue-router)**
        this.$router.push('/'); //  假设主页路由路径为 '/'
      })
      .catch(error => {
        //  处理请求错误或登录失败错误
        console.error('登录错误:', error);
        this.errorMessage = error.message; //  显示错误信息
      });
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

.form-item {
  margin-bottom: 15px;
  text-align: left;
}

.form-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-item input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 3px;
}

.form-item button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.form-item button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 5px;
}

.register-link {
  text-align: center;
  margin-top: 10px;
}
</style>