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
          <div class="user-type">
            <el-tag :type="userTypeTag">{{ userTypeLabel }}</el-tag>
          </div>
          
          <el-card class="menu-card">
            <el-menu
              :default-active="activeMenu"
              class="user-menu"
              @select="handleMenuSelect"
              style="width: 1000px;"
            >
              <el-menu-item index="profile">
                <el-icon><User /></el-icon>
                <span>个人资料</span>
              </el-menu-item>
              <!-- <el-menu-item index="address">
                <el-icon><Location /></el-icon>
                <span>收货地址</span>
              </el-menu-item> -->
              <!-- <el-menu-item index="security">
                <el-icon><Lock /></el-icon>
                <span>修改密码</span>
              </el-menu-item> -->
              <el-menu-item index="orders">
                <el-icon><List /></el-icon>
                <span>我的订单</span>
              </el-menu-item>
              <!-- 普通用户显示申请入口 -->
              <el-menu-item v-if="userStore.isSocialUser" index="poor-application">
                <el-icon><Document /></el-icon>
                <span>申请贫困户</span>
              </el-menu-item>
              <!-- 管理员显示审核入口 -->
              <el-menu-item v-if="userStore.isAdminUser" index="application-review">
                <el-icon><Check /></el-icon>
                <span>申请审核</span>
              </el-menu-item>
            </el-menu>
          </el-card>
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
            ref="profileFormRef"
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
          </el-form>
        </el-card>
        
        <!-- 贫困户申请 -->
        <el-card v-if="activeMenu === 'poor-application'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>申请贫困户</span>
            </div>
          </template>
          
          <div v-if="Array.isArray(poorApplications)" class="pending-notice">
            <div v-if="hasPendingApplication" class="pending-notice">
              <el-alert
                title="您有正在审核中的申请"
                type="warning"
                :closable="false"
                description="请耐心等待审核结果"
              />
            </div>
          
            <div v-else>
          <el-form
                ref="poorApplicationFormRef"
                :model="poorApplicationForm"
                :rules="poorApplicationRules"
            label-width="100px">
                <el-form-item label="申请标题" label-width="120px" prop="title">
              <el-input
                    v-model="poorApplicationForm.title"
                    placeholder="请输入申请标题"
                  />
            </el-form-item>
                
                <el-form-item label="申请内容" label-width="120px" prop="content">
              <el-input
                    v-model="poorApplicationForm.content"
                    type="textarea"
                    :rows="4"
                    placeholder="请详细描述您的情况"
                  />
            </el-form-item>
                
                <!-- <el-form-item label="证明材料">
                  <el-upload
                    action="/api/upload"
                    :on-success="handleUploadSuccess"
                    :on-error="handleUploadError"
                    :before-upload="beforeUpload"
                    multiple
                  >
                    <el-button type="primary">上传证明材料</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        支持jpg/png/pdf格式，单个文件不超过10MB
                      </div>
                    </template>
                  </el-upload>
            </el-form-item> -->

            <el-form-item label="家庭成员数量" label-width="120px" prop="familyMemberCount">
              <el-input-number v-model="poorApplicationForm.familyMemberCount" :min="0" :max="100" />
            </el-form-item>

            <el-form-item label="年收入" label-width="120px" prop="annualIncome">
              <el-input-number v-model="poorApplicationForm.annualIncome" />
            </el-form-item>
                
            <el-form-item>
                  <el-button type="primary" @click="handleSubmitApplication">
                    提交申请
              </el-button>
            </el-form-item>
          </el-form>
            </div>

            <!-- 申请历史 -->
            <div v-if="poorApplications.length > 0" class="application-history">
              <el-divider>申请历史</el-divider>
              <el-timeline>
                <el-timeline-item
                  v-for="app in poorApplications"
                  :key="app.id"
                  :type="getApplicationStatusType(app.status)"
                  :timestamp="formatDate(app.created_at)"
                >
                  <el-card>
                    <h4>
                      状态：
                      <el-tag :type="getApplicationStatusType(app.status)">
                        {{ getApplicationStatusText(app.status) }}
                      </el-tag>
                    </h4>
                    <p>申请原因：{{ app.reason }}</p>
                    <p v-if="app.review_comment">审核意见：{{ app.review_comment }}</p>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>

          <!-- 添加加载状态 -->
          <div v-else class="loading-state">
            <el-skeleton :rows="3" animated />
          </div>
        </el-card>
        
        <!-- 管理员审核页面 -->
        <el-card v-if="activeMenu === 'application-review'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>贫困户申请审核</span>
              <el-button type="primary" @click="fetchPendingApplications">
                刷新列表
              </el-button>
            </div>
          </template>
          
          <el-table 
            v-loading="loading"
            :data="pendingApplications"
            style="width: 100%"
          >
            <el-table-column 
              v-for="col in columns"
              :key="col.prop"
              v-bind="col"
            >
              <template #default="{ row }" v-if="col.prop === 'created_at'">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="success"
                  size="small"
                  @click="handleApprove(row)"
                >
                  通过
                </el-button>
                <el-button
                  type="danger"
                  size="small"
                  @click="handleReject(row)"
                >
                  拒绝
                  </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加分页组件 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="pagination.currentPage"
              v-model:page-size="pagination.pageSize"
              :total="pagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next"
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>

          <el-empty
            v-if="!loading && pendingApplications.length === 0"
            description="暂无待审核的申请"
          />
        </el-card>

        <!-- 收货地址 -->
        <el-card v-if="activeMenu === 'address'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>收货地址</span>
              <el-button type="primary" @click="addAddress">添加地址</el-button>
            </div>
          </template>
          
          <el-table :data="addresses" style="width: 100%">
            <el-table-column prop="name" label="收货人" width="120" />
            <el-table-column prop="phone" label="联系电话" width="150" />
            <el-table-column prop="address" label="详细地址" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="editAddress(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteAddress(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 我的订单 -->
        <el-card v-if="activeMenu === 'orders'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>我的订单</span>
            </div>
          </template>
          <OrderList />
        </el-card>

        <!-- 修改密码 -->
        <el-card v-if="activeMenu === 'security'" class="content-card">
          <template #header>
            <div class="card-header">
              <span>修改密码</span>
            </div>
          </template>
          
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px">
            <el-form-item label="原密码" prop="oldPassword">
              <el-input v-model="passwordForm.oldPassword" type="password" />
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
              <el-input v-model="passwordForm.newPassword" type="password" />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input v-model="passwordForm.confirmPassword" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- 拒绝原因对话框 -->
    <el-dialog v-model="rejectDialogVisible" title="拒绝原因" width="500px">
      <el-form :model="rejectForm">
        <el-form-item label="拒绝原因" prop="reason">
          <el-input
            v-model="rejectForm.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入拒绝原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="rejectDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmReject">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  Location,
  Lock,
  List,
  Document,
  Check,
  Plus
} from '@element-plus/icons-vue'
import { 
  getPovertyApplications,
  submitPovertyApplication,
  getPovertyApplicationDetail,
  cancelPovertyApplication,
  approvePovertyApplication,
  rejectPovertyApplication
} from '@/api/user'
import { 
  formatDate, 
  formatPhone, 
  formatStatus 
} from '@/utils/format'

