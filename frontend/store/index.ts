import { defineStore } from "pinia";
import { State, Product } from '@/components/types';
import { fetchProducts, fetchProductDetails } from '~/composables/api'; // 导入 API 请求

export const useMainStore = defineStore("main", {
  state: (): State => ({
    productInfo: {} as Product,
    cartItems: [],
    items: [],
    loading: false,
  }),
  getters: {
    itemsNumber: (state): number => state.cartItems.length,
    totalPrice: (state): number => {
      return state.cartItems.reduce((total, item) => total + (item.price || 0), 0);
    },
 //  添加 relatedItems getter。
    relatedItems: (state): Product[] => {
        const related: Product[] = [];
        //从items中随机获取三个不重复的商品
          while (related.length < 3) {
            const randomIndex = Math.floor(Math.random() * state.items.length);
            const randomItem = state.items[randomIndex];
            // 检查是否已经存在,并且id不等于当前商品
            if (!related.some(item=> item.id == randomItem.id) && randomItem.id != state.productInfo.id ) {
                related.push(randomItem);
            }
          }
          return related;
    }
  },
  actions: {
    async fetchProducts() {
      try {
        this.items = await fetchProducts(); // 使用 API 调用
      } catch (error) {
        // 错误已经在 api.ts 中处理，这里可以显示一个全局的错误消息
        console.error("Failed to fetch products");
      } finally {
        this.loading = false; // 加载结束 (无论成功还是失败)
      }
    },
     async  fetchProductDetails(id:number){
        try{
            const product = await fetchProductDetails(id);
            this.productInfo = product;
        }catch(error){
            console.error(`获取id为${id}的商品详情失败`)
        }
    },
    inCart(product: Product) {
      this.cartItems.push(product);
    },
    outCart(id: number) {
      this.cartItems = this.cartItems.filter((item) => item.id !== id);
    },
      // addtoInfo 方法不再需要，直接通过fetchProductDetails获取信息
    // addtoInfo(id: number) {
    //  const selectedProduct = this.items.find((item) => item.id === id);
    //  if (selectedProduct) {
    //    this.productInfo = selectedProduct;
    // }
    //},
  },
});