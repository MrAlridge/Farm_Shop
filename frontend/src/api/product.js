import request from '@/utils/request'

// 获取商品详情
export function getProductDetail(id) {
  return request({
    url: `products/products/${id}/`,
    method: 'get'
  })
}

// 获取商品评价
export function getProductReviews(id) {
  return request({
    url: `products/products/${id}/reviews/`,
    method: 'get'
  })
}

// 提交评价
export function submitReview(productId, data) {
  return request({
    url: `products/products/${productId}/reviews/`,
    method: 'post',
    data
  })
}

// 获取商品列表
export function getProducts(params) {
  return request({
    url: 'products/products/',
    method: 'get',
    params
  })
}

// 获取分类列表
export function getCategories() {
  return request({
    url: '/products/categories/list_categories/',
    method: 'get'
  })
}

// 创建商品
export function createProduct(data) {
  return request({
    url: 'products/products/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

// 上传商品图片
export function uploadProductImage(file) {
  const formData = new FormData()
  formData.append('image', file)
  
  return request({
    url: 'products/products/upload_image/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 