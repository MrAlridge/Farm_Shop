const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django 后端地址
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': '' // 如果你的 Django API 没有 /api 前缀，可以取消注释这行
        // }
      }
    }
  }
})
