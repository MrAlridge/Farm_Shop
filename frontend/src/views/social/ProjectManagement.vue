<template>
  <div class="project-management">
    <el-card class="page-header">
      <h2>帮扶项目管理</h2>
      <el-button type="primary" @click="showCreateDialog">发布新项目</el-button>
    </el-card>

    <!-- 项目列表 -->
    <el-card class="project-list">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="进行中" name="ongoing">
          <div v-if="ongoingProjects.length === 0" class="empty-state">
            <el-empty description="暂无进行中的项目" />
          </div>
          <el-table v-else :data="ongoingProjects" style="width: 100%">
            <el-table-column prop="title" label="项目名称" />
            <el-table-column prop="startDate" label="开始日期" />
            <el-table-column prop="endDate" label="结束日期" />
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button-group>
                  <el-button size="small" @click="viewProject(scope.row)">查看</el-button>
                  <el-button size="small" type="primary" @click="editProject(scope.row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteProject(scope.row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <div v-if="completedProjects.length === 0" class="empty-state">
            <el-empty description="暂无已完成的项目" />
          </div>
          <el-table v-else :data="completedProjects" style="width: 100%">
            <el-table-column prop="title" label="项目名称" />
            <el-table-column prop="startDate" label="开始日期" />
            <el-table-column prop="endDate" label="结束日期" />
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="viewProject(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 创建/编辑项目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑项目' : '发布新项目'"
      width="60%"
    >
      <el-form :model="projectForm" :rules="rules" ref="projectFormRef" label-width="100px">
        <el-form-item label="项目名称" prop="title">
          <el-input v-model="projectForm.title" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目类型" prop="type">
          <el-select v-model="projectForm.type" placeholder="请选择项目类型">
            <el-option label="技术培训" value="training" />
            <el-option label="资金支持" value="financial" />
            <el-option label="设备捐赠" value="equipment" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目时间" prop="dateRange">
          <el-date-picker
            v-model="projectForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item label="帮扶对象" prop="target">
          <el-select
            v-model="projectForm.target"
            multiple
            filterable
            placeholder="请选择帮扶对象"
          >
            <el-option
              v-for="item in poorUsers"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述"
          />
        </el-form-item>
        <el-form-item label="帮扶内容" prop="content">
          <el-input
            v-model="projectForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入帮扶内容"
          />
        </el-form-item>
        <el-form-item label="预期目标" prop="goals">
          <el-input
            v-model="projectForm.goals"
            type="textarea"
            :rows="4"
            placeholder="请输入预期目标"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitProject">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('ongoing')
const dialogVisible = ref(false)
const isEdit = ref(false)
const projectFormRef = ref(null)

// 模拟数据
const ongoingProjects = ref([
  {
    id: 1,
    title: '农业技术培训项目',
    startDate: '2024-04-01',
    endDate: '2024-06-30',
    status: 'ongoing',
    type: 'training',
    description: '为农户提供现代农业技术培训',
    content: '包括土壤管理、病虫害防治等技术培训',
    goals: '提高农户种植技术水平，增加产量'
  },
  {
    id: 2,
    title: '设备捐赠项目',
    startDate: '2024-05-01',
    endDate: '2024-07-31',
    status: 'ongoing',
    type: 'equipment',
    description: '捐赠农业机械设备',
    content: '提供现代化农业机械设备',
    goals: '提高农业生产效率'
  }
])

const completedProjects = ref([
  {
    id: 3,
    title: '资金支持项目',
    startDate: '2024-01-01',
    endDate: '2024-03-31',
    status: 'completed',
    type: 'financial',
    description: '提供创业资金支持',
    content: '为农户提供创业启动资金',
    goals: '帮助农户实现自主创业'
  }
])

const poorUsers = ref([
  { id: 1, name: '张三' },
  { id: 2, name: '李四' },
  { id: 3, name: '王五' }
])

const projectForm = ref({
  title: '',
  type: '',
  dateRange: [],
  target: [],
  description: '',
  content: '',
  goals: ''
})

const rules = {
  title: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择项目类型', trigger: 'change' }
  ],
  dateRange: [
    { required: true, message: '请选择项目时间', trigger: 'change' }
  ],
  target: [
    { required: true, message: '请选择帮扶对象', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入帮扶内容', trigger: 'blur' }
  ],
  goals: [
    { required: true, message: '请输入预期目标', trigger: 'blur' }
  ]
}

const getStatusType = (status) => {
  const types = {
    ongoing: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    ongoing: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

const showCreateDialog = () => {
  isEdit.value = false
  projectForm.value = {
    title: '',
    type: '',
    dateRange: [],
    target: [],
    description: '',
    content: '',
    goals: ''
  }
  dialogVisible.value = true
}

const editProject = (project) => {
  isEdit.value = true
  projectForm.value = {
    ...project,
    dateRange: [project.startDate, project.endDate]
  }
  dialogVisible.value = true
}

const viewProject = (project) => {
  // TODO: 实现查看项目详情功能
  console.log('查看项目:', project)
}

const deleteProject = (project) => {
  ElMessageBox.confirm(
    '确定要删除该项目吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现删除项目功能
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const submitProject = async () => {
  if (!projectFormRef.value) return
  
  await projectFormRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交项目功能
      ElMessage.success(isEdit.value ? '更新成功' : '发布成功')
      dialogVisible.value = false
    }
  })
}

onMounted(() => {
  // TODO: 从API获取项目列表和帮扶对象列表
})
</script>

<style scoped>
.project-management {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
}

.project-list {
  margin-bottom: 20px;
}

.empty-state {
  padding: 40px 0;
}

:deep(.el-tabs__nav) {
  margin-bottom: 20px;
}

:deep(.el-table) {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 