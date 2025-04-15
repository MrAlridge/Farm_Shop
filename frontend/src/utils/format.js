/**
 * 日期格式化
 * @param {string|Date} date 日期
 * @param {string} format 格式化模式，默认 'YYYY-MM-DD HH:mm'
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (date, format = 'YYYY-MM-DD HH:mm') => {
  if (!date) return ''
  
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const minute = String(d.getMinutes()).padStart(2, '0')
  const second = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second)
}

/**
 * 金额格式化
 * @param {number} price 金额
 * @param {string} currency 货币符号，默认 '¥'
 * @returns {string} 格式化后的金额字符串
 */
export const formatPrice = (price, currency = '¥') => {
  if (!price && price !== 0) return ''
  return `${currency}${Number(price).toFixed(2)}`
}

/**
 * 文件大小格式化
 * @param {number} bytes 字节数
 * @returns {string} 格式化后的文件大小
 */
export const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`
}

/**
 * 手机号格式化（中间4位隐藏）
 * @param {string} phone 手机号
 * @returns {string} 格式化后的手机号
 */
export const formatPhone = (phone) => {
  if (!phone) return ''
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

/**
 * 身份证号格式化（中间8位隐藏）
 * @param {string} idCard 身份证号
 * @returns {string} 格式化后的身份证号
 */
export const formatIdCard = (idCard) => {
  if (!idCard) return ''
  return idCard.replace(/(\d{6})\d{8}(\d{4})/, '$1********$2')
}

/**
 * 状态格式化
 * @param {string} status 状态值
 * @param {Object} statusMap 状态映射
 * @returns {string} 格式化后的状态文本
 */
export const formatStatus = (status, statusMap = {}) => {
  return statusMap[status] || status
}

/**
 * 数字格式化（添加千位分隔符）
 * @param {number} num 数字
 * @returns {string} 格式化后的数字
 */
export const formatNumber = (num) => {
  if (!num && num !== 0) return ''
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * 姓名脱敏
 * @param {string} name 姓名
 * @returns {string} 脱敏后的姓名
 */
export const formatName = (name) => {
  if (!name) return ''
  if (name.length <= 2) {
    return name.substr(0, 1) + '*'
  }
  return name.substr(0, 1) + '*'.repeat(name.length - 2) + name.substr(-1)
} 