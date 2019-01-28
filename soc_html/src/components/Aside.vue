<template>
  <div class="aside"
       v-bind:style="{left:left,width:width,zIndex:index}"
       v-bind:class="{
    left:placement === 'left',
    right:placement === 'right'
    }"
       v-show="show"
       :transition="(this.placement === 'left') ? 'slideleft' : 'slideright'">
    <div class="aside-dialog">
      <div class="aside-content">
        <div class="aside-close"
             @click='close'>
          <i class="ys-icon icon-clear ys-primary-color"></i>
        </div>
        <div class="aside-head"
             v-bind:style="{left:left,width:width}">
          <div class="aside-head-inner">{{ header }}</div>
        </div>
        <div class="aside-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import EventListener from 'src/assets/js/utils/EventListener.js'
  import getScrollBarWidth from 'src/assets/js/utils/getScrollBarWidth.js'
  import coerceBoolean from 'src/assets/js/utils/coerceBoolean.js'
  export default {
    name: 'aside',
    props: {
      show: {
        type: Boolean,
        coerce: coerceBoolean,
        require: true,
        twoWay: true
      },
      placement: {
        type: String,
        default: 'right'
      },
      header: {
        type: String
      },
      width: {
        type: String,
        default: 'auto'
      },
      left: {
        type: String,
        default: '0'
      },
      top: {
        type: String,
        default: '0'
      },
      margin: {
        type: String,
        default: '0'
      },
      index:{
        type: String,
        default: '98'
      }
    },
    ready:function(){
    },
    watch: {
      show(val) {
        const body = document.body
        const scrollBarWidth =  getScrollBarWidth()
        if (val) {
          if (scrollBarWidth !== 0) {
            body.style.paddingRight = scrollBarWidth + 'px'
          }
        } else {
          if (this._clickEvent) this._clickEvent.remove()
        }
      }
    },
    methods: {
      close() {
        this.show = false
      }
    }
  }
</script>

<style>
  .aside-open {
    transition: transform 0.3s;
  }
  .aside-open.has-push-right {
    transform: translateX(-300px);
  }
  .aside{
    position: fixed;
    top: 52px;
    bottom: 0;
    z-index: 98;
    width:auto;
    color:#f2f2f2;
    box-shadow:0px 3px 8px 3px rgba(0,0,0,0.3);
  }
  .aside:after{
    z-index:-1;
    content:'';
    position:absolute;
    top:0px;
    left:0px;
    width:100%;
    height:100%;
    background-image: url("../assets/images/aside-bg.png");
    background-repeat: no-repeat;
    background-size: cover;
    -webkit-filter: blur(10px);
    -ms-filter: blur(10px);
    filter: blur(10px);
    filter: progid:DXImageTransform.Microsoft.Blur(PixelRadius=10, MakeShadow=false) \9;
  }
  .aside.left {
    left: 0;
    right: auto;
  }
  .aside.right {
    left: auto;
    right: 0;
  }
  .slideright-enter {
    animation:slideright-in .3s;
  }
  .slideright-leave {
    animation:slideright-out .3s;
  }
  @keyframes slideright-in {
    0% {
      transform: translateX(100%);
      opacity: 0;
    }
    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }
  @keyframes slideright-out {
    0% {
      transform: translateX(0);
      opacity: 1;
    }
    100% {
      transform: translateX(100%);
      opacity: 0;
    }
  }
  @media (max-width: 991px) {
    .aside {
      min-width:240px
    }
  }
  .aside-dialog{
    background:rgba(22, 26, 47, 0.7);
    height:100%;
    overflow-x: hidden;
    box-shadow: 0px 11px 8px -9px rgba(0,0,0,0.2) inset;
  }
  .aside-close{
    position:fixed;
    right:20px;
    cursor:pointer;
    z-index:1000;
    margin-top:13px;
  }
  .aside-head{
    height: 40px;
    position: fixed;
    z-index: 999;
    right:0px;
  }
  /*.aside-head:before{*/
    /*content: "";*/
    /*position: absolute;*/
    /*!* width: 100%; *!*/
    /*left: 16px;*/
    /*top: 40px;*/
    /*right: 16px;*/
    /*height: 1px;*/
    /*background: rgba(74,146,255,0.4);*/
    /*z-index: -1;*/
  /*}*/
  .aside-head:before{
    content: "";
    position: absolute;
    width: 100%;
    left: 0px;
    top: 0px;
    right: 16px;
    height: 40px;
    background: rgba(22, 26, 47, 1);
    z-index: -1;
  }
  .aside-head-inner{
    padding-left: 16px;
    height: 40px;
    line-height:40px;
  }
  .aside .aside-dialog .aside-body {
    position: relative;
  }
  .aside-body{
    padding:60px 40px 20px 30px;
  }
  .edit-label{
    width:90px;
    padding-right:10px;
    display: inline-block;
  }
  .aside-sure-btn{
    padding:8px 40px;
    background: #0878cb;
    border:none;
    border-radius: 3px;
  }
  .aside-quit-btn{
    padding:8px 40px;
    background: #505050;
    border:none;
    border-radius: 3px;
  }
</style>