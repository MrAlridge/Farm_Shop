<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>贫困户注册</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="register-form"
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

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="家庭人数" prop="familyMembers">
          <el-input-number
            v-model="form.familyMembers"
            :min="1"
            :max="10"
            controls-position="right"
          />
        </el-form-item>

        <el-form-item label="年收入" prop="annualIncome">
          <el-input-number
            v-model="form.annualIncome"
            :min="0"
            :step="1000"
            controls-position="right"
          >
            <template #append>元</template>
          </el-input-number>
        </el-form-item>

        <el-form-item label="家庭住址" prop="address">
          <el-input
            v-model="form.address"
            type="textarea"
            placeholder="请输入详细家庭住址"
          />
        </el-form-item>

        <el-form-item label="申请原因" prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            placeholder="请详细说明申请原因"
          />
        </el-form-item>

        <el-form-item label="证明材料" prop="documents">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            multiple
            :limit="5"
            :on-exceed="handleExceed"
          >
            <el-button type="primary">上传文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                请上传相关证明材料，如：低保证、残疾证等
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">
            提交注册
          </el-button>
          <el-button @click="resetForm">重置</el-button>
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
  password: '',
  confirmPassword: '',
  familyMembers: 1,
  annualIncome: 0,
  address: '',
  reason: '',
  documents: []
})

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (form.confirmPassword !== '') {
      formRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ],
  familyMembers: [
    { required: true, message: '请输入家庭人数', trigger: 'blur' }
  ],
  annualIncome: [
    { required: true, message: '请输入年收入', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入家庭住址', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请输入申请原因', trigger: 'blur' }
  ]
}

const handleRemove = (file, fileList) => {
  console.log(file, fileList)
}

const handlePreview = (file) => {
  console.log(file)
}

const handleExceed = (files, uploadFiles) => {
  ElMessage.warning(
    `当前限制选择 5 个文件，本次选择了 ${files.length} 个文件，共选择了 ${
      files.length + uploadFiles.length
    } 个文件`
  )
}

const beforeRemove = (file) => {
  return ElMessageBox.confirm(`确定移除 ${file.name}？`)
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await poorStore.register(form)
        ElMessage.success('注册成功，请等待审核')
        router.push('/poor/login')
      } catch (error) {
        ElMessage.error(error.message || '注册失败')
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
.register-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.register-card {
  border-radius: 8px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: var(--text-color);
}

.register-form {
  margin-top: 20px;
}

.el-upload__tip {
  color: var(--text-color-secondary);
  font-size: 12px;
  margin-top: 5px;
}

:deep(.el-upload-list__item) {
  transition: all 0.3s;
}

:deep(.el-upload-list__item:hover) {
  background-color: var(--background-color);
}
</style> 