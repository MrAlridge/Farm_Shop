<template>
  <div class="cart-container">
    <div class="background-element"></div>
    <el-card class="cart-card">
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
            <img :src="row.product.image || '/default-product.png'" class="product-image">
          </template>
        </el-table-column>
        <el-table-column label="商品名称" prop="product.name" />
        <el-table-column label="单价" width="120">
          <template #default="{ row }">
            ¥{{ row.product.price }}
          </template>
        </el-table-column>
        <el-table-column label="数量" width="150">
          <template #default="{ row }">
            <el-input-number
              v-model="row.quantity"
              :min="1"
              :max="row.product.stock"
              size="small"
              @change="(value) => updateQuantity(row, value)" />
          </template>
        </el-table-column>
        <el-table-column label="小计" width="120">
          <template #default="{ row }">
            ¥{{ (row.product.price * row.quantity).toFixed(2) }}
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

    <!-- 结算表单对话框 -->
    <el-dialog
      v-model="checkoutDialogVisible"
      title="填写订单信息"
      width="500px"
    >
      <el-form
        :model="checkoutForm"
        :rules="checkoutRules"
        ref="checkoutFormRef"
        label-width="100px"
      >
        <el-form-item label="收货人" prop="receiver_name">
          <el-input v-model="checkoutForm.receiver_name" placeholder="请输入收货人姓名" />
        </el-form-item>
        
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="checkoutForm.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        
        <el-form-item label="收货地址" prop="shipping_address">
          <el-input
            v-model="checkoutForm.shipping_address"
            type="textarea"
            :rows="3"
            placeholder="请输入详细收货地址"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="checkoutDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCheckout">
            提交订单
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCartItems, updateCartItem, removeCartItem, clearCart, createOrder } from '@/api/cart'

const router = useRouter()
const cartItems = ref([])
const selectedItems = ref([])
const checkoutDialogVisible = ref(false)
const checkoutFormRef = ref(null)

const checkoutForm = ref({
  receiver_name: '',
  contact_phone: '',
  shipping_address: ''
})

const checkoutRules = {
  receiver_name: [
    { required: true, message: '请输入收货人姓名', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  shipping_address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' },
    { min: 5, message: '地址不能少于5个字符', trigger: 'blur' }
  ]
}

// 计算总价
const totalPrice = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    return total + item.product.price * item.quantity
  }, 0)
})

// 获取购物车数据
const fetchCartItems = async () => {
  try {
    const response = await getCartItems()
    cartItems.value = response.data
  } catch (error) {
    console.error('获取购物车数据失败:', error)
    ElMessage.error('获取购物车数据失败')
  }
}

const handleSelectionChange = (selection) => {
  selectedItems.value = selection
}

// 更新商品数量
const updateQuantity = async (item, newQuantity) => {
  try {
    await updateCartItem(item.id, newQuantity)
    ElMessage.success('更新成功')
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败')
    // 恢复原来的数量
    item.quantity = item.quantity
  }
}

// 删除商品
const removeItem = async (item) => {
  try {
    await ElMessageBox.confirm(
      '确定要从购物车中删除该商品吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await removeCartItem(item.id)
    ElMessage.success('删除成功')
    await fetchCartItems()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 清空购物车
const clearCartItems = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空购物车吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await clearCart()
    cartItems.value = []
    selectedItems.value = []
    ElMessage.success('购物车已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空购物车失败:', error)
      ElMessage.error('清空购物车失败')
    }
  }
}

// 显示结算对话框
const showCheckoutDialog = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请选择要购买的商品')
    return
  }
  checkoutDialogVisible.value = true
}

// 提交订单
const submitCheckout = async () => {
  if (!checkoutFormRef.value) return
  
  await checkoutFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 准备订单数据
        const orderData = {
          items: selectedItems.value.map(item => ({
            product_id: item.product.id,
            quantity: item.quantity
          })),
          shipping_address: checkoutForm.value.shipping_address,
          contact_phone: checkoutForm.value.contact_phone,
          receiver_name: checkoutForm.value.receiver_name
        }
        
        // 创建订单
        const response = await createOrder(orderData)
        
        if (response && response.id) {
          // 清空整个购物车
          await clearCart()
          cartItems.value = []
          selectedItems.value = []
          
          // 重置表单
          checkoutForm.value = {
            receiver_name: '',
            contact_phone: '',
            shipping_address: ''
          }
          checkoutDialogVisible.value = false
          
          ElMessage.success({
            message: '订单创建成功，正在跳转到首页...',
            duration: 2000
          })
          
          // 延迟2秒后跳转到首页
          setTimeout(() => {
            router.push('/')
          }, 2000)
        } else {
          throw new Error('订单创建失败：响应数据格式错误')
        }
      } catch (error) {
        console.error('创建订单失败:', error)
        ElMessage.error('创建订单失败：' + (error.message || '未知错误'))
      }
    }
  })
}

// 结算按钮点击事件
const checkout = () => {
  showCheckoutDialog()
}

onMounted(() => {
  fetchCartItems()
})
</script>

<style scoped>
.cart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  background-color: #f5f5f5;
}

.background-element {
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  background-color: #e0e0e0;
  z-index: -1;
}

.cart-card {
  width: 80%;
  max-width: 800px;
  margin: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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