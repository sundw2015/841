<template>
  <div v-show="showBtn" class="table-opt m-t-10" @click="show = !show" @blur="show = false" tabindex="0">
    <p class="ys-btn">
      <span class="m-r-3">操作</span>
      <i class="md font20" v-bind:class="[show ? 'md-arrow-drop-up' : 'md-arrow-drop-down' ]"></i>
    </p>
    <ul v-if="show">
      <slot></slot>
    </ul>
  </div>
</template>
<style>
.table-opt{
  display: inline-block;
  position: relative;
}
.table-opt p{
  padding:0px 10px!important;
}
.table-opt ul{
  background: rgba(0,0,0,0.4);
  color:#f2f2f2;
  position: absolute;
  top:30px;
  width:100px;
  border-radius: 3px;
}
.table-opt ul li{
  height:30px;
  line-height:30px;
  padding-left:10px;
  cursor: pointer;
}
.table-opt ul li:hover{
  color:#fff;
}
</style>
<script>
  export default {
    props: {
      show: {
        default: false
      },
      showBtn: {
        default: true
      }
    },
    data() {
      return {
      }
    },
  }

</script>