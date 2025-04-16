<template>
  <div class="poverty-info">
    <!-- 扶贫动态 -->
    <el-card class="news-card">
      <template #header>
        <div class="card-header">
          <span>扶贫动态</span>
        </div>
      </template>
      
      <el-timeline>
        <el-timeline-item
          v-for="(news, index) in povertyNews"
          :key="index"
          :timestamp="news.date"
          :type="news.type">
          <h4>{{ news.title }}</h4>
          <p>{{ news.content }}</p>
          <div v-if="news.images" class="news-images">
            <el-image
              v-for="(image, imgIndex) in news.images"
              :key="imgIndex"
              :src="image"
              :preview-src-list="news.images"
              class="news-image" />
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-card>
    
    <!-- 扶贫成果 -->
    <el-card class="achievements-card">
      <template #header>
        <div class="card-header">
          <span>扶贫成果</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8" v-for="achievement in achievements" :key="achievement.id">
          <el-card :body-style="{ padding: '0px' }" class="achievement-card">
            <img :src="achievement.image" class="achievement-image">
            <div class="achievement-info">
              <h3>{{ achievement.title }}</h3>
              <p>{{ achievement.description }}</p>
              <div class="achievement-stats">
                <div class="stat-item">
                  <span class="stat-label">帮扶人数</span>
                  <span class="stat-value">{{ achievement.helpedPeople }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">销售额</span>
                  <span class="stat-value">¥{{ achievement.sales }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 扶贫故事 -->
    <el-card class="stories-card">
      <template #header>
        <div class="card-header">
          <span>扶贫故事</span>
        </div>
      </template>
      
      <el-carousel :interval="4000" type="card" height="400px">
        <el-carousel-item v-for="story in stories" :key="story.id">
          <div class="story-content">
            <img :src="story.image" class="story-image">
            <div class="story-info">
              <h3>{{ story.title }}</h3>
              <p>{{ story.content }}</p>
              <div class="story-author">
                <el-avatar :size="40" :src="story.author.avatar" />
                <div class="author-info">
                  <span class="author-name">{{ story.author.name }}</span>
                  <span class="author-title">{{ story.author.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟扶贫动态数据
const povertyNews = ref([
  {
    date: '2024-04-01',
    type: 'success',
    title: '某村农产品成功上线平台',
    content: '经过多方努力，某村的特色农产品成功上线平台，为当地农民带来新的销售渠道。',
    images: ['/images/news/news1.jpg', '/images/news/news1_1.jpg']
  },
  {
    date: '2024-03-15',
    type: 'primary',
    title: '开展农产品种植技术培训',
    content: '平台组织专家团队前往贫困地区，为当地农民提供专业的种植技术培训。',
    images: ['/images/news/news2.jpg']
  },
  {
    date: '2024-03-01',
    type: 'warning',
    title: '平台新增10个扶贫产品',
    content: '平台新增10个来自贫困地区的特色农产品，进一步扩大扶贫范围。'
  }
])

// 模拟扶贫成果数据
const achievements = ref([
  {
    id: 1,
    title: '某村特色农产品销售',
    description: '帮助某村销售特色农产品，带动当地经济发展。',
    image: '/images/achievements/achievement1.jpg',
    helpedPeople: 50,
    sales: 100000
  },
  {
    id: 2,
    title: '技术培训项目',
    description: '开展农业技术培训，提升农民种植技能。',
    image: '/images/achievements/achievement2.jpg',
    helpedPeople: 100,
    sales: 0
  },
  {
    id: 3,
    title: '电商扶贫项目',
    description: '通过电商平台帮助贫困地区销售农产品。',
    image: '/images/achievements/achievement3.jpg',
    helpedPeople: 200,
    sales: 500000
  }
])

// 模拟扶贫故事数据
const stories = ref([
  {
    id: 1,
    title: '从贫困户到致富带头人',
    content: '通过平台销售农产品，张先生不仅自己脱贫，还带动了周边村民共同致富。',
    image: '/images/stories/story1.jpg',
    author: {
      name: '张先生',
      title: '致富带头人',
      avatar: '/images/avatars/avatar1.jpg'
    }
  },
  {
    id: 2,
    title: '返乡创业的年轻人',
    content: '李女士放弃城市工作，回乡创业，通过平台销售家乡特产，实现人生价值。',
    image: '/images/stories/story2.jpg',
    author: {
      name: '李女士',
      title: '返乡创业者',
      avatar: '/images/avatars/avatar2.jpg'
    }
  }
])
</script>

<style scoped>
.poverty-info {
  padding: 20px;
}

.news-card, .achievements-card, .stories-card {
  margin-bottom: 30px;
}

.news-images {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.news-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
}

.achievement-card {
  margin-bottom: 20px;
}

.achievement-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.achievement-info {
  padding: 14px;
}

.achievement-info h3 {
  margin: 0 0 10px 0;
}

.achievement-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  color: #909399;
  font-size: 14px;
}

.stat-value {
  display: block;
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
  margin-top: 5px;
}

.story-content {
  display: flex;
  height: 100%;
}

.story-image {
  width: 50%;
  height: 100%;
  object-fit: cover;
}

.story-info {
  width: 50%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.story-info h3 {
  margin: 0 0 10px 0;
}

.story-author {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.author-info {
  margin-left: 10px;
}

.author-name {
  display: block;
  font-weight: bold;
}

.author-title {
  display: block;
  color: #909399;
  font-size: 14px;
}
</style> 