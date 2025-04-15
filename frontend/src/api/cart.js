import request from '@/utils/request'

// 获取购物车
export const getCart = async () => {
  try {
    const response = await request.get('cart')
    return response
  } catch (error) {
    console.error('获取购物车失败:', error)
    throw error
  }
}

// 添加到购物车
export const addToCart = async (item) => {
  try {
    const response = await request.post('cart', item)
    return response
  } catch (error) {
    console.error('添加到购物车失败:', error)
    throw error
  }
}

// 更新购物车
export const updateCart = async (id, quantity) => {
  try {
    const response = await request.patch(`cart/${id}`, { quantity })
    return response
  } catch (error) {
    console.error('更新购物车失败:', error)
    throw error
  }
}

// 从购物车移除
export const removeFromCart = async (id) => {
  try {
    const response = await request.delete(`cart/${id}`)
    return response
  } catch (error) {
    console.error('从购物车移除失败:', error)
    throw error
  }
}

// 清空购物车
export const clearCart = async () => {
  try {
    const response = await request.delete('cart')
    return response
  } catch (error) {
    console.error('清空购物车失败:', error)
    throw error
  }
}

// 结算购物车
export const checkoutCart = async (items) => {
  try {
    const response = await request.post('cart/checkout', { items })
    return response
  } catch (error) {
    console.error('结算购物车失败:', error)
    throw error
  }
} 