const router = useRouter()
const userStore = useUserStore()
const activeMenu = ref('profile')

// 添加环境变量的引用
const isDevelopment = import.meta.env.DEV // Vite 中使用 import.meta.env 替代 process.env

// 用户信息
const userInfo = computed(() => ({
  username: userStore.username,
  avatar: userStore.userInfo.avatar || ''
}))

// 用户类型相关
const userTypeLabel = computed(() => {
  const typeMap = {
    'social': '普通用户',
    'poor': '贫困户',
    'admin': '管理员'
  }
  return typeMap[userStore.userType] || '普通用户'
})

const userTypeTag = computed(() => {
  const typeMap = {
    'social': 'info',
    'poor': 'success',
    'admin': 'danger'
  }
  return typeMap[userStore.userType] || 'info'
})

// 表单验证规则
const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const poorApplicationRules = {
  title: [
    { required: true, message: '请输入申请标题', trigger: 'blur' },
    { min: 10, message: '申请标题至少10个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入申请内容', trigger: 'blur' },
    { min: 10, message: '申请内容至少10个字符', trigger: 'blur' }
  ],
  familyMemberCount: [
    { required: true, message: '请输入家庭成员数量', trigger: 'blur' },
    { type: 'number', message: '请输入正确的数字', trigger: 'blur' }
  ],
  annualIncome: [
    { required: false, message: '请输入年收入', trigger: 'blur' },
    { type: 'number', message: '请输入正确的数字', trigger: 'blur' }
  ]
}

