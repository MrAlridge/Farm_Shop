import request from '@/utils/request';

// 模拟登录
export const login = async (loginData) => {
  return request(
    {
      url: 'users/login/',
      method: 'POST',
      data: loginData
    }
  )

}

// 模拟注册
export const register = async (registerData) => {
  return request(
    {
      url: 'users/users/',
      method: 'POST',
      data: registerData
    }
  )
  
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

export const getMe = () => {
  return request({
    url: 'users/users/me/',
  })
}
