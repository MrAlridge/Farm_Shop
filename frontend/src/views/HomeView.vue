<template>
    <div>
      <h1>扶贫助农平台</h1>
      <div v-if="products.length">
         <h2>产品列表</h2>
          <ul>
          <li v-for="product in products" :key="product.id">
              {{ product.name }} - ￥{{ product.price }}
              <img v-if="product.image" :src="product.image" alt="Product Image" width="100">
               <button @click="addToCart(product)">加入购物车</button>
          </li>
      </ul>
      </div>
      </div>
  </template>
  
  <script>
  /* eslint-disable */
  import api from '@/api'; //引入Axios实例
  
  export default {
      data() {
          return {
             products: []
          };
      },
       async created() {
          // 获取产品数据
          try{
              const response = await api.get('/products/products/');
              this.products = response.data.results; //根据Django REST Framework的分页
               console.log(this.products);
          }
          catch(error){
              console.error("获取产品失败",error);
          }
  
      },
      methods:{
        async addToCart(product){
          //1. 如果购物车已经有了该物品，则增加数量
          //2. 否则，添加新的购物车物品
          //调用后端的Order接口
            try {
              const response = await api.post('/orders/orders/', {
                shipping_address: "默认地址", //应该从用户信息获取
                contact_phone: "123454321",
                receiver_name: "默认用户",
                items:[
                  {
                        product_id : product.id,
                        quantity : 1
                  }
                ]
              });
              alert("成功加入购物车")
              this.$router.push('/orders') //跳转到/orders路由
            } catch (error) {
                if (error.response ) {
                  if(error.response.status === 400){
                    if(error.response.data && error.response.data.items && error.response.data.items[0].product_id){
                      alert(error.response.data.items[0].product_id[0]);
                    }
                    else{
                        alert('加入购物车失败，请稍后重试');
                    }
  
                }
                  else{
                     alert(error.response.statusText);
                  }
                } else {
                // 处理没有响应的错误（例如网络错误）
                alert= '无法连接到服务器';
               }
            }
        }
      }
  };
  </script>