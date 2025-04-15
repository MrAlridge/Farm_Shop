<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
          <el-button type="primary" @click="handleEdit">编辑资料</el-button>
        </div>
      </template>

      <el-descriptions class="user-info" :column="2">
        <el-descriptions-item label="用户名">
          {{ userStore.username }}
        </el-descriptions-item>
        <el-descriptions-item label="当前身份">
          <el-tag :type="getUserTypeTag">{{ getUserTypeLabel }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="手机号码">
          {{ userStore.phoneNumber || '未设置' }}
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">
          {{ formatDate(userStore.userInfo.date_joined) }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 普通用户显示申请贫困户按钮 -->
      <div v-if="showPoorApplicationButton" class="apply-poor-section">
        <el-divider>申请贫困户身份</el-divider>
        <el-button 
          type="primary" 
          :disabled="hasPendingApplication"
          @click="handleApplyPoor"
        >
          {{ getApplyButtonText }}
        </el-button>
      </div>

      <!-- 申请历史记录 -->
      <div v-if="poorApplications.length > 0" class="application-history">
        <el-divider>申请历史</el-divider>
        <el-timeline>
          <el-timeline-item
            v-for="app in poorApplications"
            :key="app.id"
            :type="getTimelineItemType(app.status)"
            :timestamp="formatDate(app.created_at)"
          >
            <el-card class="application-card">
              <template #header>
                <div class="application-header">
                  <el-tag :type="getStatusType(app.status)">
                    {{ getStatusLabel(app.status) }}
                  </el-tag>
                </div>
              </template>
              <p>申请原因：{{ app.reason }}</p>
              <p v-if="app.review_comment">
                审核意见：{{ app.review_comment }}
              </p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>

    <!-- 申请贫困户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="申请贫困户身份"
      width="500px"
    >
      <el-form
        ref="applyFormRef"
        :model="applyForm"
        :rules="applyRules"
        label-width="100px"
      >
        <el-form-item label="申请原因" prop="reason">
          <el-input
            v-model="applyForm.reason"
            type="textarea"
            rows="4"
            placeholder="请详细说明申请原因"
          />
        </el-form-item>
        <el-form-item label="证明材料" prop="supporting_documents">
          <el-upload
            class="upload-demo"
            action="/api/upload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                请上传相关证明材料，支持jpg/png/pdf格式
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitApplication">
            提交申请
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'
import { getPoorApplications, submitPoorApplication } from '@/api/user'
import { formatDate } from '@/utils/format'

const userStore = useUserStore()
const dialogVisible = ref(false)
const poorApplications = ref([])
const applyFormRef = ref(null)

const applyForm = ref({
  reason: '',
  supporting_documents: null
})

const applyRules = {
  reason: [
    { required: true, message: '请输入申请原因', trigger: 'blur' },
    { min: 10, message: '申请原因至少10个字符', trigger: 'blur' }
  ]
}

// 计算属性
const getUserTypeLabel = computed(() => {
  const typeMap = {
    'social': '普通用户',
    'poor': '贫困户',
    'admin': '管理员'
  }
  return typeMap[userStore.userType] || '普通用户'
})

const getUserTypeTag = computed(() => {
  const typeMap = {
    'social': 'info',
    'poor': 'success',
    'admin': 'danger'
  }
  return typeMap[userStore.userType] || 'info'
})

const showPoorApplicationButton = computed(() => {
  return userStore.userType === 'social'
})

const hasPendingApplication = computed(() => {
  return poorApplications.value.some(app => app.status === 'pending')
})

const getApplyButtonText = computed(() => {
  return hasPendingApplication.value ? '审核中' : '申请成为贫困户'
})

// 方法
const handleEdit = () => {
  // 实现编辑个人资料的逻辑
}

const handleApplyPoor = () => {
  dialogVisible.value = true
}

const getTimelineItemType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusLabel = (status) => {
  const labelMap = {
    'pending': '审核中',
    'approved': '已通过',
    'rejected': '已拒绝'
  }
  return labelMap[status] || status
}

const handleUploadSuccess = (response) => {
  applyForm.value.supporting_documents = response.url
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const submitApplication = async () => {
  if (!applyFormRef.value) return
  
  await applyFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await submitPoorApplication(applyForm.value)
        ElMessage.success('申请提交成功')
        dialogVisible.value = false
        fetchApplications() // 刷新申请列表
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '提交申请失败')
      }
    }
  })
}

const fetchApplications = async () => {
  try {
    const response = await getPoorApplications()
    poorApplications.value = response.data
  } catch (error) {
    console.error('获取申请记录失败:', error)
  }
}

onMounted(() => {
  fetchApplications()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  margin-bottom: 20px;
}

.apply-poor-section {
  text-align: center;
  margin: 20px 0;
}

.application-history {
  margin-top: 30px;
}

.application-card {
  margin-bottom: 10px;
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 