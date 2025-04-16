<template>
  <div class="project-submit">
    <el-card class="page-header">
      <h2>提交项目信息</h2>
    </el-card>

    <el-card class="submit-form">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
        class="project-form"
      >
        <!-- 项目选择 -->
        <!-- <div class="form-section">
          <h3>项目信息</h3>
          <el-form-item label="选择项目" prop="projectId">
            <el-select 
              v-model="formData.projectId" 
              placeholder="请选择要提交信息的项目"
              filterable
            >
              <el-option
                v-for="project in projects"
                :key="project.id"
                :label="project.name"
                :value="project.id"
              />
            </el-select>
          </el-form-item>
        </div> -->

        <!-- 进展信息 -->
        <div class="form-section">
          <h3>帮扶信息</h3>
          <!-- <el-form-item label="进展类型" prop="type">
            <el-select v-model="formData.type" placeholder="请选择进展类型">
              <el-option label="项目进展" value="progress" />
              <el-option label="问题反馈" value="issue" />
              <el-option label="成果展示" value="achievement" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item> -->

          <el-form-item label="标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入标题" />
          </el-form-item>

          <el-form-item label="内容" prop="content">
            <el-input
              v-model="formData.content"
              type="textarea"
              :rows="6"
              placeholder="请详细描述项目进展、问题或成果"
            />
          </el-form-item>

          <el-form-item label="相关图片">
            <el-upload
              class="submit-uploader"
              action="#"
              :auto-upload="false"
              :on-change="handleImageChange"
              :on-remove="handleImageRemove"
              :file-list="formData.images"
              multiple
            >
              <el-icon class="uploader-icon"><Plus /></el-icon>
              <div class="upload-tip">支持多张图片上传，每张不超过2MB</div>
            </el-upload>
          </el-form-item>
        </div>

        <!-- 数据统计 -->
        <div class="form-section" v-if="formData.type === 'progress' || formData.type === 'achievement'">
          <h3>数据统计</h3>
          <el-form-item label="帮扶人数" prop="helpedCount">
            <el-input-number 
              v-model="formData.helpedCount" 
              :min="0"
              placeholder="请输入帮扶人数"
            />
          </el-form-item>

          <el-form-item label="投入金额" prop="investment">
            <el-input-number 
              v-model="formData.investment" 
              :min="0"
              :precision="2"
              :step="1000"
              placeholder="请输入投入金额"
            />
            <span class="unit">元</span>
          </el-form-item>

          <el-form-item label="完成进度" prop="progress">
            <el-slider
              v-model="formData.progress"
              :step="5"
              :marks="{
                0: '0%',
                25: '25%',
                50: '50%',
                75: '75%',
                100: '100%'
              }"
            />
          </el-form-item>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="resetForm">重置</el-button>
          <el-button type="primary" @click="handleSubmit">提交信息</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const formRef = ref(null)
const imageList = ref([])

// 模拟项目数据
const projects = ref([
  { id: 1, name: '技术培训项目' },
  { id: 2, name: '资金支持项目' },
  { id: 3, name: '产品销售项目' }
])

const formData = ref({
  projectId: '',
  type: '',
  title: '',
  content: '',
  images: [],
  helpedCount: 0,
  investment: 0,
  progress: 0,
  statistics: null
})

// 表单验证规则
const rules = {
  projectId: [
    { required: true, message: '请选择项目', trigger: 'change' }
  ],
  type: [
    { required: true, message: '请选择进展类型', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入详细内容', trigger: 'blur' }
  ],
  helpedCount: [
    { required: true, message: '请输入帮扶人数', trigger: 'blur' }
  ],
  investment: [
    { required: true, message: '请输入投入金额', trigger: 'blur' }
  ],
  progress: [
    { required: true, message: '请选择完成进度', trigger: 'change' }
  ]
}

// 处理图片上传
const handleImageChange = (file) => {
  const isImage = file.raw.type.startsWith('image/')
  const isLt2M = file.raw.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 处理图片移除
const handleImageRemove = (file) => {
  const index = formData.value.images.indexOf(file)
  if (index !== -1) {
    formData.value.images.splice(index, 1)
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交信息的逻辑
      ElMessage.success('信息提交成功')
      resetForm()
    }
  })
}

// 重置表单
const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
  imageList.value = []
}

// 处理图片上传前的验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

// 处理图片上传成功
const handleUploadSuccess = (response, file) => {
  imageList.value.push({
    name: file.name,
    url: response.url
  })
}

// 处理图片上传失败
const handleUploadError = () => {
  ElMessage.error('图片上传失败')
}

// 移除图片
const handleRemove = (file) => {
  const index = formData.value.images.findIndex(item => item.name === file.name)
  if (index !== -1) {
    formData.value.images.splice(index, 1)
  }
}

// 监听进展类型变化
watch(() => formData.value.type, (newType) => {
  if (newType === 'progress' || newType === 'achievement') {
    formData.value.statistics = {
      beneficiaries: 0,
      investment: 0,
      progress: 0
    }
  } else {
    formData.value.statistics = null
  }
})
</script>

<style scoped>
.project-submit {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.submit-form {
  margin-bottom: 20px;
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #303133;
}

.submit-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 360px;
  height: 180px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-uploader:hover {
  border-color: #409eff;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.unit {
  margin-left: 10px;
  color: #606266;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}
</style> 