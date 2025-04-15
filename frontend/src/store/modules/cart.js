import { defineStore } from 'pinia'
import { getCart, addToCart, updateCart, removeFromCart, clearCart } from '@/api/cart'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cartItems')) || [],
    count: 0
  }),

  getters: {
    totalItems: (state) => state.count,
    totalPrice: (state) => {
      return state.items.reduce((total, item) => {
        return total + (item.price * item.quantity)
      }, 0)
    }
  },

  actions: {
    async fetchCart() {
      try {
        const response = await getCart()
        this.items = response.data
        this.count = this.items.reduce((total, item) => total + item.quantity, 0)
        localStorage.setItem('cartItems', JSON.stringify(this.items))
        return response
      } catch (error) {
        console.error('获取购物车失败:', error)
        throw error
      }
    },

    async addItem(item) {
      try {
        const response = await addToCart(item)
        const existingItem = this.items.find(i => i.id === item.id)
        if (existingItem) {
          existingItem.quantity += item.quantity
        } else {
          this.items.push(item)
        }
        this.count = this.items.reduce((total, item) => total + item.quantity, 0)
        localStorage.setItem('cartItems', JSON.stringify(this.items))
        return response
      } catch (error) {
        console.error('添加商品失败:', error)
        throw error
      }
    },

    async updateItemQuantity(id, quantity) {
      try {
        const response = await updateCart(id, quantity)
        const item = this.items.find(i => i.id === id)
        if (item) {
          item.quantity = quantity
          this.count = this.items.reduce((total, item) => total + item.quantity, 0)
          localStorage.setItem('cartItems', JSON.stringify(this.items))
        }
        return response
      } catch (error) {
        console.error('更新商品数量失败:', error)
        throw error
      }
    },

    async removeItem(id) {
      try {
        const response = await removeFromCart(id)
        this.items = this.items.filter(item => item.id !== id)
        this.count = this.items.reduce((total, item) => total + item.quantity, 0)
        localStorage.setItem('cartItems', JSON.stringify(this.items))
        return response
      } catch (error) {
        console.error('删除商品失败:', error)
        throw error
      }
    },

    async clearCart() {
      try {
        const response = await clearCart()
        this.items = []
        this.count = 0
        localStorage.removeItem('cartItems')
        return response
      } catch (error) {
        console.error('清空购物车失败:', error)
        throw error
      }
    }
  }
}) 