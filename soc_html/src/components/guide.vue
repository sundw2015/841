<template>
  <div class="ys-guide-box">
    <div class="guide-title">
      <span class="num" v-bind:class="[cur == step ? 'on' : '' ]">
        <span v-if="!final">{{step}}</span>
        <span v-else><i class="ys-icon icon-ok font14"></i></span>
      </span>
      <div class="text">
        <span v-if="cur > step">{{done}}</span>
        <span v-else>{{title}}</span>
        <span v-if="cur > step" class="done"><i class="ys-icon icon-ok ys-success-color"></i></span>
      </div>
    </div>
    <div class="guide-con" v-bind:class="[cur == step ? 'on' : '' ]">
      <div class="guide-con-info">
        <slot v-show="cur == step"></slot>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'guide',
    props: {
      cur: {
        type:Number
      },
      step: {
        type:Number
      },
      title: {
        type: String,
        default: ''
      },
      done: {
        type: String,
        default: ''
      },
      final: {
        default: false
      },
    },
    ready:function(){

    }
  }
</script>
<style scoped>
  .ys-guide-box{
    position:relative;
    padding-left:16px;
    margin-bottom:8px;
  }
  .guide-title{
    position:relative;
    background:rgba(0,0,0,0.25);
    border-radius:25px;
    height:40px;
    line-height:40px;
  }
  .guide-title .text{
    padding-left:50px;
  }
  .guide-title .text .done{
    margin-right:16px;
    float:right;
  }
  .guide-title .num{
    position:absolute;
    width:32px;
    height:32px;
    text-align:center;
    line-height:32px;
    font-size:18px;
    left:4px;
    top:4px;
    border-radius: 50%;
    color:#fff;
  }
  .guide-title .num.on{
    background: linear-gradient(to bottom, #00bd85, #00a071);
  }
  .guide-con{
    height:0px;
    min-height:0px;
    overflow: hidden;
    background:rgba(0,0,0,0.15);
    transition-property: min-height, height, scroll;
    transition-duration: 1000ms;
    margin-left:50px;
    margin-right:50px;
  }
  .guide-con.on{
    height:auto;
    min-height:72px;
  }
  .guide-con-info{
    padding:16px 30px;
  }
</style>