<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div class="user-info" v-if="userInfo">
            <el-avatar :size="64" :src="userInfo.avatar || ''" />
            <div class="info-content">
              <h3>{{ userInfo.username || '未登录' }}</h3>
              <p>家庭人口：{{ userInfo.family_members || 0 }}人</p>
              <p>年收入：{{ userInfo.annual_income || 0 }}元</p>
            </div>
          </div>
          <div v-else class="loading-info">
            <el-skeleton :rows="3" animated />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="action-row">
      <el-col :span="8">
        <el-card class="action-card" @click="goToProductPublish">
          <div class="action-content">
            <el-icon class="action-icon"><Goods /></el-icon>
            <div class="action-text">
              <h3>发布商品</h3>
              <p>发布您的农产品，增加收入</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="action-card" @click="goToAssistanceProjects">
          <div class="action-content">
            <el-icon class="action-icon"><Connection /></el-icon>
            <div class="action-text">
              <h3>帮扶项目</h3>
              <p>查看可申请的帮扶项目</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="action-card" @click="goToCases">
          <div class="action-content">
            <el-icon class="action-icon"><Star /></el-icon>
            <div class="action-text">
              <h3>成功案例</h3>
              <p>了解其他贫困户的成功经验</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { Goods, Connection, Star } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const userInfo = ref(null)

onMounted(async () => {
  try {
    // 先检查用户是否已登录
    if (!userStore.isLoggedIn) {
      console.warn('用户未登录，无法获取个人信息')
      return
    }
    
    // 获取用户信息
    await userStore.fetchUserInfo()
    
    // 更新本地 userInfo
    if (userStore.userInfo) {
      userInfo.value = userStore.userInfo
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})

// 导航函数
const goToProductPublish = () => {
  router.push('/poor/product/publish')
}

const goToAssistanceProjects = () => {
  router.push('/poor/assistance-projects')
}

const goToCases = () => {
  router.push('/poor/cases')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.info-card {
  height: 100%;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.loading-info {
  padding: 20px;
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

.action-row {
  margin-top: 20px;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.action-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  text-align: center;
}

.action-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.action-text h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.action-text p {
  margin: 0;
  color: #666;
  font-size: 14px;
}
</style> 