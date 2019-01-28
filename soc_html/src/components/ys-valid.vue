<template>
  <div class="ys-valid">
    <div style="line-height:0px;">
      <slot></slot>
    </div>
    <div class="ys-valid-popper ys-error-color"
         v-el:popper
         transition="fade">
      <slot name="content" class="content"></slot>
    </div>
  </div>
</template>
<style scoped>
  .ys-valid{
    position:relative;
    text-align:left!important;
  }
  .ys-valid-popper{
    display: block;
    font-size: 12px;
    position: absolute;
    visibility: visible;
    line-height: 1.5;
    z-index: 1060;
    bottom:-17px;
    width: 100%;
  }
  .content p{white-space: nowrap;}
  .fade-transition {
    display: inline-block; /* 否则 scale 动画不起作用 */
  }
  .fade-enter {
    animation: ysFadeIn .3s;
  }
  .fade-leave {
    animation: ysFadeOut .3s;
  }
  @keyframes ysFadeIn {
    0% {
      opacity: 0
    }

    100% {
      opacity: 1
    }
  }
  @-webkit-keyframes ysFadeIn {
    0% {
      opacity: 0
    }

    100% {
      opacity: 1
    }
  }
  @keyframes ysFadeOut {
    0% {
      opacity: 1
    }

    100% {
      opacity: 0
    }
  }
  @-webkit-keyframes ysFadeOut {
    0% {
      opacity: 1
    }

    100% {
      opacity: 0
    }
  }
</style>
<script>
  export default {
    name: 'ys-valid',
  }
</script>