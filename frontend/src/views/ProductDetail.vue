<template>
  <div class="product-detail">
    <el-row :gutter="20">
      <!-- 商品图片展示区 -->
      <el-col :span="12">
        <el-card class="image-card">
          <div v-if="!product.main_image" class="no-image">
            <el-empty description="暂无图片" />
          </div>
          <div v-else class="image-container">
            <el-image 
              :src="product.main_image" 
              fit="contain"
              :preview-src-list="[product.main_image]"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><picture-filled /></el-icon>
                  <span>图片加载失败</span>
                </div>
              </template>
            </el-image>
          </div>
        </el-card>
      </el-col>

      <!-- 商品信息区 -->
      <el-col :span="12">
        <el-card class="info-card">
          <div v-if="!product.id" class="loading-state">
            <el-skeleton :rows="6" animated />
          </div>
          <template v-else>
            <div class="product-header">
              <h1 class="product-name">{{ product.name }}</h1>
              <div class="product-meta">
                <el-tag size="small" type="info">{{ getCategoryName(product.category) }}</el-tag>
                <el-tag size="small" type="success" v-if="product.added_by?.user_type === 'poor'">帮扶农户</el-tag>
              </div>
            </div>

            <div class="product-price-section">
              <div class="price-main">
                <span class="price-symbol">¥</span>
                <span class="price-value">{{ product.price }}</span>
              </div>
              <div class="price-info">
                <span class="stock-info">库存: {{ product.stock }}</span>
                <span class="sales-info">销量: {{ product.sales }}</span>
              </div>
            </div>

            <el-divider />

            <div class="product-description">
              <h3>商品描述</h3>
              <p>{{ product.description }}</p>
            </div>

            <!-- <div class="product-seller">
              <h3>卖家信息</h3>
              <div class="seller-info">
                <el-avatar :size="40" :src="product.added_by?.avatar" />
                <div class="seller-details">
                  <p class="seller-name">{{ product.added_by?.username || '未知' }}</p>
                  <p class="seller-type" v-if="product.added_by?.user_type === 'poor'">帮扶农户</p>
                </div>
              </div>
            </div> -->

            <el-divider />

            <div class="purchase-section">
              <div class="quantity-selector">
                <span class="quantity-label">购买数量：</span>
                <el-input-number 
                  v-model="quantity" 
                  :min="1" 
                  :max="Math.max(1, product.stock)"
                  size="large"
                  :disabled="!product.stock"
                />
              </div>
              <div class="purchase-actions">
                <el-button 
                  type="primary" 
                  size="large" 
                  :disabled="!product.stock"
                  @click="addToCart"
                >
                  加入购物车
                </el-button>
              </div>
            </div>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <!-- 商品评价区 -->
    <el-row class="reviews-section">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="reviews-header">
              <h2>商品评价</h2>
              <el-button type="primary" @click="showReviewDialog">写评价</el-button>
            </div>
          </template>
          
          <div v-if="reviews.length > 0" class="reviews-list">
            <div v-for="review in reviews" :key="review.id" class="review-item">
              <div class="review-header">
                <el-avatar :size="40" :src="review.user.avatar" />
                <span class="review-username">{{ review.user.username }}</span>
                <el-rate v-model="review.rating" disabled />
                <span class="review-time">{{ formatDate(review.created_at) }}</span>
              </div>
              <div class="review-content">
                {{ review.content }}
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无评价" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 评价对话框 -->
    <el-dialog v-model="reviewDialogVisible" title="写评价" width="500px">
      <el-form :model="reviewForm" :rules="reviewRules" ref="reviewFormRef">
        <el-form-item label="评分" prop="rating">
          <el-rate v-model="reviewForm.rating" />
        </el-form-item>
        <el-form-item label="评价内容" prop="content">
          <el-input
            v-model="reviewForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入您的评价内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="reviewDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReview">提交评价</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProductDetail, getProductReviews, submitReview as submitReviewApi, getCategories } from '@/api/product'
import { formatDate } from '@/utils/format'

const route = useRoute()
const product = ref({
  name: '',
  price: 0,
  stock: 0,
  description: '',
  images: [],
  main_image: '',
  sales: 0,
  category: '',
  added_by: null
})
const reviews = ref([])
const quantity = ref(1)
const reviewDialogVisible = ref(false)
const reviewFormRef = ref(null)

