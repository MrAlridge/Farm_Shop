<template>
  <div class="home">
    <el-carousel :interval="4000" type="card" height="400px">
      <el-carousel-item v-for="item in banners" :key="item.id" @click="viewBlog(item.id)">
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
  { id: 1, image: '/public/images/banner1.jpg', title: '扶贫助农', blogId: 1 },
  { id: 2, image: '/public/images/banner2.jpg', title: '优质农产品', blogId: 2 },
  { id: 3, image: '/public/images/banner3.jpg', title: '乡村振兴', blogId: 3 }
])

const featuredProducts = ref([
  { id: 1, name: '野生菌菇', price: 49.9, image: '/public/images/products/mushroom.jpg' },
  { id: 2, name: '有机大米', price: 24.9, image: '/public/images/products/rice2.png' },
  { id: 3, name: '山核桃', price: 19.9, image: '/public/images/products/peanut.jpg' },
  { id: 4, name: '土鸡蛋', price: 44.5, image: '/public/images/products/egg.jpg' }
])

const povertyNews = ref([
  { date: '2025-04-01', content: '某村农产品成功上线平台', type: 'success' },
  { date: '2025-03-15', content: '开展农产品种植技术培训', type: 'primary' },
  { date: '2025-03-01', content: '平台新增6个扶贫产品', type: 'warning' }
])

const viewProduct = (id) => {
  router.push(`/product/${id}`)
}

const viewBlog = (id) => {
  router.push(`/blog/${id}`)
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.hero-section {
  position: relative;
  height: 500px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
              url('/hero-bg.jpg') center/cover;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.hero-content {
  max-width: 800px;
  padding: 0 20px;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.hero-button {
  padding: 12px 30px;
  font-size: 1.2rem;
}

.section {
  padding: 60px 0;
  text-align: center;
}

.section-title {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.assistance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.assistance-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.assistance-card:hover {
  transform: translateY(-5px);
}

.assistance-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.assistance-content {
  padding: 20px;
}

.assistance-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.assistance-description {
  color: #666;
  margin-bottom: 1.5rem;
}

.assistance-button {
  width: 100%;
}

.news-section {
  background-color: #f9f9f9;
  padding: 60px 0;
}

.news-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.news-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.news-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.news-content {
  padding: 20px;
}

.news-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
}

.news-date {
  color: #999;
  font-size: 0.9rem;
}

.news-description {
  color: #666;
  margin-top: 1rem;
}

.contact-section {
  background-color: #fff;
  padding: 60px 0;
}

.contact-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.contact-card {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  text-align: center;
}

.contact-icon {
  font-size: 2.5rem;
  color: #409eff;
  margin-bottom: 1rem;
}

.contact-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
}

.contact-info {
  color: #666;
}

.footer {
  background-color: #333;
  color: white;
  padding: 40px 0;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.footer-link {
  color: white;
  text-decoration: none;
}

.footer-link:hover {
  text-decoration: underline;
}

.footer-copyright {
  color: #999;
}

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