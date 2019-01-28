<template>
  <div class="ys-tag" v-bind:class="[size=='L' ? 'L' : '' ]">{{text}}</div>
</template>
<style scoped>
  .ys-tag{
    position:relative;
    background:rgba(74,146,255,0.4);
    background:linear-gradient(-135deg,transparent 5px,rgba(74,146,255,0.4) 0);
    border-top-left-radius:3px;
    border-bottom-right-radius:3px;
    border-bottom-left-radius:3px;
    height:22px;
    padding:0px 12px 0px 10px;
    display: inline-block;
    line-height:22px;
    font-size:12px;
  }
  .ys-tag:before{
    content:'';
    position:absolute;
    top:0px;
    right:0px;
    background:linear-gradient(to left bottom,transparent 50%,#4a92ff 0,#4a92ff) 100% 0 no-repeat;
    width:9px;
    height:9px;
    transform:translateY(0px) rotate(0deg);
    transform-origin:bottom right;
    border-bottom-left-radius:inherit;
    box-shadow:-.2em .2em .3em -.1em rgba(0,0,0,.15);
  }
  .ys-tag.L{
    position:relative;
    background:rgba(74,146,255,0.4);
    background:linear-gradient(-135deg,transparent 10px,rgba(74,146,255,0.4) 0);
    border-top-left-radius:3px;
    border-bottom-right-radius:3px;
    border-bottom-left-radius:3px;
    height:30px;
    padding:0px 20px 0px 15px;
    display: inline-block;
    line-height:30px;
    font-size:12px;
  }
  .ys-tag.L:before{
    content:'';
    position:absolute;
    top:-0.5px;
    right:-0.5px;
    background:linear-gradient(to left bottom,transparent 50%,#4a92ff 0,#4a92ff) 100% 0 no-repeat;
    width:16px;
    height:16px;
    transform:translateY(0px) rotate(0deg);
    transform-origin:bottom right;
    border-bottom-left-radius:inherit;
    box-shadow:-.2em .2em .3em -.1em rgba(0,0,0,.15);
  }
</style>
<script>
  export default {
    name: 'tag',
    props: {
      text: {
        default: ""
      },
      size: {
        default: ""
      },
    }
  }
</script>