// 模拟登录
export const login = async (loginData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          token: 'mock_token',
          userInfo: {
            id: 1,
            username: loginData.username,
            avatar: '/images/avatars/avatar1.jpg',
            email: 'user@example.com',
            phone: '13800138000'
          }
        }
      })
    }, 1000)
  })
}

// 模拟注册
export const register = async (registerData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '注册成功'
        }
      })
    }, 1000)
  })
}

// 模拟退出登录
export const logout = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          message: '退出成功'
        }
      })
    }, 1000)
  })
}

// 模拟获取用户信息
export const getUserInfo = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          id: 1,
          username: '测试用户',
          avatar: '/images/avatars/avatar1.jpg',
          email: 'user@example.com',
          phone: '13800138000'
        }
      })
    }, 1000)
  })
}

// 模拟更新用户信息
export const updateUserInfo = async (userInfo) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          ...userInfo,
          message: '更新成功'
        }
      })
    }, 1000)
  })
} 