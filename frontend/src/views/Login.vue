<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>用户登录</h2>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginData"
        :rules="rules"
        label-width="80px"
        class="login-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginData.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="请输入密码"
            show-password>
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="身份" prop="role">
          <el-radio-group v-model="loginData.role">
            <el-radio label="user">普通用户</el-radio>
            <el-radio label="poor">贫困户</el-radio>
            <el-radio label="social">帮扶单位</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading">
            登录
          </el-button>
          <el-button @click="goToRegister">注册账号</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const loginFormRef = ref(null)

const loginData = reactive({
  username: '',
  password: '',
  role: 'user' // 默认选择普通用户
})

const loading = ref(false)

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择身份', trigger: 'change' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      const success = await userStore.login(loginData);
      loading.value = false;
      if (success) {
        const redirect = route.query.redirect || '/';
        router.push(redirect);
      }
    } else {
      console.log('表单验证失败');
      return false;
    }
  })
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  position: relative;
  height: 100vh;
  width: 50vw;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  
  /* 添加伪元素作为背景 */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/images/bg.jpg'); /* 调整图片路径 */
    background-size:cover;
    background-position: center;
    background-repeat: no-repeat;
    /* filter: blur(1px); */
    z-index: 0;
  }
}

.login-card {
  width: 450px;
  z-index: 1; /* 确保卡片在背景上方 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  /* 标题样式 */
  h2 {
    text-align: center;
    color: #303133;
  }
}

.login-form {
  margin: 20px;
  
  /* 按钮容器样式 */
  .el-form-item:last-child {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;
  }

  /* 单选框组样式 */
  .el-radio-group {
    display: flex;
    gap: 20px;
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    margin: 0 20px;
  }
}

</style> 