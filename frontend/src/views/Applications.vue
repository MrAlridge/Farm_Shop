<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getApplications, cancelApplication } from '@/api/user'
import { useUserStore } from '@/store/modules/user'

const router = useRouter()
const userStore = useUserStore()
const activeTab = ref('all')
const applications = ref([])
const loading = ref(false)

// 检查用户权限
const checkUserPermission = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.error('请先登录')
    router.push('/login')
    return false
  }
  
  if (!userStore.isPoorUser) {
    ElMessage.error('只有贫困户用户可以访问此页面')
    router.push('/')
    return false
  }
  
  return true
}

// 获取申请列表
const fetchApplications = async () => {
  if (!checkUserPermission()) return
  
  loading.value = true
  try {
    const response = await getApplications()
    applications.value = response.data || []
  } catch (error) {
    console.error('获取申请列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '获取申请列表失败')
  } finally {
    loading.value = false
  }
}

// ... 其他代码保持不变 ...
</script> 