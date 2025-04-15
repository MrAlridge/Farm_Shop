// 模拟获取购物车
export const getCart = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '有机大米',
            price: 39.9,
            image: '/images/products/product1.jpg',
            quantity: 2,
            selected: true
          },
          {
            id: 2,
            name: '土鸡蛋',
            price: 15.8,
            image: '/images/products/product2.jpg',
            quantity: 1,
            selected: true
          }
        ]
      })
    }, 1000)
  })
}

// 模拟添加到购物车
export const addToCart = async (item) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '添加成功',
          item
        }
      })
    }, 1000)
  })
}

// 模拟更新购物车
export const updateCart = async (id, quantity) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '更新成功',
          id,
          quantity
        }
      })
    }, 1000)
  })
}

// 模拟从购物车移除
export const removeFromCart = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '移除成功',
          id
        }
      })
    }, 1000)
  })
}

// 模拟清空购物车
export const clearCart = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '清空成功'
        }
      })
    }, 1000)
  })
} 