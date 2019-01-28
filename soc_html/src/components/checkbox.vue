<template>
  <span class="ys-checkbox" v-bind:class="[show ? 'on' : '' ]" @click="selfClick()">
    <span class="check">
      <i class="ys-icon icon-check" v-if="show"></i>
    </span>
    <span class="verticalM m-l-5 ys-info-color" v-if="text!=''">{{text}}</span>
  </span>
</template>
<script>
  export default {
    name: 'checkbox',
    props: {
      show: {
        require: true,
        default:false
      },
      text:{
        default:""
      },
      // 由组件控制开关， 默认为是， 否则有上层控制
      autoSet: {
        default: true
      },
      read:{
        default: false
      },
    },
    ready:function(){

    },
    watch: {
      show(val) {

      }
    },
    methods: {
      selfClick () {
        if(this.read){return false}
        if (this.autoSet) {
          this.show = !this.show
        }
        this.$dispatch('ys-click', this.show)
      },
      close() {
        this.show = false
      }
    }
  }
</script>

<style scoped>
  .ys-checkbox{
    display: inline-block;
    cursor:pointer;
    line-height:2px;
  }
  .ys-checkbox .check{
    display: inline-block;
    width:12px;
    height:12px;
    border:1px solid #5373b1;
    border-radius: 2px;
    vertical-align: middle;
    white-space: nowrap;
    cursor: pointer;
    outline: 0;
    position: relative;
  }
  .ys-checkbox .check i{
    position: absolute;
    left:-1px;
    top:-1px;
    color:#fff!important;
  }
  .ys-checkbox.on .check{
    border:1px solid #4a92ff;
    background:#4a92ff;
    transition: all .2s ease-in-out;
  }
</style>