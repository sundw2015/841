<template>
  <div class="ys-tooltip">
    <div v-el:reference>
      <slot></slot>
    </div>
    <div class="ys-tooltip-popper"
         v-el:popper
         v-show="!disabled && visible"
         transition="fade">
      <div class="ys-tooltip-content">
        <div class="ys-tooltip-arrow"></div>
        <div class="ys-tooltip-arrow ys—tooptip-arrow-bg"></div>
        <div class="ys-tooltip-inner">
          <slot name="content">{{ content }}</slot>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import Popper from 'src/directives/popper';
  export default {
    mixins: [Popper],
    props: {
      placement: {
        default: 'bottom'
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
      },
      status:{
        type:Boolean,
        default:false
      }
    },
    data () {
      return {
        //visible:false
      };
    },
    ready(){

    },
    watch:{
      'status':function(){
        if(!this.status){
          this.handleClosePopper()
        }else{
          this.handleShowPopper()
        }
      }
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
    border-top-color:  #e96157
  }
  .ys-tooltip-popper[x-placement^=top] .ys—tooptip-arrow-bg{
    width: 0;
    height: 0;
    border-style: solid dashed dashed dashed;
    border-color: #fbd8d6 transparent transparent transparent;
    bottom:4px;
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
    border-right-color: #e96157
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
    border-left-color: rgba(70,76,91,.9)
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
    border-bottom-color: #e96157
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
  .ys-tooltip-inner {
    max-width: 250px;
    min-height: 26px;
    padding: 3px 8px;
    color: #e96157;
    text-align: left;
    background-color: #fbd8d6;
    white-space: normal;
    border-radius: 3px;
    border:1px solid #e96157;
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