const reviewForm = ref({
  rating: 5,
  content: ''
})

const reviewRules = {
  rating: [
    { required: true, message: '请选择评分', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入评价内容', trigger: 'blur' },
    { min: 10, message: '评价内容至少10个字符', trigger: 'blur' }
  ]
}

const categories = ref([])

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 获取分类名称
const getCategoryName = (categoryId) => {
  if (!categories.value || !categoryId) return '未知分类'
  const category = categories.value.find(c => c.id === categoryId)
  return category ? category.name : '未知分类'
}

// 获取商品详情
const fetchProductDetail = async () => {
  try {
    const response = await getProductDetail(route.params.id)
    if (response) {
      const data = response
      product.value = {
        id: data.id,
        name: data.name || '',
        price: parseFloat(data.price) || 0,
        stock: data.stock || 0,
        description: data.description || '暂无描述',
        images: data.image ? [data.image] : [],
        main_image: data.image || '',
        sales: data.sales || 0,
        category: data.category || '',
        added_by: data.added_by || null,
        created_at: data.created_at || '',
        updated_at: data.updated_at || ''
      }
    }
  } catch (error) {
    console.error('获取商品详情失败:', error)
    ElMessage.error('获取商品详情失败')
  }
}

// 获取商品评价
const fetchReviews = async () => {
  try {
    const response = await getProductReviews(route.params.id)
    reviews.value = response.data
  } catch (error) {
    ElMessage.error('获取商品评价失败')
  }
}

// 加入购物车
const addToCart = () => {
  // TODO: 实现加入购物车功能
  ElMessage.success('已加入购物车')
}

// 显示评价对话框
const showReviewDialog = () => {
  reviewDialogVisible.value = true
}

// 提交评价
const submitReview = async () => {
  if (!reviewFormRef.value) return
  
  await reviewFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // await submitReviewApi(route.params.id, reviewForm.value)
        ElMessage.success('评价提交成功')
        reviewDialogVisible.value = false
        // await fetchReviews()
        reviewForm.value = {
          rating: 5,
          content: ''
        }
      } catch (error) {
        ElMessage.error('评价提交失败')
      }
    }
  })
}

onMounted(() => {
  fetchProductDetail()
  fetchCategories()
  // fetchReviews()
})
</script>

<style scoped>
.product-detail {
  padding: 20px;
}

.image-card {
  margin-bottom: 20px;
}

.info-card {
  height: 100%;
  min-height: 400px;
}

.product-header {
  margin-bottom: 20px;
}

.product-name {
  font-size: 24px;
  margin-bottom: 10px;
  color: #303133;
}

.product-meta {
  display: flex;
  gap: 10px;
}

.product-price-section {
  margin: 20px 0;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
}

.price-main {
  display: flex;
  align-items: baseline;
  margin-bottom: 10px;
}

.price-symbol {
  font-size: 20px;
  color: #f56c6c;
  margin-right: 4px;
}

.price-value {
  font-size: 36px;
  color: #f56c6c;
  font-weight: bold;
}

.price-info {
  display: flex;
  gap: 20px;
  color: #909399;
  font-size: 14px;
}

.product-description {
  margin: 20px 0;
}

.product-description h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
}

.product-seller {
  margin: 20px 0;
}

.seller-info {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
}

.seller-details {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.seller-name {
  font-weight: bold;
  color: #303133;
}

.seller-type {
  color: #67c23a;
  font-size: 14px;
}

.purchase-section {
  margin-top: 30px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.quantity-label {
  color: #606266;
}

.purchase-actions {
  display: flex;
  justify-content: center;
}

.purchase-actions .el-button {
  width: 100%;
  height: 50px;
  font-size: 16px;
}

.reviews-section {
  margin-top: 20px;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.review-username {
  font-weight: bold;
}

.review-time {
  color: #999;
  font-size: 12px;
}

.review-content {
  color: #666;
  line-height: 1.6;
}

.image-container {
  width: 100%;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
}

.image-container :deep(.el-image) {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.no-image {
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.image-error {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #909399;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.loading-state {
  padding: 20px;
}
</style> 