<template>
  <div class="ys-step-box">
    <div class="step-title">
      <span class="num">{{step}}</span>
      <div class="title">
        <div class="right"></div>
        <div class="left"></div>
        <div class="con ys-success-color">{{title}}</div>
      </div>
    </div>
    <div class="step-con">
      <slot></slot>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'step-all',
    props: {
      step: {
        type:Number
      },
      title: {
        type: String,
        default: ''
      },
    },
    ready:function(){

    }
  }
</script>
<style scoped>
  .ys-step-box{
    position:relative;
  }
  .step-title{
    position:relative;
  }
  .step-title .title{
    position:relative;
  }
  .step-title .title .con{
    height:26px;
    line-height:24px;
    background:rgba(0,189,133,0.05);
    border-top:1px solid rgba(0,189,133,0.15);
    border-bottom:1px solid rgba(0,189,133,0.15);
    margin-left:42px;
    margin-right:15px;
  }
  .step-title .title .left{
    background:url(../assets/images/step-title-left.png);
    width:18px;
    height:26px;
    position:absolute;
    left:24px;
    top:0px;
  }
  .step-title .title .right{
    background:url(../assets/images/step-title-right.png);
    width:15px;
    height:26px;
    position:absolute;
    right:0px;
    top:0px;
  }
  .step-title .num{
    position:absolute;
    width:32px;
    height:32px;
    text-align:center;
    line-height:27px;
    font-size:18px;
    left:0px;
    top:-3px;
    background:none;
    border:3px solid #00bd85;
    border-radius: 50%;
    color:#00bd85;
    box-shadow: 1px 1px 6px 1px rgba(0,0,0,.2) inset, 2px 2px 8px 1px rgba(0,0,0,0.2);
  }
  .step-box{
    padding-left:30px;
    padding-bottom:60px
  }
  .step-con{
    border-left:1px dashed rgba(0,189,133,0.4);
    padding:16px 24px;
    margin-left:16px;
  }
</style>