<template>
  <div class="product-list-container">
    <h2>产品列表</h2>

    <div class="product-list-header"> <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="搜索产品名称">
      </div>
      <div class="create-product-button">
        <router-link :to="{ name: 'product-create' }" class="button">创建新产品</router-link>
      </div>
    </div>

    <div v-if="loading" class="loading-indicator">
      加载中...
    </div>

    <div v-if="error" class="error-indicator">
      加载产品数据失败: {{ error.message }}
    </div>

    <ul v-if="!loading && !error && filteredProducts.length > 0" class="product-list">  <-- 修改 v-for 循环的目标为 filteredProducts -->
      <li v-for="product in filteredProducts" :key="product.id" class="product-item">
          <div class="product-image">
            <img :src="product.imageUrl" :alt="product.name" v-if="product.imageUrl">
            <div class="no-image" v-else>No Image</div>
          </div>
          <div class="product-details">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-price">价格: {{ product.price }} {{ product.unit }}</p>
            <p class="product-stock">库存: {{ product.stockQuantity }}</p>
          </div>
          <div class="product-actions">
            <router-link :to="{ name: 'product-edit', params: { id: product.id } }" class="edit-button">编辑</router-link>  <-- 使用 router-link -->
            <button class="delete-button" @click="deleteProduct(product.id)">删除</button> <!- 删除按钮保持不变，点击时调用 deleteProduct 方法 -->
          </div>
        </li>
    </ul>

    <div v-if="!loading && !error && filteredProducts.length === 0" class="no-products"> <p>暂无产品</p>
      <p>暂无产品</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'ProductList',
  setup() {
    const products = ref([]);   //  products 变为响应式引用，初始值为空数组
    const loading = ref(false); //  添加 loading 状态，指示数据加载中
    const error = ref(null);    //  添加 error 状态，用于显示错误信息
    
    const router = useRouter;   // 获取Router实例

    const fetchProducts = async () => {
      loading.value = true; //  开始加载时设置为 true
      error.value = null;   //  清空之前的错误信息
      try {
        const response = await fetch('http://127.0.0.1:8000/api/products'); //  替换为你的后端产品列表 API 地址
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        products.value = data; //  将从 API 获取的数据赋值给 products
      } catch (e) {
        error.value = e; //  捕获错误并赋值给 error
        console.error("Failed to fetch products:", e);
      } finally {
        loading.value = false; //  加载完成后设置为 false (无论成功或失败)
      }
    };

    onMounted(() => {
      fetchProducts(); //  组件挂载后立即调用 fetchProducts 函数
    });

    // * 搜索功能的代码
    const searchQuery = ref('');

    const filteredProducts = computed(() => {
      const query = searchQuery.value.toLowerCase();
      return products.value.filter(product => {
        return product.name.toLowerCase().includes(query); //  根据产品名称进行模糊搜索
      });
    });

    const deleteProduct = async (id) => {
      if (confirm('确定要删除该产品吗？')) { //  添加删除确认对话框
        loading.value = true;
        error.value = null;
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/products/${id}`, { //  发送 DELETE 请求
            method: 'DELETE',
          });
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          //  删除成功后，重新加载产品列表
          fetchProducts();
        } catch (e) {
          error.value = e;
          console.error("Failed to delete product:", e);
        } finally {
          loading.value = false;
        }
      }
    };

    const editProduct = (id) => { //  (可选) 如果你想在 script 中进行路由跳转，可以保留 editProduct 方法
      router.push(`/products/${id}/edit`);
    };

    return {
      products,
      loading,
      error,
      fetchProducts,
      searchQuery,
      filteredProducts,
      deleteProduct, //  暴露 deleteProduct 方法
      editProduct,   //  (可选) 暴露 editProduct 方法
    };
  },
};
</script>

<style scoped>
.product-list-container {
  padding: 20px;
}

.product-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* 响应式网格布局 */
  gap: 20px;
}

.product-item {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.product-image {
  width: 150px;
  height: 150px;
  margin-bottom: 10px;
  overflow: hidden;
  border-radius: 50%; /* 圆形图片 */
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 图片填充容器，保持比例 */
}

.product-image .no-image {
  width: 100%;
  height: 100%;
  background-color: #eee;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
}

.product-name {
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.product-price,
.product-stock {
  margin-bottom: 5px;
  color: #666;
}

.product-actions {
  margin-top: 10px;
}

.edit-button,
.delete-button {
  padding: 8px 15px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin: 0 5px;
}

.edit-button {
  background-color: #007bff;
  color: white;
}

.delete-button {
  background-color: #dc3545;
  color: white;
}

.no-products {
  text-align: center;
  padding: 20px;
  color: #777;
}

.search-bar {
  margin-bottom: 20px;
  text-align: center;
}

.search-bar input {
  width: 80%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.loading-indicator,
.error-indicator {
  text-align: center;
  padding: 20px;
  color: #777;
}

.product-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.create-product-button .button {
  padding: 10px 20px;
  background-color: #28a745; /*  绿色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none; /*  去除 router-link 默认的下划线 */
}

.create-product-button .button:hover {
  background-color: #218838; /*  hover 时的颜色 */
}
</style>