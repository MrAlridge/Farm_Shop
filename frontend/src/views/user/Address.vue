<template>
  <div class="address-container">
    <el-card class="address-card">
      <template #header>
        <div class="card-header">
          <span>收货地址</span>
          <el-button type="primary" @click="handleAdd">添加地址</el-button>
        </div>
      </template>
      
      <el-table :data="addressList" style="width: 100%">
        <el-table-column prop="name" label="收货人" width="120" />
        <el-table-column prop="phone" label="手机号码" width="150" />
        <el-table-column prop="address" label="收货地址" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑地址对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加地址' : '编辑地址'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="收货人" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        
        <el-form-item label="收货地址" prop="address">
          <el-input v-model="form.address" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()
const formRef = ref(null)
const dialogVisible = ref(false)
const dialogType = ref('add')
const currentAddress = ref(null)

const addressList = ref([
  {
    id: 1,
    name: '张三',
    phone: '13800138000',
    address: '北京市朝阳区建国路88号'
  },
  {
    id: 2,
    name: '李四',
    phone: '13900139000',
    address: '上海市浦东新区陆家嘴环路1000号'
  }
])

const form = reactive({
  name: '',
  phone: '',
  address: ''
})

const rules = {
  name: [
    { required: true, message: '请输入收货人姓名', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' }
  ]
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.name = ''
  form.phone = ''
  form.address = ''
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  currentAddress.value = row
  form.name = row.name
  form.phone = row.phone
  form.address = row.address
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(
    '确定要删除该收货地址吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // 调用删除地址的 API
      await userStore.deleteAddress(row.id)
      addressList.value = addressList.value.filter(item => item.id !== row.id)
      ElMessage.success('删除成功')
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    if (dialogType.value === 'add') {
      // 调用添加地址的 API
      const newAddress = await userStore.addAddress(form)
      addressList.value.push(newAddress)
      ElMessage.success('添加成功')
    } else {
      // 调用更新地址的 API
      await userStore.updateAddress(currentAddress.value.id, form)
      const index = addressList.value.findIndex(item => item.id === currentAddress.value.id)
      if (index !== -1) {
        addressList.value[index] = { ...currentAddress.value, ...form }
      }
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('操作失败，请检查输入')
  }
}
</script>

<style scoped>
.address-container {
  max-width: 1000px;
  margin: 0 auto;
}

.address-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 