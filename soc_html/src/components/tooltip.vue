<template>
  <div class="ys-tooltip" @mouseenter="handleShowPopper" @mouseleave="handleClosePopper">
    <!--@mouseleave="handleClosePopper"-->
    <div v-el:reference>
      <slot></slot>
    </div>
    <div class="ys-tooltip-popper"
         v-el:popper
         v-show="!disabled && visible"
         transition="fade">
      <div class="ys-tooltip-content">
        <div class="ys-tooltip-arrow"></div>
        <div class="ys-tooltip-inner">
          <slot name="content"><span>{{ content }}</span></slot>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import Popper from 'src/directives/popper';
  export default {
    name: 'tooltip',
    mixins: [Popper],
    props: {
      placement: {
        default: 'top'
      },
      content: {
        type: [String, Number],
        default: ''
      },
      delay: {
        type: Number,
        default: 0
      },
      disabled: {
        type: Boolean,
        default: false
      },
      controlled: {    // under this prop,Tooltip will not close when mouseleave
        type: Boolean,
        default: false
      }
    },
    data () {
      return {
        //visible:false
      };
    },
    methods: {
      handleShowPopper() {
        let self=this;
        self.timeout = setTimeout(function(){
          self.visible = true;
        },self.delay)
      },
      handleClosePopper() {
        clearTimeout(this.timeout);
        if (!this.controlled) {
          this.visible = false;
        }
      }
    }
  };
</script>
<style scoped>
  .ys-tooltip{
    display: inline-block;
    position:relative;
    line-height:1;
  }
  .ys-tooltip-popper{
    display: block;
    font-size: 12px;
    position: absolute;
    visibility: visible;
    line-height: 1.5;
    z-index: 1060;
  }
  .ys-tooltip-popper[x-placement^=top] {
    padding: 5px 0 8px
  }

  .ys-tooltip-popper[x-placement^=right] {
    padding: 0 5px 0 8px
  }

  .ys-tooltip-popper[x-placement^=bottom] {
    padding: 8px 0 5px
  }

  .ys-tooltip-popper[x-placement^=left] {
    padding: 0 8px 0 5px
  }

  .ys-tooltip-popper[x-placement^=top] .ys-tooltip-arrow {
    bottom: 3px;
    border-width: 5px 5px 0;
    border-top-color: rgba(0,0,0,.9);
  }

  .ys-tooltip-popper[x-placement=right-end] .ys-tooltip-arrow,.ys-tooltip-popper[x-placement=left-end] .ys-tooltip-arrow {
    bottom: 8px
  }

  .ys-tooltip-popper[x-placement=top] .ys-tooltip-arrow {
    left: 50%;
    margin-left: -5px
  }

  .ys-tooltip-popper[x-placement=top-start] .ys-tooltip-arrow {
    left: 16px
  }

  .ys-tooltip-popper[x-placement=top-end] .ys-tooltip-arrow {
    right: 16px
  }

  .ys-tooltip-popper[x-placement^=right] .ys-tooltip-arrow {
    left: 3px;
    border-width: 5px 5px 5px 0;
    border-right-color: rgba(0,0,0,.9);
  }

  .ys-tooltip-popper[x-placement=right] .ys-tooltip-arrow {
    top: 50%;
    margin-top: -5px
  }

  .ys-tooltip-popper[x-placement=right-start] .ys-tooltip-arrow {
    top: 8px
  }

  .ys-tooltip-popper[x-placement^=left] .ys-tooltip-arrow {
    right: 3px;
    border-width: 5px 0 5px 5px;
    border-left-color: rgba(0,0,0,.9);
  }

  .ys-tooltip-popper[x-placement=left] .ys-tooltip-arrow {
    top: 50%;
    margin-top: -5px
  }

  .ys-tooltip-popper[x-placement=left-start] .ys-tooltip-arrow {
    top: 8px
  }

  .ys-tooltip-popper[x-placement^=bottom] .ys-tooltip-arrow {
    top: 3px;
    border-width: 0 5px 5px;
    border-bottom-color: rgba(0,0,0,.9);
  }

  .ys-tooltip-popper[x-placement=bottom] .ys-tooltip-arrow {
    left: 50%;
    margin-left: -5px
  }

  .ys-tooltip-popper[x-placement=bottom-start] .ys-tooltip-arrow {
    left: 16px
  }

  .ys-tooltip-popper[x-placement=bottom-end] .ys-tooltip-arrow {
    right: 16px
  }
  .ys-tooltip-arrow {
    position: absolute;
    width: 0;
    height: 0;
    border-color: transparent;
    border-style: solid;
  }
  .ys-tooltip-arrow:after{
    content: '';
    width: 8px;
    height: 8px;
    overflow: hidden;
    zoom: 1;
    position: absolute;
    border-right: 1px solid rgba(74,146,255,0.5);
    border-bottom: 1px solid rgba(74,146,255,0.5);
    background-color: #161a2f;
  }
  .ys-tooltip-popper[x-placement=bottom] .ys-tooltip-arrow:after{
    top: 1px;
    left: -4px;
    transform: rotate(225deg);
    -o-transform: rotate(225deg);
    -moz-transform: rotate(225deg);
    -webkit-transform: rotate(225deg);
  }
  .ys-tooltip-popper[x-placement=top] .ys-tooltip-arrow:after{
    top:-9px;
    left: 50%;
    margin-left: -4px;
    transform: rotate(45deg);
    -o-transform: rotate(45deg);
    -moz-transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
  }
  .ys-tooltip-popper[x-placement=left] .ys-tooltip-arrow:after{
    top:-4px;
    left:-9px;
    transform: rotate(-45deg);
    -o-transform: rotate(-45deg);
    -moz-transform: rotate(-45deg);
    -webkit-transform: rotate(-45deg);
  }
  .ys-tooltip-popper[x-placement=right] .ys-tooltip-arrow:after{
    top: -4px;
    left: 1px;
    transform: rotate(135deg);
    -o-transform: rotate(135deg);
    -moz-transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
  }
  .ys-tooltip-inner {
    padding: 2px 6px;
    color: #fff;
    text-align: left;
    background: #161a2f;
    border-radius: 3px;
    white-space:nowrap;
    border:1px solid rgba(74,146,255,0.5);
  }
  .ys-tooltip-inner span{
    transform: scale(0.9);
    display: inline-block;
  }
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