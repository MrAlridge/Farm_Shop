<template>
  <div class="policies-container">
    <el-card class="policies-card">
      <template #header>
        <div class="card-header">
          <span>扶贫政策</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索政策"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" class="policies-tabs">
        <el-tab-pane label="全部政策" name="all">
          <el-collapse v-model="activeCollapse">
            <el-collapse-item
              v-for="policy in filteredPolicies"
              :key="policy.id"
              :title="policy.title"
              :name="policy.id"
            >
              <div class="policy-content">
                <p class="policy-meta">
                  <span>发布时间：{{ policy.publishTime }}</span>
                  <span>发布单位：{{ policy.publisher }}</span>
                </p>
                <div class="policy-text" v-html="policy.content"></div>
                <div class="policy-actions">
                  <el-button type="primary" link @click="applyForPolicy(policy)">
                    申请该政策
                  </el-button>
                  <el-button type="primary" link @click="downloadPolicy(policy)">
                    下载政策文件
                  </el-button>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-tab-pane>
        
        <el-tab-pane label="已申请" name="applied">
          <el-table :data="appliedPolicies" style="width: 100%">
            <el-table-column prop="title" label="政策名称" />
            <el-table-column prop="applyTime" label="申请时间" width="180" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link @click="viewPolicyDetail(row)">
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
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { usePoorStore } from '@/store/modules/poor'

const poorStore = usePoorStore()
const searchQuery = ref('')
const activeTab = ref('all')
const activeCollapse = ref([])

// 模拟政策数据
const policies = ref([
  {
    id: 1,
    title: '农村危房改造补助政策',
    publishTime: '2024-01-15',
    publisher: '住房和城乡建设部',
    content: `
      <p>为改善农村贫困家庭住房条件，特制定本政策：</p>
      <p>1. 补助对象：建档立卡贫困户、低保户、农村分散供养特困人员、贫困残疾人家庭</p>
      <p>2. 补助标准：每户补助2-3万元</p>
      <p>3. 申请流程：向村委会提出申请，经审核后报乡镇政府审批</p>
    `,
    status: 'available'
  },
  {
    id: 2,
    title: '产业扶贫项目支持政策',
    publishTime: '2024-02-20',
    publisher: '农业农村部',
    content: `
      <p>为促进贫困地区产业发展，特制定本政策：</p>
      <p>1. 支持范围：特色种植、养殖、农产品加工等产业</p>
      <p>2. 支持方式：提供技术培训、资金补贴、市场对接等服务</p>
      <p>3. 申请条件：建档立卡贫困户，有产业发展意愿和能力</p>
    `,
    status: 'available'
  }
])

// 模拟已申请政策数据
const appliedPolicies = ref([
  {
    id: 3,
    title: '教育扶贫资助政策',
    applyTime: '2024-03-01',
    status: '审核中'
  }
])

const filteredPolicies = computed(() => {
  if (!searchQuery.value) return policies.value
  const query = searchQuery.value.toLowerCase()
  return policies.value.filter(policy => 
    policy.title.toLowerCase().includes(query) ||
    policy.content.toLowerCase().includes(query)
  )
})

const getStatusType = (status) => {
  const statusMap = {
    '审核中': 'warning',
    '已通过': 'success',
    '已拒绝': 'danger',
    'available': 'info'
  }
  return statusMap[status] || 'info'
}

const applyForPolicy = async (policy) => {
  try {
    await poorStore.applyForPolicy(policy.id)
    ElMessage.success('申请提交成功')
    // 更新已申请列表
    appliedPolicies.value.push({
      id: policy.id,
      title: policy.title,
      applyTime: new Date().toLocaleDateString(),
      status: '审核中'
    })
  } catch (error) {
    ElMessage.error(error.message || '申请失败')
  }
}

const downloadPolicy = (policy) => {
  // 模拟下载政策文件
  ElMessage.success('开始下载政策文件')
}

const viewPolicyDetail = (policy) => {
  // 跳转到政策详情页
  console.log('查看政策详情:', policy)
}
</script>

<style scoped>
.policies-container {
  padding: 20px;
}

.policies-card {
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

.policies-tabs {
  margin-top: 20px;
}

.policy-content {
  padding: 10px;
}

.policy-meta {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.policy-meta span {
  margin-right: 20px;
}

.policy-text {
  line-height: 1.6;
  margin-bottom: 15px;
}

.policy-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}
</style> 