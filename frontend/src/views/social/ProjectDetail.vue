<template>
  <div class="project-detail">
    <el-card class="page-header">
      <div class="header-content">
        <h2>帮扶项目详情</h2>
        <div class="actions" v-if="isOwner">
          <el-button type="primary" @click="handleEdit">编辑项目</el-button>
          <el-button 
            v-if="project.status === 'draft'" 
            type="success" 
            @click="handlePublish"
          >发布项目</el-button>
          <el-button 
            v-if="project.status === 'published'" 
            type="warning" 
            @click="handleClose"
          >结束项目</el-button>
          <el-button type="danger" @click="handleDelete">删除项目</el-button>
        </div>
      </div>
    </el-card>

    <el-card v-loading="loading" class="project-content">
      <div v-if="project.id" class="project-info">
        <div class="project-image">
          <el-image 
            :src="project.image" 
            :preview-src-list="[project.image]"
            fit="cover"
            style="width: 100%; max-height: 300px; border-radius: 4px;"
          />
        </div>
        
        <div class="project-header">
          <h1>{{ project.name }}</h1>
          <el-tag :type="getStatusType(project.status)">
            {{ getStatusText(project.status) }}
          </el-tag>
        </div>
        
        <div class="project-meta">
          <p><strong>创建时间：</strong>{{ formatDate(project.created_at) }}</p>
          <p v-if="project.published_at"><strong>发布时间：</strong>{{ formatDate(project.published_at) }}</p>
          <p v-if="project.closed_at"><strong>结束时间：</strong>{{ formatDate(project.closed_at) }}</p>
        </div>
        
        <div class="project-description">
          <h3>项目简介</h3>
          <p>{{ project.description }}</p>
        </div>
        
        <div class="project-details">
          <h3>项目详情</h3>
          <p>{{ project.details }}</p>
        </div>
        
        <div class="project-requirements">
          <h3>帮扶要求</h3>
          <p>{{ project.requirements }}</p>
        </div>
        
        <div class="project-contact">
          <h3>联系方式</h3>
          <p><strong>联系人：</strong>{{ project.contact_name }}</p>
          <p><strong>联系电话：</strong>{{ project.contact_phone }}</p>
          <p><strong>联系邮箱：</strong>{{ project.contact_email }}</p>
        </div>
      </div>
      <div v-else class="not-found">
        <el-empty description="项目不存在或已被删除" />
      </div>
    </el-card>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <span>确定要删除项目 "{{ project.name }}" 吗？此操作不可恢复。</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjectDetail, deleteProject, publishProject, closeProject } from '@/api/project'
import { useUserStore } from '@/store/modules/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const project = ref({})
const loading = ref(true)
const deleteDialogVisible = ref(false)

// 判断当前用户是否为项目所有者
const isOwner = computed(() => {
  return project.value.user_id === userStore.userId
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

// 处理编辑项目
const handleEdit = () => {
  router.push(`/social/project-edit/${project.value.id}`)
}

// 处理发布项目
const handlePublish = async () => {
  try {
    await publishProject(project.value.id)
    ElMessage.success('项目发布成功')
    getDetail()
  } catch (error) {
    console.error('发布项目失败:', error)
    ElMessage.error('发布项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 处理结束项目
const handleClose = async () => {
  try {
    await closeProject(project.value.id)
    ElMessage.success('项目已结束')
    getDetail()
  } catch (error) {
    console.error('结束项目失败:', error)
    ElMessage.error('结束项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 处理删除项目
const handleDelete = () => {
  deleteDialogVisible.value = true
}

// 确认删除项目
const confirmDelete = async () => {
  try {
    await deleteProject(project.value.id)
    ElMessage.success('项目删除成功')
    deleteDialogVisible.value = false
    router.push('/social/project-manage')
  } catch (error) {
    console.error('删除项目失败:', error)
    ElMessage.error('删除项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
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
.project-requirements,
.project-contact {
  margin-top: 20px;
}

.project-description h3,
.project-details h3,
.project-requirements h3,
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