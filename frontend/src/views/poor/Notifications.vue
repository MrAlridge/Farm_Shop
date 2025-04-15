<template>
  <div class="notifications-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>消息通知</span>
          <el-button type="primary" @click="markAllAsRead" :disabled="!unreadCount">
            全部标记为已读
          </el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab" class="notifications-tabs">
        <!-- 全部消息 -->
        <el-tab-pane label="全部消息" name="all">
          <el-timeline>
            <el-timeline-item
              v-for="notification in allNotifications"
              :key="notification.id"
              :type="getNotificationType(notification.type)"
              :timestamp="notification.createTime"
              placement="top"
            >
              <el-card class="notification-card" :class="{ 'unread': !notification.isRead }">
                <div class="notification-content">
                  <div class="notification-header">
                    <span class="title">{{ notification.title }}</span>
                    <el-tag size="small" :type="getNotificationType(notification.type)">
                      {{ getNotificationTypeText(notification.type) }}
                    </el-tag>
                  </div>
                  <div class="notification-body">
                    {{ notification.content }}
                  </div>
                  <div class="notification-footer">
                    <el-button
                      v-if="!notification.isRead"
                      type="primary"
                      size="small"
                      @click="markAsRead(notification)"
                    >
                      标记为已读
                    </el-button>
                    <el-button
                      v-if="notification.actionUrl"
                      type="primary"
                      size="small"
                      @click="handleAction(notification)"
                    >
                      查看详情
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-tab-pane>

        <!-- 未读消息 -->
        <el-tab-pane label="未读消息" name="unread">
          <el-timeline>
            <el-timeline-item
              v-for="notification in unreadNotifications"
              :key="notification.id"
              :type="getNotificationType(notification.type)"
              :timestamp="notification.createTime"
              placement="top"
            >
              <el-card class="notification-card">
                <div class="notification-content">
                  <div class="notification-header">
                    <span class="title">{{ notification.title }}</span>
                    <el-tag size="small" :type="getNotificationType(notification.type)">
                      {{ getNotificationTypeText(notification.type) }}
                    </el-tag>
                  </div>
                  <div class="notification-body">
                    {{ notification.content }}
                  </div>
                  <div class="notification-footer">
                    <el-button
                      type="primary"
                      size="small"
                      @click="markAsRead(notification)"
                    >
                      标记为已读
                    </el-button>
                    <el-button
                      v-if="notification.actionUrl"
                      type="primary"
                      size="small"
                      @click="handleAction(notification)"
                    >
                      查看详情
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-tab-pane>

        <!-- 已读消息 -->
        <el-tab-pane label="已读消息" name="read">
          <el-timeline>
            <el-timeline-item
              v-for="notification in readNotifications"
              :key="notification.id"
              :type="getNotificationType(notification.type)"
              :timestamp="notification.createTime"
              placement="top"
            >
              <el-card class="notification-card">
                <div class="notification-content">
                  <div class="notification-header">
                    <span class="title">{{ notification.title }}</span>
                    <el-tag size="small" :type="getNotificationType(notification.type)">
                      {{ getNotificationTypeText(notification.type) }}
                    </el-tag>
                  </div>
                  <div class="notification-body">
                    {{ notification.content }}
                  </div>
                  <div class="notification-footer">
                    <el-button
                      v-if="notification.actionUrl"
                      type="primary"
                      size="small"
                      @click="handleAction(notification)"
                    >
                      查看详情
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePoorStore } from '@/store/modules/poor'
import { ElMessage } from 'element-plus'

const router = useRouter()
const poorStore = usePoorStore()
const activeTab = ref('all')
const notifications = ref([])

// 计算属性
const unreadNotifications = computed(() => {
  return notifications.value.filter(n => !n.isRead)
})

const readNotifications = computed(() => {
  return notifications.value.filter(n => n.isRead)
})

const unreadCount = computed(() => {
  return unreadNotifications.value.length
})

// 获取通知类型
const getNotificationType = (type) => {
  const typeMap = {
    'system': 'info',
    'project': 'success',
    'material': 'warning',
    'education': 'primary'
  }
  return typeMap[type] || 'info'
}

// 获取通知类型文本
const getNotificationTypeText = (type) => {
  const typeMap = {
    'system': '系统通知',
    'project': '帮扶项目',
    'material': '物资援助',
    'education': '教育资助'
  }
  return typeMap[type] || type
}

// 标记为已读
const markAsRead = async (notification) => {
  try {
    await poorStore.markNotificationAsRead(notification.id)
    notification.isRead = true
    ElMessage.success('已标记为已读')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 标记全部为已读
const markAllAsRead = async () => {
  try {
    await poorStore.markAllNotificationsAsRead()
    notifications.value.forEach(n => n.isRead = true)
    ElMessage.success('已全部标记为已读')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 处理通知动作
const handleAction = (notification) => {
  if (notification.actionUrl) {
    router.push(notification.actionUrl)
  }
}

// 获取通知列表
const fetchNotifications = async () => {
  try {
    const res = await poorStore.getNotifications()
    notifications.value = res.data
  } catch (error) {
    ElMessage.error('获取通知失败')
  }
}

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped>
.notifications-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notifications-tabs {
  margin-top: 20px;
}

.notification-card {
  margin-bottom: 10px;
}

.notification-card.unread {
  background-color: var(--el-color-primary-light-9);
}

.notification-content {
  padding: 10px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.notification-header .title {
  font-weight: bold;
  font-size: 16px;
}

.notification-body {
  margin-bottom: 10px;
  color: var(--text-color-regular);
}

.notification-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-card__header) {
  padding: 10px 20px;
}

:deep(.el-card__body) {
  padding: 20px;
}

:deep(.el-timeline-item__node) {
  background-color: var(--el-color-primary);
}
</style> 