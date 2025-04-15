<template>
  <div class="cart-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的购物车</span>
          <el-button type="danger" @click="clearCart" :disabled="!cartItems.length">
            清空购物车
          </el-button>
        </div>
      </template>
      
      <el-table
        :data="cartItems"
        style="width: 100%"
        @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column label="商品图片" width="120">
          <template #default="{ row }">
            <img :src="row.image" class="product-image">
          </template>
        </el-table-column>
        <el-table-column label="商品名称" prop="name" />
        <el-table-column label="单价" width="120">
          <template #default="{ row }">
            ¥{{ row.price }}
          </template>
        </el-table-column>
        <el-table-column label="数量" width="150">
          <template #default="{ row }">
            <el-input-number
              v-model="row.quantity"
              :min="1"
              :max="row.stock"
              size="small"
              @change="updateQuantity(row)" />
          </template>
        </el-table-column>
        <el-table-column label="小计" width="120">
          <template #default="{ row }">
            ¥{{ (row.price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button
              type="danger"
              size="small"
              @click="removeItem(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="cart-footer">
        <div class="total">
          总计：<span class="price">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
        <el-button
          type="primary"
          size="large"
          @click="checkout"
          :disabled="!selectedItems.length">
          结算 ({{ selectedItems.length }})
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCart, updateCart, checkoutCart } from '@/api/cart'

const router = useRouter()

const cartItems = ref([])

const selectedItems = ref([])

// 计算总价
const totalPrice = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    return total + item.price * item.quantity
  }, 0)
})

const handleSelectionChange = (selection) => {
  selectedItems.value = selection
}

const updateQuantity = async (item) => {
  try {
    await updateCart(item.id, { quantity: item.quantity })
    ElMessage.success('数量更新成功')
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败')
  }
}

const removeItem = (item) => {
  ElMessageBox.confirm(
    '确定要从购物车中删除该商品吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = cartItems.value.findIndex(i => i.id === item.id)
    if (index !== -1) {
      cartItems.value.splice(index, 1)
      ElMessage.success('删除成功')
    }
  })
}

const clearCart = () => {
  ElMessageBox.confirm(
    '确定要清空购物车吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    cartItems.value = []
    ElMessage.success('购物车已清空')
  })
}

const checkout = async () => {
  try {
    await checkoutCart(selectedItems.value)
    ElMessage.success('结算成功')
    router.push('/orders/checkout')
  } catch (error) {
    console.error('结算失败:', error)
    ElMessage.error('结算失败')
  }
}

onMounted(async () => {
  try {
    const response = await getCart()
    cartItems.value = response.data
  } catch (error) {
    console.error('获取购物车失败:', error)
  }
})
</script>

<style scoped>
.cart-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.cart-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.total {
  margin-right: 20px;
  font-size: 16px;
}

.price {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
}
</style> 