<template >
  <div class="container py-5" style="padding-top:70px;">
    <DetailsBreadcrumb :details="store.productInfo" />
    <DetailsBox :item="store.productInfo" />
    <DetailsText />

    <div class="related-item">
      <hr>
      <h6 class="pb-4">RELATED PRODUCTS</h6>
      <ClientOnly>
        <ProductsCard :cards="store.relatedItems" />
      </ClientOnly>
    </div>

  </div>
</template>

<script setup lang="ts">
const store = useMainStore()
const route = useRoute()

onMounted(async () => {
  let itemId = Number(route.params.id)
  //获取商品详情
  await store.fetchProductDetails(itemId)
})

</script>

<style scoped>
hr {
  width: 50px;
  border-bottom: 1px solid black;
}

.related-item {
  padding-left: 8rem;
  padding-right: 8rem;
  height: auto;
  text-align: center;
}
</style>
