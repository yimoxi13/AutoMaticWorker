<script>
export default {
  data() {
    return {
      message: ""
    };
  },
  mounted() {
    // 使用axios发送请求到后端获取数据
    this.$axios.get("http://localhost:5000/api/data")
    .then(response => {
        this.message = response.data.message;
      })
    .catch(error => {
        console.error("Error fetching data:", error);
      });
  }
};
</script>

<template>
  <div>
    <h1>Vue + Flask + Pywebview Example</h1>
    <p>{{ message }}</p>
    <h5>可选流程: </h5>
    1.<button>流程一</button>
  </div>
</template>

<style>
/* 可以添加一些样式规则，这里暂未详细设置 */
</style>