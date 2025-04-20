<template>
  <div class="orders-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="全部订单" name="all">
        <order-list :orders="allOrders" />
      </el-tab-pane>
      <el-tab-pane label="待发货" name="pending">
        <order-list :orders="pendingOrders" />
      </el-tab-pane>
      <!-- <el-tab-pane label="待发货" name="paid">
        <order-list :orders="paidOrders" />
      </el-tab-pane> -->
      <el-tab-pane label="待收货" name="shipped">
        <order-list :orders="shippedOrders" />
      </el-tab-pane>
      <el-tab-pane label="已完成" name="completed">
        <order-list :orders="completedOrders" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import OrderList from '../components/OrderList.vue'
import { getOrders } from '@/api/order'

const activeTab = ref('all')
const orders = ref([])

// 获取订单数据
const fetchOrders = async () => {
  try {
    const response = await getOrders()
    if (response && response.results) {
      orders.value = response.results
    } else {
      console.error('获取订单数据失败：响应格式不正确')
      ElMessage.error('获取订单数据失败')
    }
  } catch (error) {
    console.error('获取订单数据失败:', error)
    ElMessage.error('获取订单数据失败：' + (error.message || '未知错误'))
  }
}

// 根据状态筛选订单
const allOrders = computed(() => orders.value)
const pendingOrders = computed(() => orders.value.filter(order => order.status === 'pending'))
// const paidOrders = computed(() => orders.value.filter(order => order.status === 'paid'))
const shippedOrders = computed(() => orders.value.filter(order => order.status === 'shipped'))
const completedOrders = computed(() => orders.value.filter(order => order.status === 'completed'))

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders-container {
  padding: 20px;
}
</style> 