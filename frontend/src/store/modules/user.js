import { defineStore } from 'pinia'
import { login, register, getUserInfo, updateUserInfo } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
    isLoggedIn: false
  }),

  getters: {
    username: (state) => state.userInfo?.username || '',
    avatar: (state) => state.userInfo?.avatar || '',
    userId: (state) => state.userInfo?.id || null
  },

  actions: {
    async login(credentials) {
      try {
        const response = await login(credentials)
        this.token = response.data.token
        this.isLoggedIn = true
        localStorage.setItem('token', this.token)
        await this.getUserInfo()
        return response
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },

    async register(userData) {
      try {
        const response = await register(userData)
        return response
      } catch (error) {
        console.error('注册失败:', error)
        throw error
      }
    },

    async getUserInfo() {
      try {
        const response = await getUserInfo()
        this.userInfo = response.data
        this.isLoggedIn = true
        return response
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.logout()
        throw error
      }
    },

    async updateUserInfo(userData) {
      try {
        const response = await updateUserInfo(userData)
        this.userInfo = { ...this.userInfo, ...userData }
        return response
      } catch (error) {
        console.error('更新用户信息失败:', error)
        throw error
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      this.isLoggedIn = false
      localStorage.removeItem('token')
    }
  }
}) 