<template>
  <div class="orders-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="全部订单" name="all">
        <order-list :orders="allOrders" />
      </el-tab-pane>
      <el-tab-pane label="待付款" name="unpaid">
        <order-list :orders="unpaidOrders" />
      </el-tab-pane>
      <el-tab-pane label="待发货" name="unshipped">
        <order-list :orders="unshippedOrders" />
      </el-tab-pane>
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
import { ref, computed } from 'vue'
import OrderList from '../components/OrderList.vue'

const activeTab = ref('all')

// 模拟订单数据
const orders = ref([
  {
    id: '202404010001',
    status: 'unpaid',
    createTime: '2024-04-01 10:00:00',
    totalAmount: 109.7,
    items: [
      {
        id: 1,
        name: '有机大米',
        price: 39.9,
        quantity: 2,
        image: '/product1.jpg'
      },
      {
        id: 2,
        name: '土鸡蛋',
        price: 29.9,
        quantity: 1,
        image: '/product2.jpg'
      }
    ]
  },
  {
    id: '202403280001',
    status: 'completed',
    createTime: '2024-03-28 15:30:00',
    totalAmount: 49.9,
    items: [
      {
        id: 3,
        name: '山核桃',
        price: 49.9,
        quantity: 1,
        image: '/product3.jpg'
      }
    ]
  }
])

// 根据状态筛选订单
const allOrders = computed(() => orders.value)
const unpaidOrders = computed(() => orders.value.filter(order => order.status === 'unpaid'))
const unshippedOrders = computed(() => orders.value.filter(order => order.status === 'unshipped'))
const shippedOrders = computed(() => orders.value.filter(order => order.status === 'shipped'))
const completedOrders = computed(() => orders.value.filter(order => order.status === 'completed'))
</script>

<style scoped>
.orders-container {
  padding: 20px;
}
</style> 