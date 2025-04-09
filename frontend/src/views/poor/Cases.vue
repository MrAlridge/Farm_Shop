<template>
  <div class="cases-container">
    <el-row :gutter="20">
      <!-- 案例分类导航 -->
      <el-col :span="6">
        <el-card class="category-card">
          <template #header>
            <div class="card-header">
              <span>案例分类</span>
            </div>
          </template>
          <el-menu
            :default-active="activeCategory"
            class="category-menu"
            @select="handleCategorySelect"
          >
            <el-menu-item index="all">
              <el-icon><Collection /></el-icon>
              <span>全部案例</span>
            </el-menu-item>
            <el-menu-item index="industry">
              <el-icon><Shop /></el-icon>
              <span>产业扶贫</span>
            </el-menu-item>
            <el-menu-item index="education">
              <el-icon><Reading /></el-icon>
              <span>教育扶贫</span>
            </el-menu-item>
            <el-menu-item index="employment">
              <el-icon><Briefcase /></el-icon>
              <span>就业扶贫</span>
            </el-menu-item>
            <el-menu-item index="technology">
              <el-icon><Cpu /></el-icon>
              <span>科技扶贫</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 案例列表 -->
      <el-col :span="18">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>案例列表</span>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索案例"
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

          <el-row :gutter="20">
            <el-col
              v-for="caseItem in filteredCases"
              :key="caseItem.id"
              :span="8"
              class="case-item"
            >
              <el-card class="case-card" :body-style="{ padding: '0px' }">
                <img :src="caseItem.coverImage" class="case-image" />
                <div class="case-content">
                  <div class="case-header">
                    <h3 class="title">{{ caseItem.title }}</h3>
                    <el-tag :type="getCaseType(caseItem.type)">
                      {{ getCaseTypeText(caseItem.type) }}
                    </el-tag>
                  </div>
                  <div class="case-body">
                    <p class="summary">{{ caseItem.summary }}</p>
                    <div class="case-meta">
                      <span class="location">
                        <el-icon><Location /></el-icon>
                        {{ caseItem.location }}
                      </span>
                      <span class="time">
                        <el-icon><Timer /></el-icon>
                        {{ caseItem.publishTime }}
                      </span>
                    </div>
                  </div>
                  <div class="case-footer">
                    <el-button
                      type="primary"
                      size="small"
                      @click="viewCaseDetail(caseItem)"
                    >
                      查看详情
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>

          <!-- 分页 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              :page-sizes="[9, 18, 27, 36]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 案例详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="currentCase?.title"
      width="70%"
    >
      <div v-if="currentCase" class="case-detail">
        <div class="detail-header">
          <div class="meta-info">
            <span class="location">
              <el-icon><Location /></el-icon>
              {{ currentCase.location }}
            </span>
            <span class="time">
              <el-icon><Timer /></el-icon>
              {{ currentCase.publishTime }}
            </span>
            <span class="views">
              <el-icon><View /></el-icon>
              {{ currentCase.views }}
            </span>
          </div>
        </div>
        <div class="detail-content">
          <div class="case-images">
            <el-carousel :interval="4000" type="card" height="300px">
              <el-carousel-item v-for="image in currentCase.images" :key="image">
                <img :src="image" class="carousel-image" />
              </el-carousel-item>
            </el-carousel>
          </div>
          <div class="case-description" v-html="currentCase.content"></div>
          <div class="case-effect">
            <h4>扶贫效果</h4>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="脱贫人数">
                {{ currentCase.effect.peopleCount }}人
              </el-descriptions-item>
              <el-descriptions-item label="人均增收">
                {{ currentCase.effect.incomeIncrease }}元
              </el-descriptions-item>
              <el-descriptions-item label="产业规模">
                {{ currentCase.effect.industryScale }}
              </el-descriptions-item>
              <el-descriptions-item label="就业岗位">
                {{ currentCase.effect.jobCount }}个
              </el-descriptions-item>
            </el-descriptions>
          </div>
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
  Collection,
  Shop,
  Reading,
  Briefcase,
  Cpu,
  Search,
  Location,
  Timer,
  View
} from '@element-plus/icons-vue'

const poorStore = usePoorStore()
const activeCategory = ref('all')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(9)
const total = ref(0)
const cases = ref([])
const currentCase = ref(null)
const detailDialogVisible = ref(false)

// 获取案例类型
const getCaseType = (type) => {
  const typeMap = {
    'industry': 'success',
    'education': 'primary',
    'employment': 'warning',
    'technology': 'info'
  }
  return typeMap[type] || 'info'
}

// 获取案例类型文本
const getCaseTypeText = (type) => {
  const typeMap = {
    'industry': '产业扶贫',
    'education': '教育扶贫',
    'employment': '就业扶贫',
    'technology': '科技扶贫'
  }
  return typeMap[type] || type
}

// 处理分类选择
const handleCategorySelect = (index) => {
  activeCategory.value = index
  currentPage.value = 1
  fetchCases()
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchCases()
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchCases()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchCases()
}

// 查看案例详情
const viewCaseDetail = async (caseItem) => {
  try {
    const res = await poorStore.getCaseDetail(caseItem.id)
    currentCase.value = res.data
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取案例详情失败')
  }
}

// 获取案例列表
const fetchCases = async () => {
  try {
    const params = {
      category: activeCategory.value,
      keyword: searchKeyword.value,
      page: currentPage.value,
      pageSize: pageSize.value
    }
    const res = await poorStore.getCases(params)
    cases.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取案例列表失败')
  }
}

// 计算过滤后的案例列表
const filteredCases = computed(() => {
  return cases.value
})

onMounted(() => {
  fetchCases()
})
</script>

<style scoped>
.cases-container {
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

.case-item {
  margin-bottom: 20px;
}

.case-card {
  height: 100%;
  transition: all 0.3s;
}

.case-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.case-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.case-content {
  padding: 14px;
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.case-header .title {
  margin: 0;
  font-size: 16px;
  flex: 1;
  margin-right: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.case-body {
  margin-bottom: 10px;
}

.case-body .summary {
  color: var(--text-color-regular);
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.case-meta {
  display: flex;
  justify-content: space-between;
  color: var(--text-color-secondary);
  font-size: 14px;
}

.case-meta .location,
.case-meta .time {
  display: flex;
  align-items: center;
  gap: 4px;
}

.case-footer {
  display: flex;
  justify-content: flex-end;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.case-detail {
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

.case-images {
  margin-bottom: 20px;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.case-description {
  line-height: 1.8;
  margin-bottom: 20px;
}

.case-effect {
  margin-top: 20px;
}

.case-effect h4 {
  margin-bottom: 20px;
  color: var(--text-color-primary);
}

:deep(.el-card__header) {
  padding: 10px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-carousel__item) {
  border-radius: 8px;
  overflow: hidden;
}
</style> 