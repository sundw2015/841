<template>
  <div class="textC ys-info-color"
       v-bind:style="{width: width, height:height,lineHeight:height}">
    <div class="d-i-b verticalM">
      <p style="line-height:1"><i class="ys-icon icon-chart-no-data" style="margin-left:6px;color:rgba(154,188,238,0.25);font-size: 60px;"></i></p>
      <p style="line-height:1;color:rgba(154,188,238,0.7);" class="m-t-20">暂时没有数据</p>
    </div>
  </div>
</template>
<style scoped>

</style>
<script>
  export default {
    name:"noData",
    props: {
      width:{
        default: "100%"
      },
      height:{
        default: "200px"
      },
    },
    data() {
      return {

      }
    },
    ready(){

    },
    methods:{
    },
  }
</script>