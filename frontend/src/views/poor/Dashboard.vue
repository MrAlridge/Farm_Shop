<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 个人信息卡片 -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div class="user-info">
            <div class="info-item">
              <span class="label">用户名：</span>
              <span class="value">{{ userInfo.username }}</span>
            </div>
            <div class="info-item">
              <span class="label">家庭人数：</span>
              <span class="value">{{ userInfo.familyMembers }}人</span>
            </div>
            <div class="info-item">
              <span class="label">年收入：</span>
              <span class="value">{{ userInfo.annualIncome }}元</span>
            </div>
            <div class="info-item">
              <span class="label">家庭住址：</span>
              <span class="value">{{ userInfo.address }}</span>
            </div>
            <div class="info-item">
              <span class="label">申请状态：</span>
              <el-tag :type="getStatusType(userInfo.status)">
                {{ userInfo.status }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 帮扶项目卡片 -->
      <el-col :span="16">
        <el-card class="projects-card">
          <template #header>
            <div class="card-header">
              <span>可申请帮扶项目</span>
            </div>
          </template>
          <el-table :data="assistanceProjects" style="width: 100%">
            <el-table-column prop="name" label="项目名称" />
            <el-table-column prop="provider" label="提供方" />
            <el-table-column prop="description" label="项目描述" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  @click="applyForProject(row)"
                  :disabled="row.status !== 'available'"
                >
                  申请
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 物资援助卡片 -->
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card class="material-card">
          <template #header>
            <div class="card-header">
              <span>物资援助</span>
            </div>
          </template>
          <el-table :data="materialAssistance" style="width: 100%">
            <el-table-column prop="name" label="物资名称" />
            <el-table-column prop="quantity" label="数量" />
            <el-table-column prop="provider" label="提供方" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  @click="applyForMaterial(row)"
                  :disabled="row.status !== 'available'"
                >
                  申请
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <!-- 教育资助卡片 -->
      <el-col :span="12">
        <el-card class="education-card">
          <template #header>
            <div class="card-header">
              <span>教育资助</span>
            </div>
          </template>
          <el-table :data="educationAssistance" style="width: 100%">
            <el-table-column prop="name" label="资助项目" />
            <el-table-column prop="description" label="资助内容" />
            <el-table-column prop="provider" label="提供方" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  @click="applyForEducation(row)"
                  :disabled="row.status !== 'available'"
                >
                  申请
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePoorStore } from '@/store/modules/poor'
import { ElMessage } from 'element-plus'

const poorStore = usePoorStore()
const userInfo = ref({})
const assistanceProjects = ref([])
const materialAssistance = ref([])
const educationAssistance = ref([])

const getStatusType = (status) => {
  const statusMap = {
    'available': 'success',
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return statusMap[status] || 'info'
}

const applyForProject = async (project) => {
  try {
    await poorStore.applyForProject(project.id)
    ElMessage.success('申请提交成功')
    await fetchData()
  } catch (error) {
    ElMessage.error(error.message || '申请失败')
  }
}

const applyForMaterial = async (material) => {
  try {
    await poorStore.applyForMaterial(material.id)
    ElMessage.success('申请提交成功')
    await fetchData()
  } catch (error) {
    ElMessage.error(error.message || '申请失败')
  }
}

const applyForEducation = async (education) => {
  try {
    await poorStore.applyForEducation(education.id)
    ElMessage.success('申请提交成功')
    await fetchData()
  } catch (error) {
    ElMessage.error(error.message || '申请失败')
  }
}

const fetchData = async () => {
  try {
    const [userInfoRes, projectsRes, materialRes, educationRes] = await Promise.all([
      poorStore.getUserInfo(),
      poorStore.fetchAssistanceProjects(),
      poorStore.fetchMaterialAssistance(),
      poorStore.fetchEducationAssistance()
    ])
    userInfo.value = userInfoRes.data
    assistanceProjects.value = projectsRes.data
    materialAssistance.value = materialRes.data
    educationAssistance.value = educationRes.data
  } catch (error) {
    ElMessage.error('获取数据失败')
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.info-card {
  height: 100%;
}

.user-info {
  padding: 10px;
}

.info-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.info-item .label {
  width: 80px;
  color: var(--text-color-secondary);
}

.info-item .value {
  flex: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-card__header) {
  padding: 10px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}
</style> 