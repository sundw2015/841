<template>
  <span class="ys-tab-box">
    <span v-for="item in list" class="ys-tab-item"
    v-bind:class="[checked==item.id ? 'on' : '']"
    @click="selectOption(item.id)">{{item.name}}</span>
  </span>
</template>
<script>
  export default {
    name: 'ys-tab',
    props: {
      disabled: {
        type: Boolean,
        default: false
      },
      size: {
        default:"large",
      },
      list:{
        default: []
      },
      checked:{
        default: ""
      }
    },
    ready: function() {
      
    },
    methods: {
      selectOption(id){
        this.checked=id;
        this.$dispatch('change', this.checked);
      }
    }
  };
</script>
<style scoped>
.ys-tab-box{
  display: inline-block;
  background:rgba(0,0,0,0.3);
  height:26px;
  line-height:22px;
  padding:2px;
  border-radius: 3px;
  color:#93a6d8;
}
.ys-tab-item{
  cursor: pointer;
  display: inline-block;
  padding:0px 14px;
}
.ys-tab-item.on{
  background:#4a92ff;
  color:#fff;
  border-radius: 3px;
}
</style>