<template>
  <div class="home">
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="item in banners" :key="item.id">
        <img :src="item.image" :alt="item.title" class="banner-image">
      </el-carousel-item>
    </el-carousel>

    <div class="featured-products">
      <h2>精选商品</h2>
      <el-row :gutter="20">
        <el-col :span="6" v-for="product in featuredProducts" :key="product.id">
          <el-card :body-style="{ padding: '0px' }" class="product-card">
            <img :src="product.image" class="product-image">
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="price">¥{{ product.price }}</p>
              <el-button type="primary" @click="viewProduct(product.id)">查看详情</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="poverty-info">
      <h2>扶贫动态</h2>
      <el-timeline>
        <el-timeline-item
          v-for="(info, index) in povertyNews"
          :key="index"
          :timestamp="info.date"
          :type="info.type">
          {{ info.content }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 模拟数据
const banners = ref([
  { id: 1, image: '/banner1.jpg', title: '扶贫助农' },
  { id: 2, image: '/banner2.jpg', title: '优质农产品' },
  { id: 3, image: '/banner3.jpg', title: '乡村振兴' }
])

const featuredProducts = ref([
  { id: 1, name: '有机大米', price: 39.9, image: '/product1.jpg' },
  { id: 2, name: '土鸡蛋', price: 29.9, image: '/product2.jpg' },
  { id: 3, name: '山核桃', price: 49.9, image: '/product3.jpg' },
  { id: 4, name: '野生蜂蜜', price: 59.9, image: '/product4.jpg' }
])

const povertyNews = ref([
  { date: '2024-04-01', content: '某村农产品成功上线平台', type: 'success' },
  { date: '2024-03-15', content: '开展农产品种植技术培训', type: 'primary' },
  { date: '2024-03-01', content: '平台新增10个扶贫产品', type: 'warning' }
])

const viewProduct = (id) => {
  router.push(`/product/${id}`)
}
</script>

<style scoped>
.home {
  padding: 20px;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.featured-products {
  margin: 40px 0;
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

.poverty-info {
  margin: 40px 0;
}
</style> 