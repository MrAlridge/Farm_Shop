import request from '@/utils/request'

// 获取商品详情
export function getProductDetail(id) {
  return request({
    url: `/products/products/${id}`,
    method: 'get'
  })
}

// 获取商品评价列表
export function getProductReviews(id) {
  return request({
    url: `/products/products/${id}/reviews`,
    method: 'get'
  })
}

// 提交商品评价
export function submitReview(productId, data) {
  return request({
    url: `/products/products/${productId}/reviews`,
    method: 'post',
    data
  })
}

// 获取商品列表
export function getProducts(params) {
  return request({
    url: '/products/products',
    method: 'get',
    params
  })
}

// 获取商品分类
export function getCategories() {
  return request({
    url: '/products/categories/list_categories',
    method: 'get'
  })
} 