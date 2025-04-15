<template>
  <div class="cases-container">
    <el-card class="cases-card">
      <template #header>
        <div class="card-header">
          <span>成功案例</span>
          <el-input
            v-model="searchQuery"
            placeholder="搜索案例"
            class="search-input"
            clearable
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
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <el-card class="case-card" shadow="hover">
            <img :src="caseItem.image" class="case-image" />
            <div class="case-content">
              <h3 class="case-title">{{ caseItem.title }}</h3>
              <p class="case-summary">{{ caseItem.summary }}</p>
              <div class="case-meta">
                <span class="case-time">{{ caseItem.time }}</span>
                <span class="case-location">{{ caseItem.location }}</span>
              </div>
              <div class="case-tags">
                <el-tag
                  v-for="tag in caseItem.tags"
                  :key="tag"
                  size="small"
                  class="case-tag"
                >
                  {{ tag }}
                </el-tag>
              </div>
              <div class="case-actions">
                <el-button type="primary" link @click="viewCaseDetail(caseItem)">
                  查看详情
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[8, 16, 24, 32]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { usePoorStore } from '@/store/modules/poor'

const poorStore = usePoorStore()
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(8)
const total = ref(0)

// 模拟案例数据
const cases = ref([
  {
    id: 1,
    title: '养殖致富路',
    summary: '通过养殖技术培训和资金支持，帮助贫困户实现年收入翻倍',
    image: 'https://via.placeholder.com/300x200',
    time: '2024-02-15',
    location: '河南省信阳市',
    tags: ['养殖', '技术培训', '资金支持']
  },
  {
    id: 2,
    title: '电商助农记',
    summary: '通过电商平台帮助贫困户销售农产品，实现稳定增收',
    image: 'https://via.placeholder.com/300x200',
    time: '2024-01-20',
    location: '四川省凉山州',
    tags: ['电商', '农产品', '销售']
  },
  {
    id: 3,
    title: '教育改变命运',
    summary: '通过教育资助帮助贫困家庭子女完成学业，实现就业',
    image: 'https://via.placeholder.com/300x200',
    time: '2024-03-01',
    location: '贵州省毕节市',
    tags: ['教育', '就业', '技能培训']
  }
])

const filteredCases = computed(() => {
  if (!searchQuery.value) return cases.value
  const query = searchQuery.value.toLowerCase()
  return cases.value.filter(caseItem => 
    caseItem.title.toLowerCase().includes(query) ||
    caseItem.summary.toLowerCase().includes(query) ||
    caseItem.tags.some(tag => tag.toLowerCase().includes(query))
  )
})

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  // 这里可以调用 API 获取新的数据
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  // 这里可以调用 API 获取新的数据
}

const viewCaseDetail = (caseItem) => {
  // 跳转到案例详情页
  console.log('查看案例详情:', caseItem)
}
</script>

<style scoped>
.cases-container {
  padding: 20px;
}

.cases-card {
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

.case-card {
  margin-bottom: 20px;
  height: 100%;
}

.case-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.case-content {
  padding: 15px;
}

.case-title {
  margin: 0 0 10px 0;
  font-size: 18px;
  line-height: 1.4;
}

.case-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.case-meta {
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 12px;
  margin-bottom: 10px;
}

.case-tags {
  margin-bottom: 10px;
}

.case-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.case-actions {
  display: flex;
  justify-content: flex-end;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style> 