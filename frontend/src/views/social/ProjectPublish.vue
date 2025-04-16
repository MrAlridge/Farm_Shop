<template>
  <div class="project-publish">
    <el-card class="page-header">
      <h2>发布帮扶项目</h2>
    </el-card>

    <el-card class="publish-form">
      <el-form
        ref="formRef"
        :model="projectForm"
        :rules="rules"
        label-width="120px"
        class="project-form"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <h3>基本信息</h3>
          <el-form-item label="项目名称" prop="name">
            <el-input v-model="projectForm.name" placeholder="请输入项目名称" />
          </el-form-item>
          
          <el-form-item label="项目类型" prop="type">
            <el-select v-model="projectForm.type" placeholder="请选择项目类型">
              <el-option label="技术培训" value="training" />
              <el-option label="资金支持" value="financial" />
              <el-option label="产品销售" value="sales" />
              <el-option label="就业帮扶" value="employment" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>

          <el-form-item label="项目图片" prop="image">
            <el-upload
              class="project-uploader"
              :show-file-list="false"
              :before-upload="beforeImageUpload"
              :http-request="uploadImage"
            >
              <img v-if="projectForm.image" :src="projectForm.image" class="project-image" />
              <el-icon v-else class="uploader-icon"><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">建议尺寸：800x600px，支持 jpg、png 格式</div>
          </el-form-item>
        </div>

        <!-- 项目详情 -->
        <div class="form-section">
          <h3>项目详情</h3>
          <el-form-item label="项目简介" prop="description">
            <el-input
              v-model="projectForm.description"
              type="textarea"
              :rows="4"
              placeholder="请输入项目简介"
            />
          </el-form-item>

          <el-form-item label="项目内容" prop="content">
            <el-input
              v-model="projectForm.content"
              type="textarea"
              :rows="6"
              placeholder="请输入项目详细内容，如：帮扶方式、具体要求等"
            />
          </el-form-item>

          <el-form-item label="帮扶对象" prop="targetBeneficiaries">
            <el-input
              v-model="projectForm.targetBeneficiaries"
              type="textarea"
              :rows="3"
              placeholder="请描述帮扶对象的要求，如：年龄、地区、技能等"
            />
          </el-form-item>

          <el-form-item label="预期目标" prop="expectedGoals">
            <el-input
              v-model="projectForm.expectedGoals"
              type="textarea"
              :rows="3"
              placeholder="请描述项目的预期目标"
            />
          </el-form-item>
        </div>

        <!-- 时间安排 -->
        <div class="form-section">
          <h3>时间安排</h3>
          <el-form-item label="项目时间" prop="dateRange">
            <el-date-picker
              v-model="projectForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :min-date="new Date()"
            />
          </el-form-item>

          <el-form-item label="报名截止" prop="deadline">
            <el-date-picker
              v-model="projectForm.deadline"
              type="date"
              placeholder="选择报名截止日期"
              :min-date="new Date()"
            />
          </el-form-item>
        </div>

        <!-- 联系方式 -->
        <div class="form-section">
          <h3>联系方式</h3>
          <el-form-item label="联系人" prop="contactPerson">
            <el-input v-model="projectForm.contactPerson" placeholder="请输入联系人姓名" />
          </el-form-item>

          <el-form-item label="联系电话" prop="contactPhone">
            <el-input v-model="projectForm.contactPhone" placeholder="请输入联系电话" />
          </el-form-item>

          <el-form-item label="联系邮箱" prop="contactEmail">
            <el-input v-model="projectForm.contactEmail" placeholder="请输入联系邮箱" />
          </el-form-item>
        </div>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="resetForm">重置</el-button>
          <el-button type="primary" @click="submitForm">发布项目</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const formRef = ref(null)

// 表单数据
const projectForm = ref({
  name: '',
  type: '',
  image: '',
  description: '',
  content: '',
  targetBeneficiaries: '',
  expectedGoals: '',
  dateRange: [],
  deadline: '',
  contactPerson: '',
  contactPhone: '',
  contactEmail: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择项目类型', trigger: 'change' }
  ],
  image: [
    { required: true, message: '请上传项目图片', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入项目简介', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入项目内容', trigger: 'blur' }
  ],
  targetBeneficiaries: [
    { required: true, message: '请输入帮扶对象', trigger: 'blur' }
  ],
  expectedGoals: [
    { required: true, message: '请输入预期目标', trigger: 'blur' }
  ],
  dateRange: [
    { required: true, message: '请选择项目时间', trigger: 'change' }
  ],
  deadline: [
    { required: true, message: '请选择报名截止日期', trigger: 'change' }
  ],
  contactPerson: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  contactPhone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  contactEmail: [
    { required: true, message: '请输入联系邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 图片上传前的验证
const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

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

// 上传图片
const uploadImage = async (options) => {
  try {
    // TODO: 实现图片上传到服务器的逻辑
    // 这里模拟上传成功
    const reader = new FileReader()
    reader.readAsDataURL(options.file)
    reader.onload = () => {
      projectForm.value.image = reader.result
    }
    ElMessage.success('图片上传成功')
  } catch (error) {
    ElMessage.error('图片上传失败')
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交项目信息的逻辑
      ElMessage.success('项目发布成功')
      resetForm()
    }
  })
}
</script>

<style scoped>
.project-publish {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.publish-form {
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

.project-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 300px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.project-uploader:hover {
  border-color: #409eff;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.project-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
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