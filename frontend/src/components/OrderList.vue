<template>
  <div class="order-list">
    <el-card v-for="order in orders" :key="order.id" class="order-card">
      <template #header>
        <div class="order-header">
          <span class="order-id">订单号：{{ order.id }}</span>
          <span class="order-time">{{ order.createTime }}</span>
          <el-tag :type="getStatusType(order.status)">
            {{ getStatusText(order.status) }}
          </el-tag>
        </div>
      </template>
      
      <div class="order-items">
        <div v-for="item in order.items" :key="item.id" class="order-item">
          <img :src="item.image" class="item-image">
          <div class="item-info">
            <h4>{{ item.name }}</h4>
            <p class="price">¥{{ item.price }}</p>
            <p class="quantity">x{{ item.quantity }}</p>
          </div>
        </div>
      </div>
      
      <div class="order-footer">
        <div class="total-amount">
          总计：<span class="price">¥{{ order.totalAmount.toFixed(2) }}</span>
        </div>
        <div class="actions">
          <el-button
            v-if="order.status === 'unpaid'"
            type="primary"
            @click="payOrder(order)">
            立即付款
          </el-button>
          <el-button
            v-if="order.status === 'shipped'"
            type="success"
            @click="confirmReceive(order)">
            确认收货
          </el-button>
          <el-button
            v-if="order.status === 'completed'"
            @click="viewOrder(order)">
            查看详情
          </el-button>
          <el-button
            v-if="order.status === 'unpaid'"
            type="danger"
            @click="cancelOrder(order)">
            取消订单
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps({
  orders: {
    type: Array,
    required: true
  }
})

const getStatusType = (status) => {
  const types = {
    unpaid: 'warning',
    unshipped: 'info',
    shipped: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    unpaid: '待付款',
    unshipped: '待发货',
    shipped: '待收货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const payOrder = (order) => {
  // TODO: 实现支付逻辑
  ElMessage.success('支付成功')
}

const confirmReceive = (order) => {
  ElMessageBox.confirm(
    '确认已收到商品？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现确认收货逻辑
    ElMessage.success('确认收货成功')
  })
}

const viewOrder = (order) => {
  // TODO: 实现查看订单详情逻辑
  console.log('查看订单:', order)
}

const cancelOrder = (order) => {
  ElMessageBox.confirm(
    '确定要取消该订单吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现取消订单逻辑
    ElMessage.success('订单已取消')
  })
}
</script>

<style scoped>
.order-list {
  padding: 20px 0;
}

.order-card {
  margin-bottom: 20px;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-id {
  font-weight: bold;
}

.order-time {
  color: #909399;
}

.order-items {
  padding: 20px 0;
}

.order-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-right: 20px;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  margin: 0 0 10px 0;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.quantity {
  color: #909399;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
}

.total-amount {
  font-size: 16px;
}

.actions {
  display: flex;
  gap: 10px;
}
</style> 