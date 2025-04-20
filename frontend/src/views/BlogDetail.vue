<template>
  <div class="blog-detail">
    <el-card class="blog-card">
      <template #header>
        <div class="blog-header">
          <h1>{{ blog.title }}</h1>
          <div class="blog-meta">
            <span class="publish-time">发布时间：{{ blog.publishTime }}</span>
            <span class="author">作者：{{ blog.author }}</span>
          </div>
        </div>
      </template>
      
      <div class="blog-content">
        <img :src="blog.image" :alt="blog.title" class="blog-image">
        <div class="content-text" v-html="blog.content"></div>
      </div>

      <div class="blog-footer">
        <el-button type="primary" @click="goBack">返回首页</el-button>
        <div class="share-buttons">
          <el-button type="info" plain>分享</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const blog = ref({
  id: '',
  title: '',
  publishTime: '',
  author: '',
  image: '',
  content: ''
})

onMounted(() => {
  // 这里应该根据路由参数获取博客详情
  // 模拟数据
  if(route.params.id == 1){
    blog.value = {
    id: route.params.id,
    title: '中央财政强农惠农富农政策清单发布',
    publishTime: '2025-03-21',
    author: '央视网',
    image: '/public/images/blog/blog1.png',
    content: `
      <p><b>央视网消息</b>（新闻联播）：近日，农业农村部发布2025年中央财政强农惠农富农政策清单，包括9项稳定实施的中央财政到人到户农业补贴政策。</p>
      <p>围绕着保护农民利益、调动种粮积极性，今年，继续实施耕地地力保护补贴，在东北地区实施玉米和大豆生产者补贴、在稻谷主产省实施稻谷补贴。农机购置与应用补贴对高性能播种机、智能高速插秧机等生产急需农机进行重点支持。小麦“一喷三防”补助支持主产区农民在小麦生产中后期喷施杀虫剂、植物生长调节剂等。农业社会化服务补助支持服务组织向农民在生产关键环节提供耕种等专业化服务。继续实施大豆玉米带状复合种植补助、耕地轮作休耕补助等补贴政策。农业保险保费补贴政策重点支持扩大稻谷、小麦、玉米、大豆完全成本保险和种植收入保险投保面积，发展特色农产品保险。</p>
    `
    }
  } else if(route.params.id == 2){
    blog.value = {
      id: route.params.id,
      title: '助力优质农产品“走出大山”',
      publishTime: '2025-01-16',
      author: '刘慧',
      image: '/public/images/blog/blog2.png',
      content: `
        <h2>453个贫困县1800多名参展商参加贫困地区农产品产销对接活动——助力优质农产品“走出大山”</h2>
        <p>发展产业是实现脱贫的根本之策。产业扶贫，产销对接的作用至关重要。6月26日，农业农村部在北京启动2018全国贫困地区农产品产销对接行动。专家表示，这有助于“以销促产”，推动贫困地区产业发展；也有助于让贫困地区“小而美”的特色农产品“走出大山”，丰富市民餐桌——时下，正是各类瓜果蔬菜集中上市的季节。由于受流通体系不完善、产销信息不对称、市场周期性波动等因素影响，贫困地区农产品仍然存在运不出、卖不掉、价不高等问题，各地在不同程度上还存在农产品卖难问题，一定程度上制约了农民增收和脱贫攻坚步伐。为贫困地区打开产品销路</p>
        <p>在“中国马铃薯良种之乡”甘肃渭源县展台前，小如拇指般大小的马铃薯种子十分吸引眼球。甘肃田地农业科技有限责任公司销售经理王建军告诉记者，他们公司主要从事马铃薯种薯繁育，销往四川、内蒙古、新疆、青海、贵州、山东、陕西等全国多个省份，年销售总额6800万元，是当地带动农民脱贫致富的农业产业化龙头企业。但是，由于公司地处偏僻，面临渠道资源不足的问题。他希望通过这次参展，提高公司知名度，吸引更多企业采购公司的产品。</p>
        <p>为了推动建立贫困地区农产品产销对接长效机制，农业农村部今年启动了全国贫困地区农产品产销对接行动，开展贫困地区农产品出村活动、农产品电商出村工程、爱心扶贫销售公益活动、特色农业品牌创建活动、农产品产地市场建设工程、贫困地区农产品产销对接宣传活动等6大活动。据了解，此次在北京举行的首场产销对接活动，以集中连片贫困地区尤其是深度贫困地区为主，展出优质特色农产品，产销双方参与踊跃，合作意愿非常强烈。截至目前，活动现场签约超过54亿元，总采购额达到127亿元，采购量约252.6万吨。</p>
        <p>提高农产品供给质量产销对接是实现农产品价值的关键环节，是推进产业扶贫、促进农民增收的重要举措。开展贫困地区农产品产销对接行动，有助于“以销促产”，推动贫困地区产业发展，让贫困群众有稳定的增收渠道；同时，也有助于让贫困地区“小而美”的特色农产品“走出大山”，丰富市民的餐桌，让消费者找到“小时候的味道”。</p>
        <p>在西藏那曲县展台前，西藏天牧牧业开发有限公司展出的牦牛肉、羊肉因其品质优良，很快就被预订一空。在云南怒江傈僳族自治州展台展出的醇香草果、美味野生菌、雪山竹叶菜，让人们不由得爱上高原美味。怒江州扶贫投资开发有限公司市场销售部经理王峰说，让高原美味走出怒江，走出云南，是建立产业扶贫助力脱贫攻坚的关键。希望通过此次参展让更多人爱上高原美味。</p>
        <p>在湖南省湘西土家族苗族自治州永顺县展台前，人们争相购买当地特色产品莓茶。湖南永顺县莓茶是一种集饮用、保健、医药于一身的纯天然绿色饮品，被称为“茶中回甘之王”。永顺县毛坝乡乡长彭岚告诉记者，永顺县是国家级贫困县，毛坝乡是国家级贫困乡，他们乡种植7000亩莓茶，此次参展的莓茶深受欢迎，展品被抢购一空。（记者 刘慧）</p>
      `
    }
  } else {
    blog.value = {
      id: route.params.id,
      title: '【政策解读】直播助农：乡村振兴的电商新模式',
      publishTime: '2025-02-17',
      author: '农产品推广中心',
      image: '/public/images/blog/blog3.png',
      content: `
        <h2>直播助农作为乡村振兴和网络扶贫深度融合发展的新兴产物，正在引领农村电商模式不断创新。</h2>
        <h4>直播助农的内涵</h4>
        <p>直播助农新模式是乡村发展的主体行动者，通过网络/电视直播平台、软件推销和销售农副产品的形式，并最终达到帮助农村脱贫和完成产业升级的一种手段。目前的直播平台包括传统电商平台开辟的直播功能，如京东直播、淘宝直播、拼多多直播等；也包括娱乐社交平台、功能软件平台开辟的直播购物功能，如抖音、快手、斗鱼、得到等。</p>
        <img src="/public/images/blog/blog3-2.png" alt="直播助农新模式" class="blog-image">
        <h4>直播助农新模式的链条效应</h4>
        <h5>01电子商务配套产业市场链</h5>
        <p>基于农村电商近年来的发展积淀，很多地区都建立了相对成熟的电子商务配套产业系统，融合直播这种新型的元素，推进农村电子商务模式上的创新。从销售端口产品的选品，到技术支撑、资金扶持以及最终的销售、售后等建立市场链条。由负责的企业及电商平台主导，配套产业市场完成整体运营过程，并从中实现管理和发展壮大等目的。在农村与大市场的对接、小生产与大市场的对接以及各种生产要素的流动和分配当中，起到协调作用，并且将农业的规模化经营提升到技术范围内。利用直播平台的流量效应提高农民以及贫困农户的基本收益，保障其权利的实现。同时，电子商务最为便捷地利用直播带货的红利，促进乡村振兴和网络脱贫的实现。</p>
        <h5>02个体农户直播销售新兴链</h5>
        <p>早在2018年，仅通过快手这一APP平台销售商品的用户中，就有115万人来自贫困县，全年销售额高达193亿元。从各种直播平台上成长起来的“野生网红”、个体农户主播，冲破原有地域圈层造成的生产制约，将农民形象包装打磨，连同农副产品一道形成大众认可的新型品牌。“直播/短视频+扶贫销售”助农的模式，得到了广泛的肯定，在全国各地的农村涌现出一批愿意带领乡亲脱贫的直播新网红。而农民新网红的出现只是一个缩影，在其背后所蕴藏的是农村对于直播助农以及电商平台发展潜力的运用。作为脱贫攻坚新力量的直播电商模式，在农村迅速落地开花，所形成的数字增长率不仅将农村巨大的内生驱动力发挥出来，更是广大农民群体对于发展自我、发展地区经济决心的展现。</p>
      `
    }
  }
})

const goBack = () => {
  router.push('/')
}
</script>

<style scoped>
.blog-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.blog-card {
  margin-bottom: 20px;
}

.blog-header {
  text-align: center;
}

.blog-header h1 {
  margin: 0;
  color: #303133;
  font-size: 28px;
}

.blog-meta {
  margin-top: 10px;
  color: #909399;
  font-size: 14px;
}

.blog-meta span {
  margin-right: 20px;
}

.blog-content {
  margin: 20px 0;
}

.blog-image {
  width: 100%;
  max-height: 500px;
  object-fit: cover;
  margin-bottom: 20px;
}

.content-text {
  line-height: 1.8;
  color: #606266;
}

.content-text :deep(p) {
  margin: 16px 0;
}

.content-text :deep(ul) {
  padding-left: 20px;
}

.blog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;
}

.share-buttons {
  display: flex;
  gap: 10px;
}
</style> 