// 个人资料表单
const profileFormRef = ref(null)
const profileForm = ref({
  username: userStore.username || '',
  phone: userStore.phoneNumber || '',
  email: userStore.userInfo.email || ''
})

// 贫困户申请相关
const poorApplications = ref([])
const poorApplicationFormRef = ref(null)
const poorApplicationForm = ref({
  title: '',
  type: 'poverty', // 申请类型为贫困户
  content: '',     // 申请内容
  familyMemberCount: 0,
  annualIncome: 0
})

const hasPendingApplication = computed(() => {
  return Array.isArray(poorApplications.value) && 
         poorApplications.value.some(app => app.status === 'pending')
})

// 管理员审核相关
const pendingApplications = ref([])
const loading = ref(false)
const rejectDialogVisible = ref(false)
const rejectForm = ref({
  reason: '',
  applicationId: null
})

// 分页相关
const pagination = ref({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 地址相关
const addresses = ref([])
const addAddress = () => {
  // 添加地址的逻辑
  ElMessage.info('添加地址功能待实现')
}

const editAddress = (address) => {
  // 编辑地址的逻辑
  ElMessage.info('编辑地址功能待实现')
}

const deleteAddress = (address) => {
  // 删除地址的逻辑
  ElMessage.info('删除地址功能待实现')
}

// 密码相关
const passwordFormRef = ref(null)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const changePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 这里应该调用修改密码的API
        ElMessage.success('密码修改成功')
        passwordForm.value = {
          oldPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      } catch (error) {
        ElMessage.error('密码修改失败')
      }
    }
  })
}

// 方法
const handleMenuSelect = (index) => {
  activeMenu.value = index
  if (index === 'orders') {
    router.push('/orders')
  }
}

const saveProfile = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await userStore.updateUserInfo(profileForm.value)
  ElMessage.success('保存成功')
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleSubmitApplication = async () => {
  if (!poorApplicationFormRef.value) return

  await poorApplicationFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const applicationData = {
          title: poorApplicationForm.value.title,
          content: poorApplicationForm.value.content,
          family_members: poorApplicationForm.value.familyMemberCount,
          household_income: poorApplicationForm.value.annualIncome
        }

        await submitPovertyApplication(applicationData)
        ElMessage.success('申请提交成功')
        await fetchApplications()
        poorApplicationForm.value = {
          title: '',
          content: '',
          familyMemberCount: 0,
          annualIncome: 0
        }
      } catch (error) {
        console.error('提交申请失败:', error)
        ElMessage.error(error.response?.data?.detail || '提交申请失败')
      }
    }
  })
}

const handleUploadSuccess = (response) => {
  poorApplicationForm.value.supporting_documents = response.url
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}

const beforeUpload = (file) => {
  const isValidType = ['image/jpeg', 'image/png', 'application/pdf'].includes(file.type)
  if (!isValidType) {
    ElMessage.error('只能上传 JPG/PNG/PDF 格式的文件')
    return false
  }
  return true
}

const getApplicationStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

// 状态文本映射
const statusMap = {
  'pending': '审核中',
  'approved': '已通过',
  'rejected': '已拒绝'
}

// 在模板中使用格式化函数
const getApplicationStatusText = (status) => {
  return formatStatus(status, statusMap)
}

// 格式化手机号显示
const formatPhoneDisplay = computed(() => {
  return formatPhone(profileForm.value.phone)
})

