import request from '@/utils/request'

// 获取项目列表
export function getProjects(params) {
  return request({
    url: '/poverty/projects/',
    method: 'get',
    params
  })
}

// 获取项目详情
export function getProjectDetail(id) {
  return request({
    url: `/poverty/projects/${id}/`,
    method: 'get'
  })
}

// 创建项目
export function createProject(data) {
  return request({
    url: '/poverty/projects/',
    method: 'post',
    data
  })
}

// 更新项目
export function updateProject(id, data) {
  return request({
    url: `/poverty/projects/${id}/`,
    method: 'put',
    data
  })
}

// 删除项目
export function deleteProject(id) {
  return request({
    url: `/poverty/projects/${id}/`,
    method: 'delete'
  })
}

// 发布项目
export function publishProject(id) {
  return request({
    url: `/poverty/projects/${id}/publish/`,
    method: 'post'
  })
}

// 结束项目
export function closeProject(id) {
  return request({
    url: `/poverty/projects/${id}/close/`,
    method: 'post'
  })
}

// 获取我的项目
export function getMyProjects(params) {
  return request({
    url: '/poverty/projects/my_projects/',
    method: 'get',
    params
  })
}

// 获取已发布的项目
export function getPublishedProjects(params) {
  return request({
    url: '/poverty/projects/published_projects/',
    method: 'get',
    params
  })
}

// 上传项目图片
export function uploadProjectImage(file, projectId = null) {
  const formData = new FormData()
  formData.append('image', file)
  if (projectId) {
    formData.append('project_id', projectId)
  }
  
  return request({
    url: '/poverty/projects/upload-image/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}


