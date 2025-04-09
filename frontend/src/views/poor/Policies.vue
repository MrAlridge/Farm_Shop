<template>
  <div class="policies-container">
    <el-row :gutter="20">
      <!-- 政策分类导航 -->
      <el-col :span="6">
        <el-card class="category-card">
          <template #header>
            <div class="card-header">
              <span>政策分类</span>
            </div>
          </template>
          <el-menu
            :default-active="activeCategory"
            class="category-menu"
            @select="handleCategorySelect"
          >
            <el-menu-item index="all">
              <el-icon><Document /></el-icon>
              <span>全部政策</span>
            </el-menu-item>
            <el-menu-item index="industry">
              <el-icon><Shop /></el-icon>
              <span>产业扶贫</span>
            </el-menu-item>
            <el-menu-item index="education">
              <el-icon><Reading /></el-icon>
              <span>教育扶贫</span>
            </el-menu-item>
            <el-menu-item index="health">
              <el-icon><FirstAidKit /></el-icon>
              <span>医疗扶贫</span>
            </el-menu-item>
            <el-menu-item index="employment">
              <el-icon><Briefcase /></el-icon>
              <span>就业扶贫</span>
            </el-menu-item>
            <el-menu-item index="housing">
              <el-icon><House /></el-icon>
              <span>住房保障</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 政策列表 -->
      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>政策列表</span>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索政策"
                class="search-input"
                clearable
                @clear="handleSearch"
                @input="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </template>

          <el-timeline>
            <el-timeline-item
              v-for="policy in filteredPolicies"
              :key="policy.id"
              :timestamp="policy.publishTime"
              placement="top"
            >
              <el-card class="policy-card">
                <div class="policy-content">
                  <div class="policy-header">
                    <h3 class="title">{{ policy.title }}</h3>
                    <el-tag :type="getPolicyType(policy.type)">
                      {{ getPolicyTypeText(policy.type) }}
                    </el-tag>
                  </div>
                  <div class="policy-body">
                    <p class="summary">{{ policy.summary }}</p>
                    <div class="policy-meta">
                      <span class="source">来源：{{ policy.source }}</span>
                      <span class="views">
                        <el-icon><View /></el-icon>
                        {{ policy.views }}
                      </span>
                    </div>
                  </div>
                  <div class="policy-footer">
                    <el-button
                      type="primary"
                      size="small"
                      @click="viewPolicyDetail(policy)"
                    >
                      查看详情
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>

          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[10, 20, 30, 50]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 政策详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="currentPolicy?.title"
      width="60%"
    >
      <div v-if="currentPolicy" class="policy-detail">
        <div class="detail-header">
          <div class="meta-info">
            <span class="source">来源：{{ currentPolicy.source }}</span>
            <span class="time">发布时间：{{ currentPolicy.publishTime }}</span>
            <span class="views">
              <el-icon><View /></el-icon>
              {{ currentPolicy.views }}
            </span>
          </div>
        </div>
        <div class="detail-content" v-html="currentPolicy.content"></div>
        <div class="detail-footer">
          <el-button type="primary" @click="downloadPolicy(currentPolicy)">
            下载政策文件
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePoorStore } from '@/store/modules/poor'
import { ElMessage } from 'element-plus'
import {
  Document,
  Shop,
  Reading,
  FirstAidKit,
  Briefcase,
  House,
  Search,
  View
} from '@element-plus/icons-vue'

const poorStore = usePoorStore()
const activeCategory = ref('all')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const policies = ref([])
const currentPolicy = ref(null)
const detailDialogVisible = ref(false)

// 获取政策类型
const getPolicyType = (type) => {
  const typeMap = {
    'industry': 'success',
    'education': 'primary',
    'health': 'warning',
    'employment': 'info',
    'housing': 'danger'
  }
  return typeMap[type] || 'info'
}

// 获取政策类型文本
const getPolicyTypeText = (type) => {
  const typeMap = {
    'industry': '产业扶贫',
    'education': '教育扶贫',
    'health': '医疗扶贫',
    'employment': '就业扶贫',
    'housing': '住房保障'
  }
  return typeMap[type] || type
}

// 处理分类选择
const handleCategorySelect = (index) => {
  activeCategory.value = index
  currentPage.value = 1
  fetchPolicies()
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchPolicies()
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchPolicies()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchPolicies()
}

// 查看政策详情
const viewPolicyDetail = async (policy) => {
  try {
    const res = await poorStore.getPolicyDetail(policy.id)
    currentPolicy.value = res.data
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取政策详情失败')
  }
}

// 下载政策文件
const downloadPolicy = async (policy) => {
  try {
    await poorStore.downloadPolicyFile(policy.id)
    ElMessage.success('下载成功')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

// 获取政策列表
const fetchPolicies = async () => {
  try {
    const params = {
      category: activeCategory.value,
      keyword: searchKeyword.value,
      page: currentPage.value,
      pageSize: pageSize.value
    }
    const res = await poorStore.getPolicies(params)
    policies.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取政策列表失败')
  }
}

// 计算过滤后的政策列表
const filteredPolicies = computed(() => {
  return policies.value
})

onMounted(() => {
  fetchPolicies()
})
</script>

<style scoped>
.policies-container {
  padding: 20px;
}

.category-card {
  height: 100%;
}

.category-menu {
  border-right: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 300px;
}

.policy-card {
  margin-bottom: 10px;
}

.policy-content {
  padding: 10px;
}

.policy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.policy-header .title {
  margin: 0;
  font-size: 18px;
}

.policy-body {
  margin-bottom: 10px;
}

.policy-body .summary {
  color: var(--text-color-regular);
  margin-bottom: 10px;
}

.policy-meta {
  display: flex;
  justify-content: space-between;
  color: var(--text-color-secondary);
  font-size: 14px;
}

.policy-footer {
  display: flex;
  justify-content: flex-end;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.policy-detail {
  padding: 20px;
}

.detail-header {
  margin-bottom: 20px;
}

.meta-info {
  display: flex;
  gap: 20px;
  color: var(--text-color-secondary);
  font-size: 14px;
}

.detail-content {
  line-height: 1.8;
  margin-bottom: 20px;
}

.detail-footer {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

:deep(.el-card__header) {
  padding: 10px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-timeline-item__node) {
  background-color: var(--el-color-primary);
}
</style> 