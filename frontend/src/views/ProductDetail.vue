<template>
  <div class="product-detail">
    <el-row :gutter="20">
      <!-- 商品图片 -->
      <el-col :span="12">
        <el-carousel :interval="4000" type="card" height="400px">
          <el-carousel-item v-for="image in product.images" :key="image">
            <img :src="image" class="product-image">
          </el-carousel-item>
        </el-carousel>
      </el-col>
      
      <!-- 商品信息 -->
      <el-col :span="12">
        <div class="product-info">
          <h1>{{ product.name }}</h1>
          <p class="price">¥{{ product.price }}</p>
          <p class="sales">销量: {{ product.sales }}</p>
          <p class="stock">库存: {{ product.stock }}</p>
          
          <div class="quantity-selector">
            <span>数量：</span>
            <el-input-number
              v-model="quantity"
              :min="1"
              :max="product.stock"
              size="small" />
          </div>
          
          <div class="actions">
            <el-button type="primary" size="large" @click="addToCart">
              加入购物车
            </el-button>
            <el-button type="success" size="large" @click="buyNow">
              立即购买
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>
    
    <!-- 商品详情 -->
    <el-tabs v-model="activeTab" class="product-tabs">
      <el-tab-pane label="商品详情" name="detail">
        <div class="detail-content" v-html="product.detail"></div>
      </el-tab-pane>
      <el-tab-pane label="商品评价" name="reviews">
        <div class="reviews">
          <el-rate
            v-model="reviewForm.rating"
            :texts="['很差', '较差', '一般', '较好', '很好']"
            show-text />
          
          <el-input
            v-model="reviewForm.content"
            type="textarea"
            :rows="3"
            placeholder="请输入评价内容"
            class="review-input" />
          
          <el-button type="primary" @click="submitReview">提交评价</el-button>
          
          <div class="review-list">
            <div v-for="review in reviews" :key="review.id" class="review-item">
              <div class="review-header">
                <span class="username">{{ review.username }}</span>
                <el-rate v-model="review.rating" disabled />
                <span class="date">{{ review.date }}</span>
              </div>
              <p class="review-content">{{ review.content }}</p>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const productId = route.params.id

// 模拟商品数据
const product = ref({
  id: 1,
  name: '有机大米',
  price: 39.9,
  description: '产自山区，天然无污染，口感香糯',
  images: [
    '/images/products/product1.jpg',
    '/images/products/detail1.jpg',
    '/images/products/detail2.jpg',
    '/images/products/detail3.jpg'
  ],
  sales: 1000,
  stock: 500
})

const quantity = ref(1)
const activeTab = ref('detail')

// 评价表单
const reviewForm = reactive({
  rating: 5,
  content: ''
})

// 模拟评价数据
const reviews = ref([
  {
    id: 1,
    username: '用户1',
    rating: 5,
    content: '商品质量很好，非常满意！',
    date: '2024-04-01'
  },
  {
    id: 2,
    username: '用户2',
    rating: 4,
    content: '包装完好，物流很快。',
    date: '2024-03-28'
  }
])

const addToCart = () => {
  // TODO: 实现加入购物车逻辑
  ElMessage.success('已加入购物车')
}

const buyNow = () => {
  // TODO: 实现立即购买逻辑
  router.push('/cart')
}

const submitReview = () => {
  if (!reviewForm.content) {
    ElMessage.warning('请输入评价内容')
    return
  }
  
  // TODO: 实现提交评价逻辑
  ElMessage.success('评价提交成功')
  reviewForm.content = ''
}
</script>

<style scoped>
.product-detail {
  padding: 20px;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 20px;
}

.price {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
  margin: 20px 0;
}

.sales, .stock {
  color: #909399;
  margin: 10px 0;
}

.quantity-selector {
  margin: 20px 0;
  display: flex;
  align-items: center;
}

.actions {
  margin-top: 30px;
}

.actions .el-button {
  margin-right: 20px;
}

.product-tabs {
  margin-top: 40px;
}

.detail-content {
  padding: 20px;
}

.reviews {
  padding: 20px;
}

.review-input {
  margin: 20px 0;
}

.review-list {
  margin-top: 30px;
}

.review-item {
  border-bottom: 1px solid #ebeef5;
  padding: 20px 0;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.username {
  margin-right: 20px;
  font-weight: bold;
}

.date {
  margin-left: 20px;
  color: #909399;
}

.review-content {
  color: #606266;
  line-height: 1.5;
}
</style> 