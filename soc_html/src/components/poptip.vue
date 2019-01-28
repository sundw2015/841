<template>
  <div
        :class="classes"
        @mouseenter="handleMouseenter"
        @mouseleave="handleMouseleave"
        v-clickoutside="handleClose">
    <div
        :class="[prefixCls + '-rel']"
        v-el:reference
        @click="handleClick"
        @mousedown="handleFocus"
        @mouseup="handleBlur">
      <slot></slot>
    </div>
    <div :class="[prefixCls + '-popper']" :style="styles" transition="fade" v-el:popper v-show="visible">
      <div :class="[prefixCls + '-content']">
        <div :class="[prefixCls + '-arrow']"></div>
        <div :class="[prefixCls + '-inner']" v-if="confirm">
          <div :class="[prefixCls + '-body']">
            <div :class="[prefixCls + '-body-message']">
              <slot name="title">{{ title }}</slot>
            </div>
            <slot name="content"></slot>
          </div>
          <div :class="[prefixCls + '-footer']">
            <button type="primary"
                    class="ys-btn"
                    size="small"
                    @click="ok">{{ okText }}</button>
            <button type="text"
                    class="ys-btn ys-btn-white"
                    size="small"
                    @click="cancel">{{ cancelText }}</button>
          </div>
        </div>
        <div :class="[prefixCls + '-inner']" v-if="!confirm">
          <div :class="[prefixCls + '-title']" v-if="showTitle" v-el:title><slot name="title"><div :class="[prefixCls + '-title-inner']">{{ title }}</div></slot></div>
          <div :class="[prefixCls + '-body']">
            <div :class="[prefixCls + '-body-content']"><slot name="content"><div :class="[prefixCls + '-body-content-inner']">{{ content }}</div></slot></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import Popper from 'src/directives/popper';
  import clickoutside from 'src/directives/clickoutside';
  const prefixCls = 'ivu-poptip';
  export default {
    name: 'ys-poptip',
    mixins: [Popper],
    directives: { clickoutside },
    props: {
      trigger: {
        default: 'click'
      },
      placement: {
        default: 'right'
      },
      title: {
        type: [String, Number]
      },
      content: {
        type: [String, Number],
        default: ''
      },
      width: {
        type: [String, Number]
      },
      confirm: {
        type: Boolean,
        default: false
      },
      okText: {
        type: String,
        default: '确定'
      },
      cancelText: {
        type: String,
        default: '取消'
      }
    },
    data () {
      return {
        prefixCls: prefixCls,
        showTitle: true
      };
    },
    computed: {
      classes () {
        return [
          'ivu-poptip',
          {
            ['ivu-poptip-confirm']: this.confirm
          }
        ];
      },
      styles () {
        let style = {};
        if (this.width) {
          style.width = '${this.width}px';
        }
        return style;
      }
    },
    methods: {
      handleClick () {
        if (this.confirm) {
          this.visible = !this.visible;
          return true;
        }
        if (this.trigger !== 'click') {
          return false;
        }
        this.visible = !this.visible;
      },
      handleClose () {
        if (this.confirm) {
          this.visible = false;
          return true;
        }
        if (this.trigger !== 'click') {
          return false;
        }
        this.visible = false;
      },
      handleFocus () {
        if (this.trigger !== 'focus' || this.confirm) {
          return false;
        }
        this.visible = true;
      },
      handleBlur () {
        if (this.trigger !== 'focus' || this.confirm) {
          return false;
        }
        this.visible = false;
      },
      handleMouseenter () {
        if (this.trigger !== 'hover' || this.confirm) {
          return false;
        }
        this.visible = true;
      },
      handleMouseleave () {
        if (this.trigger !== 'hover' || this.confirm) {
          return false;
        }
        this.visible = false;
      },
      cancel () {
        this.visible = false;
        this.$emit('on-cancel');
      },
      ok () {
        this.visible = false;
        this.$emit('on-ok');
      }
    },
    ready () {
      if (!this.confirm) {
        this.showTitle = this.$els.title.innerHTML != '<div class="${prefixCls}-title-inner"></div>';
      }
    }
  };
