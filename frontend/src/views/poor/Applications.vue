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
      
      <el-tabs v-model="activeTab" class="applications-tabs">
        <el-tab-pane label="全部申请" name="all">
          <el-table :data="applications" style="width: 100%">
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
import { usePoorStore } from '@/store/modules/poor'
import { getApplications, cancelApplication } from '@/api/poor'

const router = useRouter()
const poorStore = usePoorStore()
const activeTab = ref('all')
const applications = ref([])

// 获取申请列表
const fetchApplications = async () => {
  try {
    const response = await getApplications()
    applications.value = response.data
  } catch (error) {
    ElMessage.error('获取申请列表失败')
  }
}

onMounted(() => {
  fetchApplications()
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
      '确定要取消该申请吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await cancelApplication(application.id)
    await fetchApplications()
    ElMessage.success('申请已取消')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消申请失败')
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
</style> 