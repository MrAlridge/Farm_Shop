<template>
  <div class="shipping-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>发货管理</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="待发货" name="pending">
          <el-table :data="pendingOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="180" />
            <el-table-column prop="order_date" label="下单时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.order_date) }}
              </template>
            </el-table-column>
            <el-table-column label="商品信息">
              <template #default="{ row }">
                <div v-for="item in row.items" :key="item.id">
                  {{ item.product_name }} x {{ item.quantity }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="handleShip(row)"
                  :disabled="row.items.every(item => item.shipping_status === 'shipped')"
                >
                  发货
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="已发货" name="shipped">
          <el-table :data="shippedOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="180" />
            <el-table-column prop="order_date" label="下单时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.order_date) }}
              </template>
            </el-table-column>
            <el-table-column label="商品信息">
              <template #default="{ row }">
                <div v-for="item in row.items" :key="item.id">
                  {{ item.product_name }} x {{ item.quantity }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button 
                  type="info" 
                  size="small" 
                  @click="viewOrderDetail(row.id)"
                >
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPendingShippingOrders, shipOrderItem } from '@/api/order'
import { formatDate, formatPrice } from '@/utils/format'

const router = useRouter()
const activeTab = ref('pending')
const orders = ref([])

// 获取订单数据
const fetchOrders = async () => {
  try {
    const response = await getPendingShippingOrders()
    orders.value = response || []
    console.log(orders.value, response)
  } catch (error) {
    console.error('获取订单失败:', error)
    ElMessage.error('获取订单失败')
    orders.value = []
  }
}

// 根据状态筛选订单
const pendingOrders = computed(() => {
  if (!orders.value) return []
  return orders.value.filter(order => order.items.some(item => item.shipping_status === 'pending'))
})

const shippedOrders = computed(() => {
  if (!orders.value) return []
  return orders.value.filter(order => order.items.every(item => item.shipping_status === 'shipped'))
})

// 查看订单详情
const viewOrderDetail = (orderId) => {
  router.push(`/poor/order/${orderId}`)
}

// 处理发货
const handleShip = async (order) => {
  try {
    await ElMessageBox.confirm('确认发货该订单吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 发货每个订单项
    for (const item of order.items) {
      await shipOrderItem(item.id)
    }
    
    ElMessage.success('发货成功')
    fetchOrders() // 刷新订单列表
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('发货失败：' + (error.response?.data?.error || error.message))
    }
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.shipping-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 