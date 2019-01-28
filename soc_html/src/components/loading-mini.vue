<template>
  <span class="ys-loading" v-if="show">
    <img src="../assets/images/loading-text.png" style="width:14px;"/>
  </span>
</template>
<script>
  export default {
    name: 'loading-mini',
    props: {
      placement: {
        default: 'bottom'
      },
      show: {
        default: false
      },
    },
    data () {
      return {
        //visible:false
      };
    },
    methods: {
      handleShowPopper() {

      },
      handleClosePopper() {

      }
    }
  };
</script>
<style scoped>
  .ys-loading{
    display: inline-block;
    vertical-align: middle;
  }
  .ys-loading img{
    line-height:1;
    -webkit-animation:spin 1.5s linear infinite;
    -moz-animation:spin 1.5s linear infinite;
    animation:spin 1.5s linear infinite;
  }
  @-moz-keyframes spin { 100% { -moz-transform: rotate(360deg); } }
  @-webkit-keyframes spin { 100% { -webkit-transform: rotate(360deg); } }
  @keyframes spin { 100% { -webkit-transform: rotate(360deg); transform:rotate(360deg); } }

</style>