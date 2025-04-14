<template>
  <div class="user-center">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :span="6">
        <el-card class="user-info-card">
          <div class="user-avatar">
            <el-avatar :size="100" :src="userInfo.avatar" />
          </div>
          <h3 class="username">{{ userInfo.username }}</h3>
          <p class="user-level">会员等级：{{ userInfo.level }}</p>
          
          <el-menu
            :default-active="activeMenu"
            class="user-menu"
            @select="handleMenuSelect">
            <el-menu-item index="profile">
              <el-icon><User /></el-icon>
              <span>个人资料</span>
            </el-menu-item>
            <el-menu-item index="address">
              <el-icon><Location /></el-icon>
              <span>收货地址</span>
            </el-menu-item>
            <el-menu-item index="security">
              <el-icon><Lock /></el-icon>
              <span>账户安全</span>
            </el-menu-item>
            <el-menu-item index="orders">
              <el-icon><List /></el-icon>
              <span>我的订单</span>
            </el-menu-item>
            <el-menu-item index="favorites">
              <el-icon><Star /></el-icon>
              <span>我的收藏</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
      
      <!-- 内容区域 -->
      <el-col :span="18">
        <!-- 个人资料 -->
        <el-card v-if="activeMenu === 'profile'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>个人资料</span>
              <el-button type="primary" @click="saveProfile">保存修改</el-button>
            </div>
          </template>
          
          <el-form
            ref="profileForm"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="profileForm.phone" />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" />
            </el-form-item>
            <el-form-item label="头像">
              <el-upload
                class="avatar-uploader"
                action="/api/upload"
                :show-file-list="false"
                :on-success="handleAvatarSuccess">
                <img v-if="profileForm.avatar" :src="profileForm.avatar" class="avatar">
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
              </el-upload>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 收货地址 -->
        <el-card v-if="activeMenu === 'address'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>收货地址</span>
              <el-button type="primary" @click="addAddress">新增地址</el-button>
            </div>
          </template>
          
          <el-table :data="addresses" style="width: 100%">
            <el-table-column prop="name" label="收货人" width="120" />
            <el-table-column prop="phone" label="手机号" width="120" />
            <el-table-column prop="address" label="收货地址" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" link @click="editAddress(row)">
                  编辑
                </el-button>
                <el-button type="danger" link @click="deleteAddress(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <!-- 账户安全 -->
        <el-card v-if="activeMenu === 'security'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>账户安全</span>
            </div>
          </template>
          
          <el-form
            ref="securityForm"
            :model="securityForm"
            :rules="securityRules"
            label-width="100px">
            <el-form-item label="原密码" prop="oldPassword">
              <el-input
                v-model="securityForm.oldPassword"
                type="password"
                show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="securityForm.newPassword"
                type="password"
                show-password />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="securityForm.confirmPassword"
                type="password"
                show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 我的订单 -->
        <Orders v-if="activeMenu === 'orders'" />
        
        <!-- 我的收藏 -->
        <el-card v-if="activeMenu === 'favorites'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>我的收藏</span>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="6" v-for="item in favorites" :key="item.id">
              <el-card :body-style="{ padding: '0px' }" class="favorite-item">
                <img :src="item.image" class="favorite-image">
                <div class="favorite-info">
                  <h4>{{ item.name }}</h4>
                  <p class="price">¥{{ item.price }}</p>
                  <el-button type="primary" @click="viewProduct(item.id)">
                    查看详情
                  </el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'
import {
  User,
  Location,
  Lock,
  List,
  Star,
  Plus
} from '@element-plus/icons-vue'
import Orders from './Orders.vue'

const router = useRouter()
const activeMenu = ref('profile')

// 用户信息
const userInfo = ref({
  username: useUserStore.username,
  level: '普通会员',
  avatar: useUserStore.avatar || ''
})

// 个人资料表单
const profileForm = reactive({
  username: useUserStore.username,
  phone: useUserStore.phone,
  email: useUserStore.email,
  avatar: useUserStore.avatar || ''
})

const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 收货地址
const addresses = ref([
  {
    id: 1,
    name: '张三',
    phone: '13800138000',
    address: '北京市朝阳区xxx街道xxx号'
  }
])

// 账户安全表单
const securityForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const securityRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== securityForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 收藏列表
const favorites = ref([
  {
    id: 1,
    name: '有机大米',
    price: 39.9,
    image: '/product1.jpg'
  },
  {
    id: 2,
    name: '土鸡蛋',
    price: 29.9,
    image: '/product2.jpg'
  }
])

const handleMenuSelect = (index) => {
  activeMenu.value = index
}

const saveProfile = () => {
  // TODO: 实现保存个人资料逻辑
  ElMessage.success('保存成功')
}

const handleAvatarSuccess = (response) => {
  profileForm.avatar = response.url
}

const addAddress = () => {
  // TODO: 实现新增地址逻辑
}

const editAddress = (address) => {
  // TODO: 实现编辑地址逻辑
}

const deleteAddress = (address) => {
  // TODO: 实现删除地址逻辑
}

const changePassword = () => {
  // TODO: 实现修改密码逻辑
  ElMessage.success('密码修改成功')
}

const viewProduct = (id) => {
  router.push(`/product/${id}`)
}
</script>

<style scoped>
.user-center {
  padding: 20px;
}

.user-info-card {
  text-align: center;
}

.user-avatar {
  margin-bottom: 20px;
}

.username {
  margin: 10px 0;
}

.user-level {
  color: #909399;
  margin-bottom: 20px;
}

.user-menu {
  border-right: none;
}

.content-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.avatar-uploader {
  text-align: center;
}

.avatar-uploader .avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
}

.favorite-item {
  margin-bottom: 20px;
}

.favorite-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.favorite-info {
  padding: 14px;
}

.favorite-info h4 {
  margin: 0 0 10px 0;
}

.price {
  color: #f56c6c;
  font-weight: bold;
  margin: 10px 0;
}
</style> 