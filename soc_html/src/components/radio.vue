<template>
  <div class="ys-checkbox-box">
    <span class="ys-checkbox"
          v-for="radio in list"
          @click="setRadio(radio)"
          v-bind:class="[radio.id==value ? 'on' : '', radio.disabled ? 'disabled' : '' ]">
      <span class="check"></span>
      <span class="verticalM m-l-5" v-bind:class="[radio.id==value ? '' : 'ys-info-color' ]">{{radio.text}}</span>
    </span>
  </div>
</template>
<script>
  export default {
    name: 'radio',
    props: {
      list: {
        type: Array,
        default: []
      },
      value: {
        default: '',
        twoWay: true
      }
    },
    data () {
      return {
        curId: 0,
      }
    },
    ready:function(){

    },
    watch: {
    },
    methods: {
      setRadio (radio) {
        if(!radio.disabled){
          this.value = radio.id
        }
      }
    }
  }
</script>

<style scoped>
  .ys-checkbox-box{
    display: inline-block;
  }
  .ys-checkbox{
   display: inline-block;
   cursor:pointer;
   line-height:18px;
   margin-right:20px;
  }
  .ys-checkbox .check{
   display: inline-block;
   width:12px;
   height:12px;
   border:1px solid #5373b1;
   border-radius: 50%;
   vertical-align: middle;
   white-space: nowrap;
   cursor: pointer;
   outline: 0;
   position: relative;
  }
  .ys-checkbox.on .check:before{
    content:"";
    position: absolute;
    width:6px;
    height:6px;
    border-radius: 50%;
    left:2px;
    top:2px;
    background: #4a92ff;
    transform: scale(1);
    transition: all .2s ease-in-out;
  }
  .ys-checkbox.on .check{
    border:1px solid #4a92ff;
    transition: all .1s ease-in-out;
  }
</style>