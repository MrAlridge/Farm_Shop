import { createStore } from 'vuex'
import user from './modules/user'
import cart from './modules/cart'
import products from './modules/products'

export default createStore({
  state: {
    loading: false,
    loadingText: '',
    error: null
  },
  mutations: {
    SET_LOADING(state, { status, text = '' }) {
      state.loading = status
      state.loadingText = text
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    showLoading({ commit }, text = '') {
      commit('SET_LOADING', { status: true, text })
    },
    hideLoading({ commit }) {
      commit('SET_LOADING', { status: false })
    },
    showError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('SET_ERROR', null)
    }
  },
  modules: {
    user,
    cart,
    products
  }
}) 