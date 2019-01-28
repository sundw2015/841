<template>
  <span class="ys-switch-tab" @click="toggle" :class="[disabled ? 'disabled' : '']">
    <span class="ys-switch-tab-inner"
          v-bind:class="[checked==list[0].id ? 'on' : '']">{{list[0].name}}</span>
    <span class="ys-switch-tab-inner"
          v-bind:class="[checked==list[1].id ? 'on' : '']">{{list[1].name}}</span>
  </span>
</template>
<script>
  export default {
    name: 'ys-switch-tab',
    props: {
      checked: {
        default: ""
      },
      list:{
        default: []
      },
      disabled:{
        default: false
      }
    },
    computed: {
      innerClasses () {
        return '';
      }
    },
    methods: {
      toggle () {
        if(this.disabled){
          return false
        }
//        if(this.checked==this.list[0].id){
//          this.checked=this.list[1].id
//        }else{
//          this.checked=this.list[0].id
//        }
        this.$emit('on-change', this.checked);
        this.$dispatch('on-form-change', this.checked);
        this.$dispatch('change', this.checked);
      }
    }
  };
</script>
<style scoped>
  .ys-switch-tab-inner{
    padding:0px 6px;
    display: inline-block;
  }
  .ys-switch-tab-inner.on{
    background:#4a92ff;
    color:#fff;
    transition: all .2s ease-in-out;
  }
  .ys-switch-tab {
    height: 26px;
    line-height: 24px;
    border-radius: 3px;
    border: 1px solid #7395ca;
    color:#7e9fd0;
    position: relative;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    transition: all .2s ease-in-out;
    display: inline-block;
  }
</style>