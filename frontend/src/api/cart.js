import request from '@/utils/request'

// 获取购物车数据
export function getCartItems() {
  const cartItems = localStorage.getItem('cartItems')
  return Promise.resolve({
    data: cartItems ? JSON.parse(cartItems) : []
  })
}

// 添加商品到购物车
export function addToCart(productId, quantity) {
  return getCartItems().then(response => {
    const cartItems = response.data
    const existingItem = cartItems.find(item => item.product.id === productId)
    
    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      cartItems.push({
        id: Date.now(), // 使用时间戳作为临时ID
        product: {
          id: productId,
          name: '', // 这些字段会在添加到购物车时更新
          price: 0,
          image: '',
          stock: 0
        },
        quantity: quantity
      })
    }
    
    localStorage.setItem('cartItems', JSON.stringify(cartItems))
    return Promise.resolve({ data: cartItems })
  })
}

// 更新购物车商品数量
export function updateCartItem(itemId, quantity) {
  return getCartItems().then(response => {
    const cartItems = response.data
    const item = cartItems.find(item => item.id === itemId)
    
    if (item) {
      item.quantity = quantity
      localStorage.setItem('cartItems', JSON.stringify(cartItems))
    }
    
    return Promise.resolve({ data: cartItems })
  })
}

// 从购物车删除商品
export function removeCartItem(itemId) {
  return getCartItems().then(response => {
    const cartItems = response.data.filter(item => item.id !== itemId)
    localStorage.setItem('cartItems', JSON.stringify(cartItems))
    return Promise.resolve({ data: cartItems })
  })
}

// 清空购物车
export function clearCart() {
  localStorage.removeItem('cartItems')
  return Promise.resolve({ data: [] })
}

// 创建订单
export function createOrder(data) {
  return request({
    url: 'orders/orders/',
    method: 'post',
    data
  })
}

// 取消订单
export function cancelOrder(orderId) {
  return request({
    url: `orders/orders/${orderId}/cancel/`,
    method: 'post'
  })
} 