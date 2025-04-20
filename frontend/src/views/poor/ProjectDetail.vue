<template>
  <div class="project-detail">
    <el-card class="page-header">
      <div class="header-content">
        <h2>帮扶项目详情</h2>
        <div class="actions">
          <!-- <el-button type="primary" @click="handleApply" v-if="canApply">申请帮扶</el-button> -->
          <el-button @click="goBack">返回列表</el-button>
        </div>
      </div>
    </el-card>

    <el-card v-loading="loading" class="project-content">
      <div v-if="project.id" class="project-info">
        <div class="project-image" v-if="project.image || project.image_url">
          <el-image 
            :src="project.image || project.image_url" 
            :preview-src-list="[project.image || project.image_url]"
            fit="cover"
            style="width: 100%; max-height: 300px; border-radius: 4px;"
          />
        </div>
        
        <div class="project-header">
          <h1>{{ project.name }}</h1>
          <el-tag :type="getStatusType(project.status)">
            {{ project.status_display || getStatusText(project.status) }}
          </el-tag>
        </div>
        
        <div class="project-meta">
          <p><strong>发布时间：</strong>{{ formatDate(project.created_at) }}</p>
          <p><strong>发布单位：</strong>{{ project.supporter?.username || '未知' }}</p>
          <p v-if="project.start_date"><strong>开始时间：</strong>{{ formatDate(project.start_date) }}</p>
          <p v-if="project.end_date"><strong>结束时间：</strong>{{ formatDate(project.end_date) }}</p>
          <p v-if="project.deadline"><strong>申请截止：</strong>{{ formatDate(project.deadline) }}</p>
        </div>
        
        <div class="project-description">
          <h3>项目简介</h3>
          <p>{{ project.description }}</p>
        </div>
        
        <div class="project-details">
          <h3>项目详情</h3>
          <p>{{ project.content }}</p>
        </div>
        
        <div class="project-contact">
          <h3>联系方式</h3>
          <p><strong>联系人：</strong>{{ project.contact_person }}</p>
          <p><strong>联系电话：</strong>{{ project.contact_phone }}</p>
          <p><strong>联系邮箱：</strong>{{ project.contact_email }}</p>
        </div>
      </div>
      <div v-else class="not-found">
        <el-empty description="项目不存在或已被删除" />
      </div>
    </el-card>

    <!-- 申请确认对话框 -->
    <el-dialog
      v-model="applyDialogVisible"
      title="确认申请"
      width="30%"
    >
      <span>确定要申请项目 "{{ project.name }}" 吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="applyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmApply">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProjectDetail } from '@/api/project'
import { useUserStore } from '@/store/modules/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const project = ref({})
const loading = ref(true)
const applyDialogVisible = ref(false)

// 判断是否可以申请
const canApply = computed(() => {
  return project.value.status === 'published' && !project.value.has_applied
})

// 获取项目详情
const getDetail = async () => {
  loading.value = true
  try {
    const response = await getProjectDetail(route.params.id)
    project.value = response
  } catch (error) {
    console.error('获取项目详情失败:', error)
    ElMessage.error('获取项目详情失败: ' + (error.response?.data?.detail || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 处理申请项目
const handleApply = () => {
  applyDialogVisible.value = true
}

// 确认申请项目
const confirmApply = async () => {
  try {
    // TODO: 实现申请帮扶项目的API调用
    ElMessage.success('申请提交成功')
    applyDialogVisible.value = false
    // 刷新项目详情
    getDetail()
  } catch (error) {
    console.error('申请项目失败:', error)
    ElMessage.error('申请项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 返回列表
const goBack = () => {
  router.push('/poor/assistance-projects')
}

// 获取状态类型
const getStatusType = (status) => {
  switch (status) {
    case 'published':
      return 'success'
    case 'draft':
      return 'info'
    case 'closed':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case 'published':
      return '已发布'
    case 'draft':
      return '草稿'
    case 'closed':
      return '已结束'
    default:
      return '未知状态'
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 组件挂载时获取数据
onMounted(() => {
  getDetail()
})
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.project-content {
  margin-bottom: 20px;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-header h1 {
  margin: 0;
}

.project-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.project-meta p {
  margin: 0;
}

.project-description,
.project-details,
.project-contact {
  margin-top: 20px;
}

.project-description h3,
.project-details h3,
.project-contact h3 {
  margin-top: 0;
  margin-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}

.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}
</style> 