</script>
<style scoped>
  .ivu-poptip,.ivu-poptip-rel {
    display: inline-block;
    position:relative;
  }
  .ivu-poptip-title {
    margin: 0;
    padding: 8px 16px;
    position: relative
  }

  .ivu-poptip-title-inner {
    color: #fff;
  }

  .ivu-poptip-body {
    padding: 8px 16px;
    display: block;
  }

  .ivu-poptip-body-content {
    overflow: auto
  }

  .ivu-poptip-body-content-inner {
    color: #657180
  }

  .ivu-poptip-inner {
    width: 100%;
    background-color:#161a2f;
    background-clip: padding-box;
    white-space: nowrap;
    border-radius: 3px;
    border: 1px solid rgba(74,146,255,0.5);
  }

  .ivu-poptip-popper {
    display: block;
    font-size: 12px;
    position: absolute
  }
  .ivu-poptip-popper{
    visibility: visible;
    line-height: 1.5;
    z-index: 1060;
  }
  .ivu-poptip-popper[x-placement^=top] {
    padding: 5px 0 8px
  }

  .ivu-poptip-popper[x-placement^=right] {
    padding: 0 5px 0 8px
  }

  .ivu-poptip-popper[x-placement^=bottom] {
    padding: 8px 0 5px
  }

  .ivu-poptip-popper[x-placement^=left] {
    padding: 0 8px 0 5px
  }

  .ivu-poptip-popper[x-placement^=top] .ivu-poptip-arrow {
    bottom: 3px;
    border-width: 5px 5px 0;
    border-top-color: rgba(0,0,0,.5)
  }

  .ivu-poptip-popper[x-placement=right-end] .ivu-poptip-arrow,.ivu-poptip-popper[x-placement=left-end] .ivu-poptip-arrow {
    bottom: 8px
  }

  .ivu-poptip-popper[x-placement=top] .ivu-poptip-arrow {
    left: 50%;
    margin-left: -5px
  }

  .ivu-poptip-popper[x-placement=top-start] .ivu-poptip-arrow {
    left: 16px
  }

  .ivu-poptip-popper[x-placement=top-end] .ivu-poptip-arrow {
    right: 16px
  }

  .ivu-poptip-popper[x-placement^=right] .ivu-poptip-arrow {
    left: 3px;
    border-width: 5px 5px 5px 0;
    border-right-color: rgba(0,0,0,.5)
  }

  .ivu-poptip-popper[x-placement=right] .ivu-poptip-arrow {
    top: 50%;
    margin-top: -5px
  }

  .ivu-poptip-popper[x-placement=right-start] .ivu-poptip-arrow {
    top: 8px
  }

  .ivu-poptip-popper[x-placement^=left] .ivu-poptip-arrow {
    right: 3px;
    border-width: 5px 0 5px 5px;
    border-left-color: rgba(0,0,0,.5)
  }

  .ivu-poptip-popper[x-placement=left] .ivu-poptip-arrow {
    top: 50%;
    margin-top: -5px
  }

  .ivu-poptip-popper[x-placement=left-start] .ivu-poptip-arrow {
    top: 8px
  }

  .ivu-poptip-popper[x-placement^=bottom] .ivu-poptip-arrow {
    top: 3px;
    border-width: 0 5px 5px;
    border-bottom-color: rgba(0,0,0,.5)
  }

  .ivu-poptip-popper[x-placement=bottom] .ivu-poptip-arrow {
    left: 50%;
    margin-left: -5px
  }

  .ivu-poptip-popper[x-placement=bottom-start] .ivu-poptip-arrow {
    left: 16px
  }

  .ivu-poptip-popper[x-placement=bottom-end] .ivu-poptip-arrow {
    right: 16px
  }

  .ivu-poptip-popper[x-placement^=top] .ivu-poptip-arrow:after {
    content: " ";
    bottom: 1px;
    margin-left: -5px;
    border-bottom-width: 0;
    border-top-color: rgba(0,0,0,0)
  }

  .ivu-poptip-popper[x-placement^=right] .ivu-poptip-arrow:after {
    content: " ";
    left: 1px;
    bottom: -5px;
    border-left-width: 0;
    border-right-color: rgba(0,0,0,0)
  }

  .ivu-poptip-popper[x-placement^=bottom] .ivu-poptip-arrow:after {
    content: " ";
    top: 1px;
    margin-left: -5px;
    border-top-width: 0;
    border-bottom-color: rgba(0,0,0,0)
  }

  .ivu-poptip-popper[x-placement^=left] .ivu-poptip-arrow:after {
    content: " ";
    right: 1px;
    border-right-width: 0;
    border-left-color: rgba(0,0,0,0);
    bottom: -5px
  }

  .ivu-poptip-arrow,.ivu-poptip-arrow:after {
    display: block;
    width: 0;
    height: 0;
    position: absolute;
    border-color: transparent;
    border-style: solid
  }

  .ivu-poptip-arrow {
    border-width: 6px
  }

  .ivu-poptip-arrow:after {
    content: "";
    border-width: 5px
  }
  .ivu-poptip-popper[x-placement^=right] .ivu-poptip-arrow:before{
    content: '';
    width: 8px;
    height: 8px;
    overflow: hidden;
    zoom: 1;
    position: absolute;
    border-right: 1px solid rgba(74,146,255,0.5);
    border-bottom: 1px solid rgba(74,146,255,0.5);
    background-color: #161a2f;
    top: -4px;
    left: 1px;
    transform: rotate(135deg);
    -o-transform: rotate(135deg);
    -moz-transform: rotate(135deg);
    -webkit-transform: rotate(135deg);
  }
  .ivu-poptip-popper[x-placement^=left] .ivu-poptip-arrow:before{
    content: '';
    width: 8px;
    height: 8px;
    overflow: hidden;
    zoom: 1;
    position: absolute;
    border-right: 1px solid rgba(74,146,255,0.5);
    border-bottom: 1px solid rgba(74,146,255,0.5);
    background-color: #161a2f;
    top:-4px;
    left:-9px;
    transform: rotate(-45deg);
    -o-transform: rotate(-45deg);
    -moz-transform: rotate(-45deg);
    -webkit-transform: rotate(-45deg);
  }
  .ivu-poptip-confirm .ivu-poptip-inner {
    white-space: nowrap;
  }

  .ivu-poptip-confirm .ivu-poptip-body {
    padding: 16px 16px 8px
  }

  .ivu-poptip-confirm .ivu-poptip-footer {
    text-align: left;
    padding: 8px 16px 16px
  }

  .ivu-poptip-confirm .ivu-poptip-footer button {
    margin-right: 4px
  }
  .ivu-poptip-confirm .ivu-poptip-footer button:first-child{
    margin-right:6px;
  }
  .ivu-poptip-popper {
    min-width: 0;
    text-align: left
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