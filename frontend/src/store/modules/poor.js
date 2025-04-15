import { defineStore } from 'pinia'
import { 
  registerPoor, 
  loginPoor, 
  getPoorInfo, 
  submitApplication,
  getApplicationStatus,
  getAssistanceProjects,
  applyForProject,
  getMaterialAssistance,
  applyForMaterial,
  getEducationAssistance,
  applyForEducation
} from '@/api/poor'

export const usePoorStore = defineStore('poor', {
  state: () => ({
    token: localStorage.getItem('poor-token') || '',
    userInfo: null,
    isLoggedIn: false,
    applicationStatus: null,
    assistanceProjects: [],
    materialAssistance: [],
    educationAssistance: []
  }),

  getters: {
    username: (state) => state.userInfo?.username || '',
    status: (state) => state.userInfo?.status || '',
    approvedProjects: (state) => state.assistanceProjects.filter(project => project.status === 'approved'),
    availableMaterials: (state) => state.materialAssistance.filter(material => material.status === 'available'),
    availableEducation: (state) => state.educationAssistance.filter(edu => edu.status === 'available')
  },

  actions: {
    async register(userData) {
      try {
        const response = await registerPoor(userData)
        return response
      } catch (error) {
        console.error('注册失败:', error)
        throw error
      }
    },

    async login(credentials) {
      try {
        const response = await loginPoor(credentials)
        this.token = response.data.token
        this.userInfo = response.data.userInfo
        this.isLoggedIn = true
        localStorage.setItem('poor-token', this.token)
        return response
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },

    async getUserInfo() {
      try {
        const response = await getPoorInfo(this.userInfo?.id)
        this.userInfo = response.data
        return response
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },

    async submitApplication(applicationData) {
      try {
        const response = await submitApplication(applicationData)
        return response
      } catch (error) {
        console.error('提交申请失败:', error)
        throw error
      }
    },

    async getApplicationStatus() {
      try {
        const response = await getApplicationStatus(this.userInfo?.id)
        this.applicationStatus = response.data
        return response
      } catch (error) {
        console.error('获取申请状态失败:', error)
        throw error
      }
    },

    async fetchAssistanceProjects() {
      try {
        const response = await getAssistanceProjects()
        this.assistanceProjects = response.data
        return response
      } catch (error) {
        console.error('获取帮扶项目失败:', error)
        throw error
      }
    },

    async applyForProject(projectId) {
      try {
        const response = await applyForProject(projectId)
        return response
      } catch (error) {
        console.error('申请帮扶项目失败:', error)
        throw error
      }
    },

    async fetchMaterialAssistance() {
      try {
        const response = await getMaterialAssistance()
        this.materialAssistance = response.data
        return response
      } catch (error) {
        console.error('获取物资援助失败:', error)
        throw error
      }
    },

    async applyForMaterial(materialId) {
      try {
        const response = await applyForMaterial(materialId)
        return response
      } catch (error) {
        console.error('申请物资援助失败:', error)
        throw error
      }
    },

    async fetchEducationAssistance() {
      try {
        const response = await getEducationAssistance()
        this.educationAssistance = response.data
        return response
      } catch (error) {
        console.error('获取教育资助失败:', error)
        throw error
      }
    },

    async applyForEducation(assistanceId) {
      try {
        const response = await applyForEducation(assistanceId)
        return response
      } catch (error) {
        console.error('申请教育资助失败:', error)
        throw error
      }
    },

    logout() {
      this.token = ''
      this.userInfo = null
      this.isLoggedIn = false
      localStorage.removeItem('poor-token')
    }
  }
}) 