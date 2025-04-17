import { defineStore } from 'pinia'
import * as userApi from '@/api/user'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 假设 api/user.js 导出了一个 getMe 函数用于请求 /users/me/
// 并且 login 函数返回的数据包含 userInfo (含 userType) 或需要调用 getMe 获取

export const useUserStore = defineStore('user', {
  // 从 localStorage 初始化 state
  state: () => ({
    token: localStorage.getItem('userToken') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
    userInfo: (() => {
      try {
        return JSON.parse(localStorage.getItem('userInfo')) || {}
      } catch (e) {
        console.error("无法解析 localStorage 中的 userInfo:", e)
        localStorage.removeItem('userInfo')
        return {}
      }
    })(),
    isLoggedIn: !!localStorage.getItem('userToken'),
    // 贫困户专属字段
    applicationStatus: null,
    assistanceProjects: [],
    materialAssistance: [],
    educationAssistance: []
  }),

  getters: {
    username: (state) => state.userInfo?.username,
    avatar: (state) => state.userInfo?.avatar || '',
    userId: (state) => state.userInfo?.id,
    userType: (state) => state.userInfo?.user_type,
    isPoorUser: (state) => state.userInfo?.user_type === 'poor',
    isSocialUser: (state) => state.userInfo?.user_type === 'social',
    isAdminUser: (state) => state.userInfo?.is_staff === true,
    status: (state) => state.userInfo?.status || '',
    approvedProjects: (state) => state.assistanceProjects.filter(project => project.status === 'approved'),
    availableMaterials: (state) => state.materialAssistance.filter(material => material.status === 'available'),
    availableEducation: (state) => state.educationAssistance.filter(edu => edu.status === 'available'),
    phoneNumber: (state) => state.userInfo?.phone_number,
  },

  actions: {
    // 设置 Token 并存入 localStorage
    setTokens(accessToken, refreshToken) {
      this.token = accessToken
      this.refreshToken = refreshToken
      if (accessToken) {
        localStorage.setItem('userToken', accessToken)
      } else {
        localStorage.removeItem('userToken')
      }
      if (refreshToken) {
        localStorage.setItem('refreshToken', refreshToken)
      } else {
        localStorage.removeItem('refreshToken')
      }
    },

    // 设置用户信息并存入 localStorage
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      if (userInfo) {
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
        this.isLoggedIn = true
      } else {
        localStorage.removeItem('userInfo')
        this.isLoggedIn = false
      }
    },

    // 登录方法
    async login(credentials) {
      try {
        const response = await userApi.login(credentials)
        
        if (response.access && response.refresh) {
          this.setTokens(response.access, response.refresh)
          this.setUserInfo(response.user)
          
          ElMessage.success('登录成功')
          
          // 根据用户类型跳转到不同的首页
          if (this.isAdminUser) {
            router.push('/admin/dashboard')
          } else if (this.isPoorUser) {
            router.push('/poor/dashboard')
          } else if (this.isSocialUser) {
            router.push('/social/project-manage')
          } else {
            router.push('/')
          }
          
          return true
        } else {
          ElMessage.error('登录失败：服务器返回数据格式错误')
          return false
        }
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
        return false
      }
    },

    // 刷新访问令牌
    async refreshAccessToken() {
      try {
        if (!this.refreshToken) {
          return false
        }
        
        const response = await userApi.refreshToken(this.refreshToken)
        
        if (response.access) {
          this.token = response.access
          localStorage.setItem('userToken', response.access)
          return true
        }
        return false
      } catch (error) {
        console.error('刷新令牌失败:', error)
        return false
      }
    },

    // 登出方法
    async logout() {
      try {
        // 清除本地存储的令牌和用户信息
        this.setTokens('', '')
        this.setUserInfo(null)
        
        // 可选：调用后端登出API
        // await userApi.logout()
        
        ElMessage.success('已退出登录')
        router.push('/login')
        return true
      } catch (error) {
        console.error('登出失败:', error)
        return false
      }
    },

    // 获取当前用户信息
    async fetchUserInfo() {
      try {
        const response = await userApi.getMe()
        this.setUserInfo(response)
        return response
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return null
      }
    },

    async register(userData) {
      // 注册逻辑保持不变，注册后通常需要用户手动登录
      try {
        await userApi.register(userData); // 调用注册 API
        ElMessage.success('注册成功，请登录');
        return true;
      } catch (error) {
        console.error('注册失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '注册失败');
        return false;
      }
    },

    // 更新用户信息
    async updateUserInfo(userData) {
      // ... (基本不变, 确保更新后也保存 userType) ...
      const userId = this.userId;
      if (!userId) {
        ElMessage.error('无法更新信息：用户未登录或用户信息不完整');
        return false;
      }
      try {
        const updatedUserInfo = await userApi.updateUserInfo(userId, userData);
        // 合并旧信息和更新后的信息，确保 userType 等字段保留
        this.setUserInfo({ ...this.userInfo, ...updatedUserInfo });
        ElMessage.success('用户信息更新成功');
        return true;
      } catch (error) {
        console.error('更新用户信息失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '更新用户信息失败');
        return false;
      }
    },

    // 修改密码
    async changePassword(passwordData) {
      // ... (保持不变) ...
       const userId = this.userId;
       if (!userId) {
         ElMessage.error('无法修改密码：用户未登录');
         return false;
       }
      try {
        await userApi.changePassword(passwordData);
        ElMessage.success('密码修改成功');
        return true;
      } catch (error) {
        console.error('密码修改失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '密码修改失败');
        return false;
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
  }
})
