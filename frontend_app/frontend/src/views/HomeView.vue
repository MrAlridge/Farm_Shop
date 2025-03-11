<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <h1>欢迎来到扶贫助农管理系统</h1>
    <ProductList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ProductList from '@/components/ProductList.vue';

export default defineComponent({
  name: 'HomeView',
  components: {
    ProductList,
  },
});
</script>
