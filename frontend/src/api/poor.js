// 贫困户注册
export const registerPoor = async (userData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          username: userData.username,
          status: 'pending',
          message: '注册成功，等待审核'
        }
      })
    }, 1000)
  })
}

// 贫困户登录
export const loginPoor = async (credentials) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          token: 'poor-token-123',
          userInfo: {
            id: 1,
            username: credentials.username,
            role: 'poor',
            status: 'approved'
          }
        }
      })
    }, 1000)
  })
}

// 获取贫困户信息
export const getPoorInfo = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          username: '张三',
          familyMembers: 4,
          annualIncome: 20000,
          address: '某省某市某县某村',
          status: 'approved',
          assistanceNeeds: ['教育资助', '物资援助']
        }
      })
    }, 1000)
  })
}

// 提交申请材料
export const submitApplication = async (applicationData) => {
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

// 获取申请状态
export const getApplicationStatus = async (id) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          status: 'approved',
          reviewNotes: '符合条件，已通过审核'
        }
      })
    }, 1000)
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