import request from '@/utils/request'

// 获取订单列表
export function getOrders() {
  return request({
    url: '/orders/orders/',
    method: 'get'
  })
}

// 获取订单详情
export function getOrderDetail(id) {
  return request({
    url: `/orders/orders/${id}/`,
    method: 'get'
  })
}

// 创建订单
export function createOrder(data) {
  return request({
    url: '/orders/orders/',
    method: 'post',
    data
  })
}

// 支付订单
export function payOrder(id) {
  return request({
    url: `/orders/orders/${id}/pay/`,
    method: 'post'
  })
}

// 取消订单
export function cancelOrder(id) {
  return request({
    url: `/orders/orders/${id}/cancel/`,
    method: 'post'
  })
}

// 确认收货
export function confirmReceive(id) {
  return request({
    url: `/orders/orders/${id}/confirm/`,
    method: 'post'
  })
}

// 发货订单
export function shipOrder(id, data) {
  return request({
    url: `/orders/orders/${id}/ship/`,
    method: 'post',
    data
  })
}

// 获取贫困户待发货订单
export function getPendingShippingOrders() {
  return request({
    url: '/orders/orders/pending_shipping/',
    method: 'get'
  })
}

// 发货单个订单项
export function shipOrderItem(itemId) {
  return request({
    url: `/orders/order-items/${itemId}/ship/`,
    method: 'post'
  })
} 