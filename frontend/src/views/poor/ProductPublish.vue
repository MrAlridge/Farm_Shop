<template>
  <div class="product-publish">
    <el-card class="page-header">
      <h2>发布农产品</h2>
    </el-card>

    <el-card class="publish-form">
      <el-form
        ref="formRef"
        :model="productForm"
        :rules="rules"
        label-width="120px"
        class="product-form"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <h3>基本信息</h3>
          <el-form-item label="商品名称" prop="name">
            <el-input v-model="productForm.name" placeholder="请输入商品名称" />
          </el-form-item>
          
          <el-form-item label="商品分类" prop="category">
            <el-select v-model="productForm.category" placeholder="请选择商品分类">
              <el-option
                v-for="item in categories"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="商品图片" prop="image">
            <el-upload
              class="product-uploader"
              :show-file-list="false"
              :before-upload="beforeImageUpload"
              :http-request="uploadImage"
            >
              <img v-if="productForm.image" :src="productForm.image" class="product-image" />
              <el-icon v-else class="uploader-icon"><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">建议尺寸：800x800px，支持 jpg、png 格式</div>
          </el-form-item>
        </div>

        <!-- 价格和库存 -->
        <div class="form-section">
          <h3>价格和库存</h3>
          <el-form-item label="商品价格" prop="price">
            <el-input-number
              v-model="productForm.price"
              :precision="2"
              :step="0.1"
              :min="0"
              placeholder="请输入商品价格"
            />
            <span class="unit">元</span>
          </el-form-item>

          <el-form-item label="商品库存" prop="stock">
            <el-input-number
              v-model="productForm.stock"
              :min="0"
              :step="1"
              placeholder="请输入商品库存"
            />
            <span class="unit">件</span>
          </el-form-item>

          <el-form-item label="计量单位" prop="unit">
            <el-input v-model="productForm.unit" placeholder="请输入计量单位，如：斤、个、箱等" />
          </el-form-item>
        </div>

        <!-- 商品描述 -->
        <div class="form-section">
          <h3>商品描述</h3>
          <!-- <el-form-item label="商品简介" prop="description">
            <el-input
              v-model="productForm.description"
              type="textarea"
              :rows="4"
              placeholder="请输入商品简介"
            />
          </el-form-item> -->

          <el-form-item label="商品简介" prop="details">
            <el-input
              v-model="productForm.details"
              type="textarea"
              :rows="6"
              placeholder="请输入商品详细信息，如：产地、规格、保质期等"
            />
          </el-form-item>
        </div>

        <!-- 发货信息 -->
        <!-- <div class="form-section">
          <h3>发货信息</h3>
          <el-form-item label="发货地址" prop="address">
            <el-input v-model="productForm.address" placeholder="请输入发货地址" />
          </el-form-item>

          <el-form-item label="发货时间" prop="shippingTime">
            <el-select v-model="productForm.shippingTime" placeholder="请选择发货时间">
              <el-option label="24小时内" value="24h" />
              <el-option label="48小时内" value="48h" />
              <el-option label="72小时内" value="72h" />
              <el-option label="7天内" value="7d" />
            </el-select>
          </el-form-item>
        </div> -->

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button @click="resetForm">重置</el-button>
          <el-button type="primary" @click="submitForm">发布商品</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const formRef = ref(null)

// 商品分类数据
const categories = ref([
  { id: 1, name: '新鲜水果' },
  { id: 2, name: '时令蔬菜' },
  { id: 3, name: '粮油调味' },
  { id: 4, name: '农家特产' },
  { id: 5, name: '禽蛋肉类' }
])

// 表单数据
const productForm = ref({
  name: '',
  category: '',
  image: '',
  price: 0,
  stock: 0,
  unit: '',
  description: '',
  details: '',
  address: '',
  shippingTime: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  image: [
    { required: true, message: '请上传商品图片', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入商品价格', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入商品库存', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请输入计量单位', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入商品简介', trigger: 'blur' }
  ],
  details: [
    { required: true, message: '请输入商品详情', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入发货地址', trigger: 'blur' }
  ],
  shippingTime: [
    { required: true, message: '请选择发货时间', trigger: 'change' }
  ]
}

// 图片上传前的验证
const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 上传图片
const uploadImage = async (options) => {
  try {
    // TODO: 实现图片上传到服务器的逻辑
    // 这里模拟上传成功
    const reader = new FileReader()
    reader.readAsDataURL(options.file)
    reader.onload = () => {
      productForm.value.image = reader.result
    }
    ElMessage.success('图片上传成功')
  } catch (error) {
    ElMessage.error('图片上传失败')
  }
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      // TODO: 实现提交商品信息的逻辑
      ElMessage.success('商品发布成功')
      resetForm()
    }
  })
}

onMounted(() => {
  // TODO: 获取商品分类列表
})
</script>

<style scoped>
.product-publish {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.publish-form {
  margin-bottom: 20px;
}

.form-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.form-section:last-child {
  border-bottom: none;
}

.form-section h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  color: #303133;
}

.product-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.product-uploader:hover {
  border-color: #409eff;
}

.uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.unit {
  margin-left: 10px;
  color: #606266;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

:deep(.el-input-number) {
  width: 200px;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}
</style> 