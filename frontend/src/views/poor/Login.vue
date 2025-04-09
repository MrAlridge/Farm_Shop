<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>贫困户登录</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
        class="login-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">
            登录
          </el-button>
          <el-button @click="resetForm">重置</el-button>
          <router-link to="/poor/register" class="register-link">
            还没有账号？立即注册
          </router-link>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { usePoorStore } from '@/store/modules/poor'
import { ElMessage } from 'element-plus'

const router = useRouter()
const poorStore = usePoorStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await poorStore.login(form)
        ElMessage.success('登录成功')
        router.push('/poor/dashboard')
      } catch (error) {
        ElMessage.error(error.message || '登录失败')
      } finally {
        loading.value = false
      }
    }
  })
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}
</script>

<style scoped>
.login-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 0 20px;
}

.login-card {
  border-radius: 8px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: var(--text-color);
}

.login-form {
  margin-top: 20px;
}

.register-link {
  margin-left: 20px;
  color: var(--primary-color);
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style> 