<template>
  <div class="order-list">
    <el-table :data="orders" style="width: 100%">
      <el-table-column prop="id" label="订单号" width="180" />
      <el-table-column label="商品信息" min-width="300">
        <template #default="{ row }">
          <div v-for="item in row.items" :key="item.id" class="order-item">
            <img :src="item.product.image || '/default-product.png'" class="product-image">
            <div class="product-info">
              <div class="product-name">{{ item.product.name }}</div>
              <div class="product-price">¥{{ item.product.price }} × {{ item.quantity }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="total_amount" label="总金额" width="120">
        <template #default="{ row }">
          ¥{{ row.total_amount }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="order_date" label="下单时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.order_date) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="viewOrder(row)">查看详情</el-button>
          <!-- <el-button 
            v-if="row.status === 'pending'" 
            type="success" 
            size="small" 
            @click="payOrder(row)"
          >立即支付</el-button> -->
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { formatDate } from '@/utils/format'

const router = useRouter()

const props = defineProps({
  orders: {
    type: Array,
    required: true
  }
})

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    'pending': 'warning',
    'paid': 'primary',
    'shipped': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待发货',
    'paid': '已付款',
    'shipped': '已发货',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || '未知状态'
}

// 查看订单详情
const viewOrder = (order) => {
  router.push(`/orders/${order.id}`)
}

// 支付订单
const payOrder = (order) => {
  // TODO: 实现支付功能
  console.log('支付订单:', order)
}
</script>

<style scoped>
.order-list {
  padding: 20px;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.order-item:last-child {
  border-bottom: none;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  margin-right: 10px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  margin-bottom: 5px;
}

.product-price {
  color: #f56c6c;
  font-size: 12px;
}
</style> 