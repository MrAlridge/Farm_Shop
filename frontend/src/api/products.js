import request from '@/utils/request'

// 获取商品列表
export const getProducts = async (params = {}) => {
  try {
    const response = await request({url:'products/products',method:'get',params})
    return response
  } catch (error) {
    console.error('获取商品列表失败:', error)
    throw error
  }
}

// 获取商品详情
export const getProductDetail = async (id) => {
  try {
    const response = await request({url:`products/products/${id}`,method:'get'})
    return response
  } catch (error) {
    console.error('获取商品详情失败:', error)
    throw error
  }
}

// 获取商品分类
export const getCategories = async () => {
  try {
    const response = await request({url:'products/categories/list_categories',method:'get'})
    return response
  } catch (error) {
    console.error('获取商品分类失败:', error)
    throw error
  }
}

// 搜索商品
export const searchProducts = async (keyword) => {
  try {
    const response = await request({url:'products/products',method:'get',params:{search:keyword}})
    return response
  } catch (error) {
    console.error('搜索商品失败:', error)
    throw error
  }
} 