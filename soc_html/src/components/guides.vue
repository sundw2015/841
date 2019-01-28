<template>
  <div class="ys-guide-box">
    <div class="guide-title"
         v-for="list in step"
         v-bind:class="[cur < list.step ? 'title40' : 'title100' ,cur == list.step && cur != step.length ? 'on' : '',cur+1 == list.step ? 'm-t-100' : '' ]">
      <span class="num" v-bind:class="[cur == list.step ? 'on' : '' ]">
        <span v-if="list.step!=step.length">{{list.step}}</span>
        <span v-else><i class="ys-icon icon-ok font14"></i></span>
      </span>
      <div class="text" v-if="cur >= list.step">
        <span v-if="cur > list.step" class="ys-info-color">{{list.after}}</span>
        <span v-else v-bind:class="[cur == list.step ? 'ys-success-color' : '' ]">{{list.before}}</span>
        <span v-if="cur > list.step" class="done bounceIn animated"><i class="ys-icon icon-ok ys-success-color"></i></span>
      </div>
    </div>
    <div class="guide-con ys-box-con" v-bind:style="{top: (cur * 40 + 5 * (cur-1) ) + 'px' }">
      <slot name="content"></slot>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'guides',
    props: {
      cur: {
        type:Number,
        default:1
      },
      step: {
        type:Array
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
    ready:function(){}
  }
</script>
<style scoped>
  .m-t-100{
    margin-top:100px;
    transition: margin-top 0.8s;
  }
  .ys-guide-box{
    position:relative;
    margin-bottom:8px;
    min-height:1000px;
  }
  .guide-title{
    position:relative;
    background:rgba(0,0,0,0.25);
    border-radius:25px;
    height:40px;
    line-height:40px;
    margin-bottom:5px;
  }
  .guide-title.on{
    box-shadow: 1px 2px 2px rgba(0,0,0,0.2);
  }
  .title40{
    width:40px;
  }
  .title100{
    width:100%;
    transition: width 1s;
  }
  .guide-title .text{
    padding-left:47px;
  }
  .guide-title .text .done{
    margin-right:16px;
    float:right;
  }
  .guide-title.on:before{
    content:'';
    height:107px;
    width:2px;
    background:rgba(0,0,0,0.15);
    position:absolute;
    top:30px;
    left:19px;
    z-index:-1;
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
    right:50px;
  }
  .guide-title .num.on{
    background: linear-gradient(to bottom, #00bd85, #00a071);
  }
  .guide-con{
    position: absolute;
    left:47px;
    top:40px;
    right:20px;
    min-height:683px;
    transition: top 0.5s;
  }
  .guide-con.on{
    height:auto;
    min-height:72px;
  }
  .guide-con-info{
    padding:16px 30px;
  }
</style>