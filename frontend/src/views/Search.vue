<template>
  <div class="search-container">
    <el-card class="search-card">
      <template #header>
        <div class="search-header">
          <h2>搜索结果</h2>
          <span class="search-count">共找到 {{ searchResults.length }} 个商品</span>
        </div>
      </template>

      <div v-if="searchResults.length === 0" class="no-results">
        <el-empty description="暂无相关商品" />
      </div>

      <div v-else class="product-grid">
        <el-row :gutter="20">
          <el-col v-for="product in searchResults" :key="product.id" :xs="24" :sm="12" :md="8" :lg="6">
            <el-card class="product-card" shadow="hover" @click="viewProduct(product.id)">
              <img :src="product.image" :alt="product.name" class="product-image" />
              <div class="product-info">
                <h3 class="product-name">{{ product.name }}</h3>
                <p class="product-price">¥{{ product.price }}</p>
                <p class="product-description">{{ product.description }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchProducts } from '@/api/products'

const route = useRoute()
const router = useRouter()
const searchResults = ref([])

onMounted(async () => {
  const query = route.query.q
  if (query) {
    try {
      const response = await searchProducts(query)
      searchResults.value = response.data
    } catch (error) {
      console.error('搜索失败:', error)
    }
  }
})

const viewProduct = (id) => {
  router.push(`/product/${id}`)
}
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-count {
  color: var(--text-color-secondary);
  font-size: 14px;
}

.product-grid {
  margin-top: 20px;
}

.product-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.product-info {
  padding: 10px 0;
}

.product-name {
  margin: 0;
  font-size: 16px;
  color: var(--text-color);
}

.product-price {
  margin: 8px 0;
  font-size: 18px;
  color: var(--danger-color);
  font-weight: bold;
}

.product-description {
  margin: 0;
  font-size: 14px;
  color: var(--text-color-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.no-results {
  text-align: center;
  padding: 40px 0;
}
</style> 