const handleApprove = async (application) => {
  try {
    await ElMessageBox.confirm(
      '确定要通过该申请吗？通过后申请人将成为贫困户用户',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await approvePovertyApplication(application.id)
    ElMessage.success('已通过申请')
    await fetchPendingApplications() // 刷新列表
  } catch (error) {
    if (error !== 'cancel') {
      console.error('审核失败:', error)
      ElMessage.error(error.response?.data?.detail || '审核失败')
    }
  }
}

const handleReject = async (application) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      '请输入拒绝原因',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        inputValidator: (value) => {
          if (!value) {
            return '请输入拒绝原因'
          }
          return true
        }
      }
    )
    
    if (reason) {
      await rejectPovertyApplication(application.id, { review_comment: reason })
      ElMessage.success('已拒绝申请')
      await fetchPendingApplications() // 刷新列表
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('审核失败:', error)
      ElMessage.error(error.response?.data?.detail || '审核失败')
    }
  }
}

const viewDocument = (url) => {
  window.open(url, '_blank')
}

const fetchApplications = async () => {
  try {
    const response = await getPovertyApplications()
    poorApplications.value = response.data || []
  } catch (error) {
    console.error('获取申请列表失败:', error)
    ElMessage.error('获取申请列表失败')
  }
}

const fetchPendingApplications = async () => {
  loading.value = true
  try {
    const response = await getPovertyApplications()
    console.log('获取到的原始数据:', response)

    if (response && Array.isArray(response.data)) {
      pendingApplications.value = response.data.filter(app => app.status === 'pending')
      // 如果原始响应中包含分页信息
      if (response.total) {
        pagination.value.total = response.total
      }
    } else {
      console.warn('未获取到有效数据')
      pendingApplications.value = []
    }
  } catch (error) {
    console.error('获取待审核申请失败:', error)
    ElMessage.error('获取待审核申请失败')
    pendingApplications.value = []
  } finally {
    loading.value = false
  }
}

const handleCancelApplication = async (application) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消该申请吗？此操作不可恢复',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await cancelPovertyApplication(application.id)
    ElMessage.success('申请已取消')
    await fetchApplications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消申请失败:', error)
      ElMessage.error('取消申请失败')
    }
  }
}

// 修改表格列定义，确保与后端返回的数据字段匹配
const columns = [
  {
    prop: 'username',
    label: '申请人',
    width: '120'
  },
  {
    prop: 'title',
    label: '申请标题'
  },
  {
    prop: 'content',
    label: '申请内容',
    showOverflowTooltip: true
  },
  {
    prop: 'created_at',
    label: '申请时间',
    width: '180',
    formatter: (row) => formatDate(row.created_at)
  }
]

// 处理页码变化
const handlePageChange = (page) => {
  pagination.value.currentPage = page
  fetchPendingApplications()
}

// 处理每页条数变化
const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.currentPage = 1
  fetchPendingApplications()
}

onMounted(async () => {
  const userStore = useUserStore()
  if (userStore.isAdminUser) {
    await fetchPendingApplications()
  } else if (userStore.isSocialUser) {
    await fetchApplications()
  }
})
</script>

<style scoped>
.user-center {
  padding: 20px;
}

.user-info-card {
  text-align: center;
  padding: 20px;
}

.user-avatar {
  margin-bottom: 15px;
}

.username {
  margin: 10px 0;
}

.user-type {
  margin-bottom: 20px;
}

.content-card {
  min-height: 500px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pending-notice {
  margin-bottom: 20px;
}

.application-history {
  margin-top: 30px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.loading-state {
  padding: 20px;
}

.el-upload__tip {
  font-size: 12px;
  color: #606266;
  margin-top: 7px;
}

.application-form {
  margin-bottom: 20px;
}

/* 添加表格内容过长时的样式 */
:deep(.el-table .cell) {
  white-space: pre-line;
}

.debug-info {
  margin: 10px 0;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.menu-card {
  margin-bottom: 20px;
}

.user-menu {
  border-right: none;
}

.user-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  padding: 0 20px;
  white-space: nowrap;
}

.user-menu :deep(.el-menu-item.is-active) {
  background-color: #ecf5ff;
  color: #409eff;
}

.user-menu :deep(.el-menu-item:hover) {
  background-color: #f5f7fa;
}
</style> 