<template>
  <div :class="wrapClasses">
    <div class="ys-modal-mask"
         v-show="show"
         transition="fade"></div>
    <div class="ys-modal"
         v-show="show"
         transition="ease"
         v-bind:style="{ width: width + 'px' }">
      <div class="ys-modal-content">
        <a class="ys-modal-close ys-primary-color" @click="close()"><i class="ys-icon icon-clear"></i></a>
        <div class="ys-modal-header"><div class="ys-modal-header-inner">{{title}}</div></div>
        <div class="ys-modal-body">
          <slot name="content"></slot>
        </div>
        <div class="ys-modal-footer textC">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .ys-modal-wrap {
    overflow: auto;
    z-index: 1000;
    -webkit-overflow-scrolling: touch;
    outline: 0;
  }
  .vertical-center-modal {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
  }
  .ys-modal-mask, .ys-modal-wrap {
    position: fixed;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
  }
  .ys-modal-mask {
    background-color: rgba(46,61,106,.4);
    height: 100%;
  }
  .ys-modal {
    width: auto;
    margin: 0 auto;
    position: relative;
    outline: 0;
    top: -50px;
    background: linear-gradient(145deg, #29293b 0%, #4e424b 100%);
    background-size: cover;
    box-shadow: 3px 3px 5px 0 rgba(0,0,0,.4);
    -moz-box-shadow:3px 3px 5px 0 rgba(0,0,0,.4);
    -webkit-box-shadow:3px 3px 5px 0 rgba(0,0,0,.4);
    transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
    -moz-transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
    -webkit-transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
  }
  .ys-modal-content {
    position: relative;
    background-clip: padding-box;
    background: rgba(30,34,54,0.75);
  }
  .ys-modal-close {
    position: absolute;
    right: 12px;
    top: 11px;
    cursor: pointer;
  }
  .ys-modal-close:hover{
    color:#f2f2f2;
  }
  .ys-modal-header {
    height:40px;
    line-height:40px;
    padding:0px 16px;
  }
  .ys-modal-header p, .ys-modal-header-inner {
    display: inline-block;
    width: 100%;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-bottom:1px solid rgba(74,146,255,0.4);
  }
  .ys-modal-body {
    padding: 16px;
    font-size: 12px;
    line-height: 1.5;
  }
  .ys-modal-footer {
    padding: 12px 18px;
    text-align: right;
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
  .ease-transition {
    display: inline-block; /* 否则 scale 动画不起作用 */
  }
  .ease-enter {
    animation: ysEaseIn .5s;
  }
  .ease-leave {
    animation: ysEaseOut .5s;
  }
  @keyframes ysEaseIn {
    0% {
      opacity: 0;
      transform: scale(.9)
    }

    100% {
      opacity: 1;
      transform: scale(1)
    }
  }
  @-webkit-keyframes ysEaseIn {
    0% {
      opacity: 0;
      transform: scale(.9)
    }

    100% {
      opacity: 1;
      transform: scale(1)
    }
  }

  @keyframes ysEaseOut {
    0% {
      opacity: 1;
      transform: scale(1)
    }

    100% {
      opacity: 0;
      transform: scale(.9)
    }
  }
  @-webkit-keyframes ysEaseOut {
    0% {
      opacity: 1;
      transform: scale(1)
    }

    100% {
      opacity: 0;
      transform: scale(.9)
    }
  }

</style>
<script>
  export default {
    name: 'ys-modal',
    props: {
      show: {
        default: false
      },
      title: {
        default: ""
      },
      width:{
        default: "400"
      }
    },
    data() {
      return {
        wrapShow: false,
      }
    },
    ready () {
      if (this.show) {
        this.wrapShow = true;
      }
    },
    computed: {
      wrapClasses () {
        return [
          'ys-modal-wrap','vertical-center-modal',
          {
            ['d-none']: !this.wrapShow,
          }
        ];
      }
    },
    methods:{
      close(){
        this.show=false;
      },
      addScrollEffect () {
        this.checkScrollBar();
        this.setScrollBar();
        document.body.style.overflow = 'hidden';
      },
      checkScrollBar () {
        let fullWindowWidth = window.innerWidth;
        if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
          const documentElementRect = document.documentElement.getBoundingClientRect();
          fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left);
        }
        this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth;
        if (this.bodyIsOverflowing) {
          this.scrollBarWidth = this.getScrollBarSize();
        }
      },
      setScrollBar () {
        if (this.bodyIsOverflowing && this.scrollBarWidth !== undefined) {
          document.body.style.paddingRight = '${this.scrollBarWidth}px';
        }
      },
      resetScrollBar () {
        document.body.style.paddingRight = '';
      },
      removeScrollEffect() {
        document.body.style.overflow = '';
        this.resetScrollBar();
      },
      getScrollBarSize(){
        if (document.documentElement.scrollHeight <= document.documentElement.clientHeight) {
          return 0
        }
        let inner = document.createElement('p')
        inner.style.width = '100%'
        inner.style.height = '200px'

        let outer = document.createElement('div')
        outer.style.position = 'absolute'
        outer.style.top = '0px'
        outer.style.left = '0px'
        outer.style.visibility = 'hidden'
        outer.style.width = '200px'
        outer.style.height = '150px'
        outer.style.overflow = 'hidden'
        outer.appendChild(inner)

        document.body.appendChild(outer)
        let w1 = inner.offsetWidth
        outer.style.overflow = 'scroll'
        let w2 = inner.offsetWidth
        if (w1 === w2) w2 = outer.clientWidth

        document.body.removeChild(outer)

        return (w1 - w2)
      }
    },
    beforeDestroy () {
      this.removeScrollEffect();
    },
    watch: {
      show (val) {
        let self=this;
        if (val === false) {
          setTimeout(function(){
            self.wrapShow = false;
            self.removeScrollEffect();
          }, 500);
        } else {
          this.wrapShow = true;
          //this.addScrollEffect();
        }
      },
    }
  }

</script>