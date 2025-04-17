<template>
  <div class="product-publish">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <h2>发布商品</h2>
        </div>
      </template>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="publish-form"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        
        <el-form-item label="商品分类" prop="category_id">
          <el-select v-model="form.category_id" placeholder="请选择商品分类">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 暂时隐藏图片上传功能
        <el-form-item label="商品图片" prop="image">
          <el-upload
            class="image-uploader"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            :http-request="handleImageUpload"
          >
            <img v-if="form.image" :src="form.image" class="image" />
            <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="image-tip">支持 jpg、png 格式，大小不超过 2MB</div>
        </el-form-item>
        -->
        
        <el-form-item label="商品价格" prop="price">
          <el-input-number
            v-model="form.price"
            :precision="2"
            :step="0.1"
            :min="0"
            placeholder="请输入商品价格"
          />
        </el-form-item>
        
        <el-form-item label="库存数量" prop="stock">
          <el-input-number
            v-model="form.stock"
            :min="0"
            :step="1"
            placeholder="请输入库存数量"
          />
        </el-form-item>
        
        <el-form-item label="计量单位" prop="unit">
          <el-input v-model="form.unit" placeholder="请输入计量单位，如：个、斤、件" />
        </el-form-item>
        
        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入商品描述"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm">发布商品</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { createProduct, uploadProductImage, getCategories } from '@/api/product'

const formRef = ref(null)
const categories = ref([])

const form = ref({
  name: '',
  category_id: '',
  image: '',
  price: 0,
  stock: 0,
  unit: '',
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  category_id: [
    { required: true, message: '请选择商品分类', trigger: 'change' }
  ],
  price: [
    { required: true, message: '请输入商品价格', trigger: 'blur' },
    { type: 'number', min: 0, message: '价格必须大于 0', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存数量', trigger: 'blur' },
    { type: 'number', min: 0, message: '库存必须大于等于 0', trigger: 'blur' }
  ],
  unit: [
    { required: true, message: '请输入计量单位', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入商品描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ]
}

// 获取商品分类列表
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    console.log('原始分类响应:', response) // 调试日志
    
    // 处理不同的响应格式
    if (Array.isArray(response)) {
      // 如果响应直接是数组
      categories.value = response
    } else if (response && typeof response === 'object') {
      if (Array.isArray(response.data)) {
        // 如果响应是 { data: [...] } 格式
        categories.value = response.data
      } else if (Array.isArray(response.results)) {
        // 如果响应是分页格式 { results: [...] }
        categories.value = response.results
      } else {
        // 尝试将对象的 values 转换为数组
        const values = Object.values(response)
        if (values.length > 0 && values.every(item => item && typeof item === 'object')) {
          categories.value = values
        } else {
          throw new Error('无法解析分类数据格式')
        }
      }
    } else {
      throw new Error('分类数据格式不正确')
    }
    
    // 确保分类数据包含必要的字段
    categories.value = categories.value.map(category => ({
      id: category.id || category.pk || category.value,
      name: category.name || category.label || '未命名分类'
    }))
    
    console.log('处理后的分类数据:', categories.value) // 调试日志
  } catch (error) {
    console.error('获取商品分类失败:', error)
    ElMessage.error('获取商品分类失败，使用默认分类')
    
    // 使用默认分类作为备选
    categories.value = [
      { id: 1, name: '其他' },
      { id: 2, name: '蔬菜' },
      { id: 3, name: '水果' },
      { id: 4, name: '肉蛋奶' },
      { id: 5, name: '粮食' }
    ]
  }
}

// 图片上传前的验证
const beforeImageUpload = (file) => {
  const isImage = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传 JPG 或 PNG 格式的图片！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

// 自定义上传方法
const handleImageUpload = async (options) => {
  try {
    const response = await uploadProductImage(options.file)
    console.log('上传响应:', response) // 调试日志
    
    if (response && response.url) {
      form.value.image = response.url
      ElMessage.success(response.message || '图片上传成功')
    } else {
      throw new Error('响应格式不正确')
    }
  } catch (error) {
    console.error('图片上传失败:', error)
    ElMessage.error('图片上传失败：' + (error.message || '未知错误'))
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 准备提交的数据
        const submitData = {
          name: form.value.name,
          category: form.value.category_id,
          price: form.value.price,
          stock: form.value.stock,
          unit: form.value.unit,
          description: form.value.description
        }
        
        const response = await createProduct(submitData)
        if (response) {
          ElMessage.success('商品发布成功')
          // 重置表单
          resetForm()
        } else {
          throw new Error('响应格式不正确')
        }
      } catch (error) {
        console.error('商品发布失败:', error)
        ElMessage.error('商品发布失败：' + (error.message || '未知错误'))
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.product-publish {
  padding: 20px;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.publish-form {
  margin-top: 20px;
}

.image-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
}

.image-uploader:hover {
  border-color: #409EFF;
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}

.image {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.image-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style> 