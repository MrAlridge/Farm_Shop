import { getProducts, getProductDetail, searchProducts } from '@/api/products'

const state = {
  products: [],
  productDetail: null,
  searchResults: [],
  loading: false,
  error: null
}

const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_PRODUCT_DETAIL(state, product) {
    state.productDetail = product
  },
  SET_SEARCH_RESULTS(state, results) {
    state.searchResults = results
  },
  SET_LOADING(state, status) {
    state.loading = status
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  // 获取商品列表
  async getProducts({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const { data } = await getProducts(params)
      commit('SET_PRODUCTS', data)
      return data
    } catch (error) {
      commit('SET_ERROR', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取商品详情
  async getProductDetail({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const { data } = await getProductDetail(id)
      commit('SET_PRODUCT_DETAIL', data)
      return data
    } catch (error) {
      commit('SET_ERROR', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 搜索商品
  async searchProducts({ commit }, keyword) {
    commit('SET_LOADING', true)
    try {
      const { data } = await searchProducts(keyword)
      commit('SET_SEARCH_RESULTS', data)
      return data
    } catch (error) {
      commit('SET_ERROR', error)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  products: state => state.products,
  productDetail: state => state.productDetail,
  searchResults: state => state.searchResults,
  loading: state => state.loading,
  error: state => state.error
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 