<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div class="user-info">
            <el-avatar :size="64" :src="userInfo.avatar" />
            <div class="info-content">
              <h3>{{ userInfo.username }}</h3>
              <p>家庭人口：{{ userInfo.familyMembers }}人</p>
              <p>年收入：{{ userInfo.annualIncome }}元</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="16">
        <el-card class="status-card">
          <template #header>
            <div class="card-header">
              <span>申请状态</span>
            </div>
          </template>
          <el-steps :active="applicationStatus" finish-status="success">
            <el-step title="提交申请" description="已提交申请材料" />
            <el-step title="审核中" description="等待工作人员审核" />
            <el-step title="审核通过" description="申请已通过审核" />
            <el-step title="帮扶匹配" description="正在匹配帮扶项目" />
          </el-steps>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card class="project-card">
          <template #header>
            <div class="card-header">
              <span>帮扶项目</span>
              <el-button type="primary" link @click="viewAllProjects">查看全部</el-button>
            </div>
          </template>
          <el-table :data="projects" style="width: 100%">
            <el-table-column prop="name" label="项目名称" />
            <el-table-column prop="type" label="项目类型" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '已申请' ? 'success' : 'info'">
                  {{ row.status }}
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
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="notification-card">
          <template #header>
            <div class="card-header">
              <span>最新通知</span>
              <el-button type="primary" link @click="viewAllNotifications">查看全部</el-button>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(notification, index) in notifications"
              :key="index"
              :timestamp="notification.time"
            >
              {{ notification.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePoorStore } from '@/store/modules/poor'

const router = useRouter()
const poorStore = usePoorStore()

const userInfo = ref({
  username: '张三',
  avatar: '',
  familyMembers: 4,
  annualIncome: 12000
})

const applicationStatus = ref(2) // 0-3 表示申请进度

const projects = ref([
  {
    id: 1,
    name: '养殖技术培训',
    type: '技能培训',
    status: '已申请'
  },
  {
    id: 2,
    name: '农产品销售帮扶',
    type: '销售帮扶',
    status: '未申请'
  }
])

const notifications = ref([
  {
    time: '2024-03-20 10:00',
    content: '您的申请已通过审核，请等待帮扶项目匹配'
  },
  {
    time: '2024-03-19 15:30',
    content: '养殖技术培训项目已开始报名，请及时申请'
  }
])

const viewAllProjects = () => {
  router.push('/poor/policies')
}

const viewProjectDetail = (project) => {
  // 跳转到项目详情页
  console.log('查看项目详情:', project)
}

const viewAllNotifications = () => {
  router.push('/poor/notifications')
}

onMounted(async () => {
  try {
    await poorStore.fetchUserInfo()
    userInfo.value = { ...userInfo.value, ...poorStore.userInfo }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
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
  display: flex;
  align-items: center;
  gap: 20px;
}

.info-content h3 {
  margin: 0 0 10px 0;
}

.info-content p {
  margin: 5px 0;
  color: #666;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-card,
.notification-card {
  height: 100%;
}
</style> 