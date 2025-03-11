<template>
    <div class="product-create-container">
      <h2>创建新产品</h2>
  
      <div v-if="loading" class="loading-indicator">
        加载中...
      </div>
      <div v-if="error" class="error-indicator">
        创建产品失败: {{ error.message }}
      </div>
  
      <form v-if="!loading && !error" @submit.prevent="createProduct">
        <div class="form-item">
          <label for="product_name">产品名称:</label>
          <input type="text" id="product_name" v-model="product.product_name">
        </div>
        <div class="form-item">
          <label for="product_description">产品描述:</label>
          <textarea id="product_description" v-model="product.product_description"></textarea>
        </div>
        <div class="form-item">
          <label for="product_category">产品分类:</label>
          <input type="text" id="product_category" v-model="product.product_category" placeholder="请填写产品分类，例如：水果、蔬菜、肉类">
        </div>
        <div class="form-item">
          <label for="product_price">价格:</label>
          <input type="number" id="product_price" v-model.number="product.product_price">
        </div>
        <div class="form-item">
          <label for="product_stock">库存:</label>
          <input type="number" id="product_stock" v-model.number="product.product_stock">
        </div>
        <div class="form-item">
          <label for="product_image">图片 URL (可选):</label>
          <input type="text" id="product_image" v-model="product.product_image">
        </div>
        <div class="form-item">
          <label for="poor_household">是否为贫困户产品:</label>
          <input type="checkbox" id="poor_household" v-model="product.poor_household">
        </div>
  
        <div class="form-actions">
          <button type="submit" class="create-button">创建</button>
          <button type="button" class="cancel-button" @click="cancelCreate">取消</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'ProductCreate',
    setup() {
      const product = ref({ // 修改 product 数据对象的属性名
        product_name: '',
        product_image: null, //  保持 null 或使用空字符串，后端处理 null
        product_description: '',
        product_price: null,
        product_stock: null,
        poor_household: false, //  默认为 false
      });
      const loading = ref(false);
      const error = ref(null);
      const router = useRouter();
  
      const createProduct = async () => {
        loading.value = true;
        error.value = null;
        try {
          const payload = { ...product.value }; //  创建 payload 对象
  
          //  处理 product_image，如果为空字符串，设置为 null (可选，后端可能已经处理)
          if (!payload.product_image) {
            payload.product_image = null;
          }
          //  确保 poor_household 是布尔值或 null (如果后端期望 null，则根据需要调整)
          if (payload.poor_household === null || payload.poor_household === undefined) {
            payload.poor_household = null; //  如果后端期望 null，可以设置为 null
          } else {
            payload.poor_household = Boolean(payload.poor_household); // 确保是布尔值
          }
  
  
          const response = await fetch('http://127.0.0.1:8000/api/products/', { //  确保 API 地址正确，末尾添加斜杠
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload), //  发送 payload 作为请求体
          });
          if (!response.ok) {
            return response.json().then(errorData => {
              throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            });
          }
          //  创建成功，跳转回产品列表页
          router.push('/products');
        } catch (e) {
          error.value = e;
          console.error("Failed to create product:", e);
        } finally {
          loading.value = false;
        }
      };
  
      const cancelCreate = () => {
        router.push('/products');
      };
  
      return {
        product,
        loading,
        error,
        createProduct,
        cancelCreate,
      };
    },
  };
  </script>
  
  <style scoped>
  /* 样式保持不变 */
  .product-create-container {
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
    box-sizing: border-box;
  }
  
  .form-item textarea {
    min-height: 100px;
    font-family: sans-serif;
  }
  
  .form-actions {
    margin-top: 20px;
    text-align: right;
  }
  
  .create-button,
  .cancel-button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
  }
  
  .create-button {
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