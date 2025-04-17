<template>
  <div class="project-management">
    <el-card class="page-header">
      <div class="header-content">
        <h2>管理帮扶项目</h2>
        <el-button type="primary" @click="handleCreate">发布新项目</el-button>
      </div>
    </el-card>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="项目状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable>
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="已结束" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称">
          <el-input v-model="filterForm.name" placeholder="输入项目名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading" class="project-list">
      <el-table :data="projects" style="width: 100%" v-if="projects.length > 0">
        <el-table-column prop="name" label="项目名称" min-width="180">
          <template #default="{ row }">
            <div class="project-name-cell">
              <el-image 
                :src="row.image" 
                :preview-src-list="[row.image]"
                fit="cover"
                style="width: 50px; height: 50px; border-radius: 4px; margin-right: 10px;"
              />
              <span>{{ row.name }}</span>
          </div>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="published_at" label="发布时间" width="180">
          <template #default="{ row }">
            {{ row.published_at ? formatDate(row.published_at) : '-' }}
              </template>
            </el-table-column>
        <el-table-column prop="closed_at" label="结束时间" width="180">
          <template #default="{ row }">
            {{ row.closed_at ? formatDate(row.closed_at) : '-' }}
              </template>
            </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleView(row)">查看</el-button>
            <el-button 
              v-if="row.status === 'draft'" 
              type="success" 
              size="small" 
              @click="handlePublish(row)"
            >发布</el-button>
            <el-button 
              v-if="row.status === 'published'" 
              type="warning" 
              size="small" 
              @click="handleClose(row)"
            >结束</el-button>
            <el-button 
              v-if="row.status === 'draft'" 
              type="primary" 
              size="small" 
              @click="handleEdit(row)"
            >编辑</el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(row)"
            >删除</el-button>
              </template>
            </el-table-column>
          </el-table>
      <el-empty v-else description="暂无项目数据" />
      
      <div class="pagination-container" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="30%"
    >
      <span>确定要删除项目 "{{ selectedProject?.name }}" 吗？此操作不可恢复。</span>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyProjects, deleteProject, publishProject, closeProject } from '@/api/project'

const router = useRouter()

// 数据列表
const projects = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选表单
const filterForm = reactive({
  status: '',
  name: ''
})

// 删除对话框
const deleteDialogVisible = ref(false)
const selectedProject = ref(null)

// 获取项目列表
const getProjects = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      ...filterForm
    }
    const response = await getMyProjects(params)
    
    // 检查响应格式并正确处理
    if (response && response.results) {
      // 直接使用 response.results 和 response.count
      projects.value = response.results
      total.value = response.count
    } else if (response && response.data && response.data.results) {
      // 兼容 response.data.results 格式
      projects.value = response.data.results
      total.value = response.data.count
    } else {
      // 处理其他可能的格式
      console.warn('API 响应格式不符合预期:', response)
      projects.value = []
      total.value = 0
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败: ' + (error.response?.data?.detail || '未知错误'))
    projects.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 处理创建项目
const handleCreate = () => {
  router.push('/social/project-publish')
}

// 处理查看项目
const handleView = (row) => {
  router.push(`/social/project-detail/${row.id}`)
}

// 处理编辑项目
const handleEdit = (row) => {
  router.push(`/social/project-edit/${row.id}`)
}

// 处理发布项目
const handlePublish = async (row) => {
  try {
    await publishProject(row.id)
    ElMessage.success('项目发布成功')
    getProjects()
  } catch (error) {
    console.error('发布项目失败:', error)
    ElMessage.error('发布项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 处理结束项目
const handleClose = async (row) => {
  try {
    await closeProject(row.id)
    ElMessage.success('项目已结束')
    getProjects()
  } catch (error) {
    console.error('结束项目失败:', error)
    ElMessage.error('结束项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 处理删除项目
const handleDelete = (row) => {
  selectedProject.value = row
  deleteDialogVisible.value = true
}

// 确认删除项目
const confirmDelete = async () => {
  if (!selectedProject.value) return
  
  try {
    await deleteProject(selectedProject.value.id)
    ElMessage.success('项目删除成功')
    deleteDialogVisible.value = false
    getProjects()
  } catch (error) {
    console.error('删除项目失败:', error)
    ElMessage.error('删除项目失败: ' + (error.response?.data?.detail || '未知错误'))
  }
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  getProjects()
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.status = ''
  filterForm.name = ''
  handleSearch()
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  getProjects()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  getProjects()
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
  getProjects()
})
</script>

<style scoped>
.project-management {
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

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.project-list {
  margin-bottom: 20px;
}

.project-name-cell {
  display: flex;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 