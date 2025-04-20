<template>
  <div class="assistance-projects-container">
    <el-card class="assistance-projects-card">
      <template #header>
        <div class="card-header">
          <span>帮扶项目</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索项目"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" class="assistance-projects-tabs">
        <el-tab-pane label="全部项目" name="all">
          <el-collapse v-model="activeCollapse">
            <el-collapse-item
              v-for="(project, index) in filteredProjects"
              :key="project?.id || index"
              :title="project?.name || '未命名项目'"
              :name="project?.id || index"
            >
              <div class="project-content">
                <div class="project-image" v-if="project.image || project.image_url">
                  <el-image 
                    :src="project.image || project.image_url" 
                    :preview-src-list="[project.image || project.image_url]"
                    fit="cover"
                    style="width: 100%; max-height: 200px; border-radius: 4px;"
                  />
                </div>
                <p class="project-meta">
                  <span>发布时间：{{ formatDate(project.created_at) }}</span>
                  <span>发布单位：{{ project.supporter?.username || '未知' }}</span>
                  <el-tag :type="getStatusType(project.status)">
                    {{ project.status_display || getStatusText(project.status) }}
                  </el-tag>
                </p>
                <div class="project-dates" v-if="project.start_date || project.end_date || project.deadline">
                  <p v-if="project.start_date"><strong>开始时间：</strong>{{ formatDate(project.start_date) }}</p>
                  <p v-if="project.end_date"><strong>结束时间：</strong>{{ formatDate(project.end_date) }}</p>
                  <p v-if="project.deadline"><strong>申请截止：</strong>{{ formatDate(project.deadline) }}</p>
                </div>
                <div class="project-description">
                  <h4>项目简介</h4>
                  <p>{{ project.description }}</p>
                </div>
                <div class="project-details">
                  <h4>项目详情</h4>
                  <p>{{ project.content }}</p>
                </div>
                <div class="project-contact">
                  <h4>联系方式</h4>
                  <p><strong>联系人：</strong>{{ project.contact_person }}</p>
                  <p><strong>联系电话：</strong>{{ project.contact_phone }}</p>
                  <p><strong>联系邮箱：</strong>{{ project.contact_email }}</p>
                </div>
                <div class="project-actions">
                  <!-- <el-button type="primary" @click="applyForProject(project)">
                    申请帮扶
                  </el-button> -->
                  <el-button type="primary" link @click="viewProjectDetail(project)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-tab-pane>
        
        <!-- <el-tab-pane label="已申请" name="applied">
          <el-table :data="appliedProjects" style="width: 100%">
            <el-table-column prop="name" label="项目名称" />
            <el-table-column prop="applyTime" label="申请时间" width="180" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link @click="viewProjectDetail(row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane> -->
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getPublishedProjects } from '@/api/project'
import { useUserStore } from '@/store/modules/user'

const router = useRouter()
const userStore = useUserStore()
const searchQuery = ref('')
const activeTab = ref('all')
const activeCollapse = ref([])
const projects = ref([])
const appliedProjects = ref([])
const loading = ref(false)

// 获取已发布的项目
const fetchProjects = async () => {
  loading.value = true
  try {
    const response = await getPublishedProjects()
    // 处理分页格式的响应
    if (response && response.results) {
      projects.value = response.results
    } else if (Array.isArray(response)) {
      projects.value = response
    } else {
      projects.value = []
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败: ' + (error.response?.data?.detail || '未知错误'))
    // 出错时设置为空数组
    projects.value = []
  } finally {
    loading.value = false
  }
}

// 过滤项目列表
const filteredProjects = computed(() => {
  // 确保 projects.value 是数组，并且过滤掉 null 值
  const validProjects = Array.isArray(projects.value) 
    ? projects.value.filter(project => project !== null) 
    : []
  
  if (!searchQuery.value) return validProjects
  
  const query = searchQuery.value.toLowerCase()
  return validProjects.filter(project => 
    (project?.name?.toLowerCase() || '').includes(query) ||
    (project?.description?.toLowerCase() || '').includes(query) ||
    (project?.content?.toLowerCase() || '').includes(query)
  )
})

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    'published': 'success',
    'draft': 'info',
    'closed': 'danger',
    '审核中': 'warning',
    '已通过': 'success',
    '已拒绝': 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'published': '已发布',
    'draft': '草稿',
    'closed': '已结束',
    '审核中': '审核中',
    '已通过': '已通过',
    '已拒绝': '已拒绝'
  }
  return statusMap[status] || '未知状态'
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

// 申请帮扶项目
const applyForProject = async (project) => {
  if (!project || !project.id) {
    ElMessage.warning('无法申请项目：项目信息无效')
    return
  }
  
  try {
    // TODO: 实现申请帮扶项目的API调用
    ElMessage.success('申请提交成功')
    // 更新已申请列表
    appliedProjects.value.push({
      id: project.id,
      name: project.name || '未命名项目',
      applyTime: new Date().toLocaleDateString(),
      status: '审核中'
    })
  } catch (error) {
    ElMessage.error(error.message || '申请失败')
  }
}

// 查看项目详情
const viewProjectDetail = (project) => {
  if (project && project.id) {
    router.push(`/poor/project-detail/${project.id}`)
  } else {
    ElMessage.warning('无法查看项目详情：项目ID无效')
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.assistance-projects-container {
  padding: 20px;
}

.assistance-projects-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 300px;
}

.assistance-projects-tabs {
  margin-top: 20px;
}

.project-content {
  padding: 10px;
}

.project-image {
  margin-bottom: 15px;
}

.project-meta {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.project-dates {
  margin-bottom: 15px;
}

.project-dates p {
  margin-bottom: 8px;
  color: #333;
}

.project-description,
.project-details,
.project-contact {
  margin-bottom: 15px;
}

.project-description h4,
.project-details h4,
.project-contact h4 {
  margin-bottom: 8px;
  color: #333;
}

.project-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}
</style> 