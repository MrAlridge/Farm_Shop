<template>
  <main>
    <HomeCarousel />
    <HomeAboutUs />
  </main>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Home'
})

const store = useMainStore();

onMounted(async () => {
  if (store.items.length === 0) {
    await store.fetchProducts(); // 现在是异步的
  }
});
</script>