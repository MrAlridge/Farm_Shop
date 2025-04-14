<template>
  <div class="applications-container">
    <el-card class="applications-card">
      <template #header>
        <div class="card-header">
          <span>我的申请</span>
          <el-button type="primary" @click="handleNewApplication">
            提交新申请
          </el-button>
        </div>
      </template>
      
      <div v-if="error" class="error-message">
        <el-alert
          :title="error"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
      
      <el-tabs v-model="activeTab" class="applications-tabs">
        <el-tab-pane label="全部申请" name="all">
          <el-table 
            v-loading="loading"
            :data="applications" 
            style="width: 100%"
            :empty-text="loading ? '加载中...' : '暂无数据'"
          >
            <el-table-column prop="id" label="申请编号" width="120" />
            <el-table-column prop="type" label="申请类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getTypeTag(row.type)">
                  {{ getTypeText(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="申请项目" />
            <el-table-column prop="applyTime" label="申请时间" width="180" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  @click="viewApplicationDetail(row)"
                >
                  查看详情
                </el-button>
                <el-button
                  v-if="row.status === 'pending'"
                  type="danger"
                  link
                  @click="handleCancelApplication(row)"
                >
                  取消申请
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="待审核" name="pending">
          <el-table :data="pendingApplications" style="width: 100%">
            <el-table-column prop="id" label="申请编号" width="120" />
            <el-table-column prop="type" label="申请类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getTypeTag(row.type)">
                  {{ getTypeText(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="申请项目" />
            <el-table-column prop="applyTime" label="申请时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  @click="viewApplicationDetail(row)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="已通过" name="approved">
          <el-table :data="approvedApplications" style="width: 100%">
            <el-table-column prop="id" label="申请编号" width="120" />
            <el-table-column prop="type" label="申请类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getTypeTag(row.type)">
                  {{ getTypeText(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="申请项目" />
            <el-table-column prop="approveTime" label="通过时间" width="180" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  @click="viewApplicationDetail(row)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="已拒绝" name="rejected">
          <el-table :data="rejectedApplications" style="width: 100%">
            <el-table-column prop="id" label="申请编号" width="120" />
            <el-table-column prop="type" label="申请类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getTypeTag(row.type)">
                  {{ getTypeText(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="申请项目" />
            <el-table-column prop="rejectTime" label="拒绝时间" width="180" />
            <el-table-column prop="reason" label="拒绝原因" />
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  @click="viewApplicationDetail(row)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
// import { usePoorStore } from '@/store/modules/poor'
// import { getApplications, cancelApplication } from '@/api/poor'
import { getApplications, cancelApplication } from '@/api/user'
import { useUserStore } from '@/store/modules/user'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('all')
const applications = ref([])
const loading = ref(false)
const error = ref(null)

// 检查用户权限
const checkUserPermission = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.error('请先登录')
    router.push('/login')
    return false
  }
  
  if (!userStore.isPoorUser) {
    ElMessage.error('只有贫困户用户可以访问此页面')
    router.push('/')
    return false
  }
  
  return true
}

// 获取申请列表
const fetchApplications = async () => {
  if (!checkUserPermission()) return
  
  loading.value = true
  error.value = null
  
  try {
    // 先尝试刷新用户信息，确保token有效
    await userStore.fetchUserInfo()
    
    const response = await getApplications()
    applications.value = response.data
  } catch (err) {
    console.error('获取申请列表失败:', err)
    error.value = err.message
    
    if (err.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      await userStore.logout()
      router.push('/login')
    } else if (err.response?.status === 403) {
      ElMessage.error('没有权限访问此功能')
    } else {
      ElMessage.error(err.response?.data?.detail || '获取申请列表失败')
    }
  } finally {
    loading.value = false
  }
}

// 在组件挂载时获取数据
onMounted(async () => {
  await fetchApplications()
})

const pendingApplications = computed(() => 
  applications.value.filter(app => app.status === 'pending')
)

const approvedApplications = computed(() => 
  applications.value.filter(app => app.status === 'approved')
)

const rejectedApplications = computed(() => 
  applications.value.filter(app => app.status === 'rejected')
)

const getTypeTag = (type) => {
  const typeMap = {
    'policy': 'success',
    'project': 'primary',
    'material': 'warning',
    'education': 'info'
  }
  return typeMap[type] || 'info'
}

const getTypeText = (type) => {
  const typeMap = {
    'policy': '政策申请',
    'project': '项目申请',
    'material': '物资申请',
    'education': '教育申请'
  }
  return typeMap[type] || type
}

const getStatusType = (status) => {
  const statusMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝'
  }
  return statusMap[status] || status
}

const handleNewApplication = () => {
  router.push('/poor/policies')
}

const viewApplicationDetail = (application) => {
  router.push(`/poor/applications/${application.id}`)
}

const handleCancelApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消该申请吗？此操作不可恢复',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const loading = ElMessage.loading('正在取消申请...', 0)
    await cancelApplication(application.id)
    loading.close()
    
    await fetchApplications()
    ElMessage.success('申请已成功取消')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消申请失败:', error)
      ElMessage.error(error.message || '取消申请失败')
    }
  }
}
</script>

<style scoped>
.applications-container {
  padding: 20px;
}

.applications-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.applications-tabs {
  margin-top: 20px;
}

/* 添加一些响应式样式 */
@media screen and (max-width: 768px) {
  .applications-container {
    padding: 10px;
  }
  
  .el-table {
    font-size: 14px;
  }
}

.error-message {
  margin-bottom: 20px;
}
</style> 