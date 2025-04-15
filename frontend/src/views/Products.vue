<template>
  <div class="products-container">
    <el-row :gutter="20">
      <!-- 筛选条件 -->
      <el-col :span="4">
        <el-card class="filter-card">
          <template #header>
            <div class="card-header">
              <span>筛选条件</span>
            </div>
          </template>
          
          <el-form :model="filterForm" label-width="80px">
            <el-form-item label="价格区间">
              <el-input-number v-model="filterForm.minPrice" :min="0" :max="1000" />
              <span class="price-separator">-</span>
              <el-input-number v-model="filterForm.maxPrice" :min="0" :max="1000" />
            </el-form-item>
            
            <el-form-item label="商品分类">
              <el-select v-model="filterForm.category" placeholder="请选择分类">
                <el-option
                  v-for="item in categories"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="排序方式">
              <el-select v-model="filterForm.sortBy" placeholder="请选择排序">
                <el-option label="价格从低到高" value="price_asc" />
                <el-option label="价格从高到低" value="price_desc" />
                <el-option label="销量从高到低" value="sales_desc" />
                <el-option label="最新上架" value="newest" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handleFilter">筛选</el-button>
              <el-button @click="resetFilter">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 商品列表 -->
      <el-col :span="20">
        <el-row :gutter="20">
          <el-col :span="6" v-for="product in products" :key="product.id">
            <el-card :body-style="{ padding: '0px' }" class="product-card">
              <img :src="product.image" class="product-image">
              <div class="product-info">
                <h3>{{ product.name }}</h3>
                <p class="price">¥{{ product.price }}</p>
                <p class="sales">销量: {{ product.sales }}</p>
                <el-button type="primary" @click="viewProduct(product.id)">
                  查看详情
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 36, 48]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProducts, getCategories } from '@/api/products'

const router = useRouter()

// 筛选表单
const filterForm = reactive({
  minPrice: 0,
  maxPrice: 1000,
  category: '',
  sortBy: ''
})

// 分类选项
const categories = ref([])

// 分页相关
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(100)

const products = ref([])

onMounted(async () => {
  try {
    const response = await getProducts()
    if (response && response.results) {
      products.value = response.results
      total.value = response.count
    } else {
      console.error('API响应格式不正确:', response)
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
  }

  try {
    const categoryResponse = await getCategories()
    categories.value = categoryResponse.map(cat => ({ value: cat.id, label: cat.name }))
  } catch (error) {
    console.error('获取商品分类失败:', error)
  }
})

const handleFilter = async () => {
  try {
    const response = await getProducts({
      min_price: filterForm.minPrice,
      max_price: filterForm.maxPrice,
      category: filterForm.category,
      sort_by: filterForm.sortBy
    })
    if (response && response.results) {
      products.value = response.results
      total.value = response.count
    } else {
      console.error('API响应格式不正确:', response)
    }
  } catch (error) {
    console.error('筛选商品失败:', error)
  }
}

const resetFilter = () => {
  filterForm.minPrice = 0
  filterForm.maxPrice = 1000
  filterForm.category = ''
  filterForm.sortBy = ''
}

const handleSizeChange = (val) => {
  pageSize.value = val
  // TODO: 重新加载数据
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  // TODO: 重新加载数据
}

const viewProduct = (id) => {
  router.push(`/product/${id}`)
}
</script>

<style scoped>
.products-container {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.price-separator {
  margin: 0 10px;
}

.product-card {
  margin-bottom: 20px;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-info {
  padding: 14px;
}

.price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin: 10px 0;
}

.sales {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.pagination-container {
  margin-top: 20px;
  text-align: center;
}
</style> 