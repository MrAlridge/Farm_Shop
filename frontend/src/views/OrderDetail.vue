<template>
  <div class="order-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单详情</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ order.id }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ formatDate(order.order_date) }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="订单总额">
          <span class="total-price">{{ formatPrice(order.total_amount) }}</span>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h3>收货信息</h3>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="收货人">{{ order.receiver_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ order.contact_phone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">{{ order.shipping_address }}</el-descriptions-item>
      </el-descriptions>

      <el-divider />

      <h3>商品信息</h3>
      <el-table :data="order.items" border>
        <el-table-column prop="product.name" label="商品名称" />
        <el-table-column prop="quantity" label="数量" width="100" />
        <el-table-column prop="product.price" label="单价" width="120">
          <template #default="{ row }">
            {{ formatPrice(row.product.price) }}
          </template>
        </el-table-column>
        <el-table-column label="小计" width="120">
          <template #default="{ row }">
            {{ formatPrice(row.subtotal) }}
          </template>
        </el-table-column>
      </el-table>

      <div class="order-actions" v-if="order.status === 'pending'">
        <!-- <el-button type="primary" @click="handlePay">立即支付</el-button> -->
        <el-button @click="handleCancel">取消订单</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getOrderDetail, payOrder, cancelOrder } from '@/api/order'
import { formatDate, formatPrice } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const order = ref({})

const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    paid: 'success',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'info'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '待发货',
    paid: '已发货',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const fetchOrderDetail = async () => {
  try {
    const response = await getOrderDetail(route.params.id)
    order.value = response
  } catch (error) {
    ElMessage.error('获取订单详情失败')
  }
}

const handlePay = async () => {
  try {
    await payOrder(order.value.id)
    ElMessage.success('支付成功')
    fetchOrderDetail()
  } catch (error) {
    ElMessage.error('支付失败')
  }
}

const handleCancel = () => {
  ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cancelOrder(order.value.id)
      ElMessage.success('订单已取消')
      fetchOrderDetail()
    } catch (error) {
      ElMessage.error('取消订单失败')
    }
  })
}

onMounted(() => {
  fetchOrderDetail()
})
</script>

<style scoped>
.order-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-price {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
}

.order-actions {
  margin-top: 20px;
  text-align: right;
}
</style> 