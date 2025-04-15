<template>
  <footer class="nav-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>关于我们</h3>
        <p>扶贫商城致力于帮助贫困地区农产品销售，助力乡村振兴。</p>
      </div>
      
      <div class="footer-section">
        <h3>联系方式</h3>
        <p>电话：400-123-4567</p>
        <p>邮箱：support@fupinshop.com</p>
        <p>地址：北京市朝阳区xxx街道xxx号</p>
      </div>
      
      <div class="footer-section">
        <h3>关注我们</h3>
        <div class="social-links">
          <el-button type="text">
            <el-icon><ChatDotRound /></el-icon>
            微信
          </el-button>
          <el-button type="text">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>© 2024 扶贫商城 版权所有</p>
      <div class="footer-links">
        <router-link to="/about">关于我们</router-link>
        <router-link to="/privacy">隐私政策</router-link>
        <router-link to="/terms">服务条款</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ChatDotRound, Share } from '@element-plus/icons-vue'
</script>

<style scoped>
.nav-footer {
  background-color: var(--background-color);
  color: var(--text-color-secondary);
  padding: 40px 0 20px;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-section {
  flex: 1;
  margin: 0 20px;
}

.footer-section h3 {
  color: var(--text-color);
  margin-bottom: 15px;
  font-size: 16px;
}

.footer-section p {
  margin: 8px 0;
  font-size: 14px;
}

.social-links {
  display: flex;
  gap: 15px;
}

.footer-bottom {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.footer-links {
  margin-top: 10px;
}

.footer-links a {
  color: var(--text-color-secondary);
  text-decoration: none;
  margin: 0 10px;
  font-size: 14px;
}

.footer-links a:hover {
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
  }
  
  .footer-section {
    margin: 20px 0;
  }
}
</style> 