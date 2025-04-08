// 模拟获取商品列表
export const getProducts = async (params = {}) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '有机大米',
            price: 39.9,
            image: '/images/products/product1.jpg',
            description: '优质有机大米，产自贫困山区',
            stock: 100,
            sales: 50,
            category: '粮食'
          },
          {
            id: 2,
            name: '土鸡蛋',
            price: 15.8,
            image: '/images/products/product2.jpg',
            description: '散养土鸡蛋，营养丰富',
            stock: 200,
            sales: 80,
            category: '禽蛋'
          },
          {
            id: 3,
            name: '山核桃',
            price: 29.9,
            image: '/images/products/product3.jpg',
            description: '野生山核桃，口感香脆',
            stock: 150,
            sales: 30,
            category: '坚果'
          }
        ]
      })
    }, 1000)
  })
}

// 模拟获取商品详情
export const getProductDetail = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const products = {
        1: {
          id: 1,
          name: '有机大米',
          price: 39.9,
          images: [
            '/images/products/product1.jpg',
            '/images/products/product1_1.jpg',
            '/images/products/product1_2.jpg'
          ],
          description: '优质有机大米，产自贫困山区',
          detail: '采用传统种植方式，无农药化肥，口感香糯',
          stock: 100,
          sales: 50,
          category: '粮食',
          reviews: [
            {
              id: 1,
              user: '张三',
              rating: 5,
              content: '米质很好，煮出来的饭很香',
              time: '2024-03-15'
            }
          ]
        }
      }
      resolve({
        data: products[id] || null
      })
    }, 1000)
  })
}

// 模拟获取商品分类
export const getCategories = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          { id: 1, name: '粮食' },
          { id: 2, name: '禽蛋' },
          { id: 3, name: '坚果' },
          { id: 4, name: '水果' },
          { id: 5, name: '蔬菜' }
        ]
      })
    }, 1000)
  })
}

// 模拟搜索商品
export const searchProducts = async (keyword) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '有机大米',
            price: 39.9,
            image: '/images/products/product1.jpg',
            description: '优质有机大米，产自贫困山区'
          }
        ]
      })
    }, 1000)
  })
} 