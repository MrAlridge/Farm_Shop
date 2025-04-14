import request from '@/utils/request';

// 登录
export const login = (data) => {
  return request({
    url: '/users/login/',
    method: 'post',
    data
  })
}

// 注册
export const register = (data) => {
  return request({
    url: '/users/users/',
    method: 'post',
    data
  })
}

export const logout = async () => {
  return Promise.resolve({
    data: {
      message: '退出成功'
    }
  })
}

export const getUserInfo = async () => {
  return request(
    {
      url: `users/users/${userId}`,
      method: 'GET'
    }
  )
}

export const updateUserInfo = async (userInfo) => {
  return request(
    {
      url: `users/users/${userId}`,
      method: 'PATCH',
      data: userInfo
    }
  )
}

export const changePassword = async (passwordData) => {
  return request(
    {
      url: 'users/users/set_password',
      method: 'POST',
      data: passwordData
    }
  )
}

// 获取当前用户信息
export const getMe = () => {
  return request({
    url: '/users/users/me/',
    method: 'get'
  })
}

// 获取申请列表
export const getApplications = () => {
  return request({
    url: '/poverty/applications/',
    method: 'get'
  })
}

// 提交申请
export const submitApplication = (data) => {
  return request({
    url: '/poverty/applications/',
    method: 'post',
    data
  })
}

// 取消申请
export const cancelApplication = (id) => {
  return request({
    url: `/poverty/applications/${id}/`,
    method: 'delete'
  })
}

// 获取申请详情
export const getApplicationDetail = (id) => {
  return request({
    url: `/poverty/applications/${id}/`,
    method: 'get'
  })
}

// 获取援助记录
export function getAssistanceRecords() {
  return request({
    url: 'poverty/assistance-records/',
    method: 'get'
  })
}

// 提交援助记录
export function submitAssistanceRecord(data) {
  return request({
    url: 'poverty/assistance-records/',
    method: 'post',
    data
  })
}

// 获取帮扶项目列表
export const getAssistanceProjects = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '寒暑假辅导',
            provider: '某教育机构',
            description: '为贫困家庭子女提供寒暑假学习辅导',
            status: 'available'
          },
          {
            id: 2,
            name: '技能培训',
            provider: '某职业培训学校',
            description: '提供职业技能培训，帮助就业',
            status: 'available'
          }
        ]
      })
    }, 1000)
  })
}

// 申请帮扶项目
export const applyForProject = async (projectId) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          status: 'pending',
          message: '申请已提交，等待审核'
        }
      })
    }, 1000)
  })
}

// 获取物资援助列表
export const getMaterialAssistance = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '大米',
            quantity: 50,
            unit: 'kg',
            provider: '某慈善基金会',
            status: 'available'
          },
          {
            id: 2,
            name: '食用油',
            quantity: 10,
            unit: 'L',
            provider: '某企业',
            status: 'available'
          }
        ]
      })
    }, 1000)
  })
}

// 申请物资援助
export const applyForMaterial = async (materialId) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          status: 'pending',
          message: '申请已提交，等待审核'
        }
      })
    }, 1000)
  })
}

// 获取教育资助信息
export const getEducationAssistance = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            name: '学费减免',
            description: '提供50%学费减免',
            provider: '某教育基金会',
            status: 'available'
          },
          {
            id: 2,
            name: '全额资助',
            description: '提供全额学费资助',
            provider: '某慈善机构',
            status: 'available'
          }
        ]
      })
    }, 1000)
  })
}

// 申请教育资助
export const applyForEducation = async (assistanceId) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          status: 'pending',
          message: '申请已提交，等待审核'
        }
      })
    }, 1000)
  })
}

export const getApplicationStatus = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      
    })
  })
}

// 刷新token
export const refreshToken = (refresh) => {
  return request({
    url: '/token/refresh/',
    method: 'post',
    data: { refresh }
  })
}

// 获取贫困户申请列表
export const getPovertyApplications = (params = {}) => {
  return request({
    url: '/poverty/applications/',
    method: 'get',
    params: {
      page: params.page || 1,
      page_size: params.pageSize || 10,
      ...params
    }
  }).then(response => {
    if (response && Array.isArray(response.results)) {
      return {
        data: response.results,
        total: response.count,
        next: response.next,
        previous: response.previous
      }
    }
    return { data: [], total: 0 }
  })
}

// 提交贫困户申请
export const submitPovertyApplication = (data) => {
  return request({
    url: '/poverty/applications/',
    method: 'post',
    data
  })
}

// 获取申请详情
export const getPovertyApplicationDetail = (id) => {
  return request({
    url: `/poverty/applications/${id}/`,
    method: 'get'
  })
}

// 取消申请
export const cancelPovertyApplication = (id) => {
  return request({
    url: `/poverty/applications/${id}/`,
    method: 'delete'
  })
}

// 审核通过申请
export const approvePovertyApplication = (id) => {
  return request({
    url: `/poverty/applications/${id}/approve/`,
    method: 'post'
  })
}

// 拒绝申请
export const rejectPovertyApplication = (id, data) => {
  return request({
    url: `/poverty/applications/${id}/reject/`,
    method: 'post',
    data
  })
}