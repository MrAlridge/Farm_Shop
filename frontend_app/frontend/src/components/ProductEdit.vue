<template>
    <div class="product-edit-container">
      <h2>编辑产品</h2>
  
      <div v-if="loading" class="loading-indicator">
        加载中...
      </div>
      <div v-if="error" class="error-indicator">
        加载产品信息失败: {{ error.message }}
      </div>
  
      <form v-if="!loading && !error && product" @submit.prevent="updateProduct">
        <div class="form-item">
          <label for="name">产品名称:</label>
          <input type="text" id="name" v-model="product.name">
        </div>
        <div class="form-item">
          <label for="description">产品描述:</label>
          <textarea id="description" v-model="product.description"></textarea>
        </div>
        <div class="form-item">
          <label for="category">产品分类:</label>
          <input type="text" id="category" v-model="product.category">
        </div>
        <div class="form-item">
          <label for="price">价格:</label>
          <input type="number" id="price" v-model.number="product.price">
        </div>
        <div class="form-item">
          <label for="unit">单位:</label>
          <input type="text" id="unit" v-model="product.unit">
        </div>
        <div class="form-item">
          <label for="stockQuantity">库存:</label>
          <input type="number" id="stockQuantity" v-model.number="product.stockQuantity">
        </div>
        <div class="form-item">
          <label for="imageUrl">图片 URL:</label>
          <input type="text" id="imageUrl" v-model="product.imageUrl">
        </div>
  
        <div class="form-actions">
          <button type="submit" class="save-button">保存</button>
          <button type="button" class="cancel-button" @click="cancelEdit">取消</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter, useRoute } from 'vue-router'; // 导入 useRouter 和 useRoute
  
  export default {
    name: 'ProductEdit',
    props: {
      id: {
        type: String, // 或 Number，取决于你的 product.id 类型
        required: true,
      },
    },
    setup(props) {
      const product = ref(null);
      const loading = ref(false);
      const error = ref(null);
      const router = useRouter(); // 获取 router 实例
      const route = useRoute();   // 获取 route 实例
  
      const fetchProduct = async () => {
        loading.value = true;
        error.value = null;
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/products/${props.id}`); //  使用 props.id 获取产品 ID
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          product.value = data;
        } catch (e) {
          error.value = e;
          console.error("Failed to fetch product:", e);
        } finally {
          loading.value = false;
        }
      };
  
      const updateProduct = async () => {
        loading.value = true;
        error.value = null;
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/products/${props.id}`, {  //  使用 props.id
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(product.value),
          });
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          //  编辑成功，跳转回产品列表页
          router.push('/products');
        } catch (e) {
          error.value = e;
          console.error("Failed to update product:", e);
        } finally {
          loading.value = false;
        }
      };
  
      const cancelEdit = () => {
        router.push('/products'); //  取消编辑，跳转回产品列表页
      };
  
      onMounted(() => {
        fetchProduct(); // 组件挂载后获取产品信息
      });
  
      return {
        product,
        loading,
        error,
        fetchProduct,
        updateProduct,
        cancelEdit,
      };
    },
  };
  </script>
  
  <style scoped>
  .product-edit-container {
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .form-item {
    margin-bottom: 15px;
  }
  
  .form-item label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  .form-item input,
  .form-item textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box; /*  重要：防止 padding 撑大 input 宽度 */
  }
  
  .form-item textarea {
    min-height: 100px;
    font-family: sans-serif; /* 避免 textarea 默认等宽字体 */
  }
  
  .form-actions {
    margin-top: 20px;
    text-align: right;
  }
  
  .save-button,
  .cancel-button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .save-button {
    background-color: #28a745;
    color: white;
    margin-right: 10px;
  }
  
  .cancel-button {
    background-color: #dc3545;
    color: white;
  }
  
  .loading-indicator,
  .error-indicator {
    text-align: center;
    padding: 20px;
    color: #777;
  }
  </style>