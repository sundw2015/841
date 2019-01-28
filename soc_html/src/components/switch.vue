<template>
    <span :class="wrapClasses" @click="toggle">
        <span :class="innerClasses">
            <slot name="open" v-if="checked"></slot>
            <slot name="close" v-if="!checked"></slot>
        </span>
    </span>
</template>
<script>
  const prefixCls = 'ivu-switch';
  export default {
    name: 'ys-switch',
    props: {
      checked: {
        type: Boolean,
        default: false
      },
      disabled: {
        type: Boolean,
        default: false
      },
      size: {
        default:"large",
      }
    },
    computed: {
      wrapClasses () {
        return [
          `${prefixCls}`,
          {
            [`${prefixCls}-checked`]: this.checked,
            [`${prefixCls}-disabled`]: this.disabled,
            [`${prefixCls}-${this.size}`]: !!this.size
          }
        ];
      },
      innerClasses () {
        return `${prefixCls}-inner`;
      }
    },
    methods: {
      toggle () {
        if (this.disabled) {
          return false;
        }
        this.checked = !this.checked;
        this.$emit('on-change', this.checked);
        this.$dispatch('on-form-change', this.checked);
      }
    }
  };
</script>
<style scoped>
  .ivu-switch {
    width: 60px;
    height: 20px;
    line-height: 20px;
    border-radius: 24px;
    vertical-align: middle;
    background: #46578e;
    position: relative;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    transition: all .2s ease-in-out;
    display: inline-block;
  }

  .ivu-switch-inner {
    color: #fff;
    font-size: 12px;
    position: absolute;
    left: 25px
  }

  .ivu-switch-inner i {
    width: 12px;
    height: 12px;
    text-align: center
  }

  .ivu-switch:after {
    content: '';
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background:linear-gradient(to bottom, #ffffff, #c1d4f1);
    position: absolute;
    left: 1px;
    top: 1px;
    cursor: pointer;
    box-shadow: 1px 0px 5px 2px rgba(0,0,0,.2);
    transition: left .2s ease-in-out,width .2s ease-in-out;
  }

  .ivu-switch:active:after {
    width: 26px
  }

  .ivu-switch:focus {
    box-shadow: 0 0 0 2px rgba(51,153,255,.2);
    outline: 0
  }

  .ivu-switch:focus:hover {
    box-shadow: none
  }

  .ivu-input-number-focused,.ivu-input-number:focus,.ivu-page-options-elevator input:focus,.ivu-select-visible .ivu-select-selection {
    box-shadow: 0 0 0 2px rgba(51,153,255,.2);
    outline: 0
  }

  .ivu-switch-small {
    width: 24px;
    height: 12px;
    line-height: 10px
  }

  .ivu-switch-small:after {
    width: 10px;
    height: 10px;
    top: 1px;
    left: 0
  }

  .ivu-switch-small:active:after {
    width: 14px
  }

  .ivu-switch-small.ivu-switch-checked:after {
    left: 14px
  }

  .ivu-switch-small:active.ivu-switch-checked:after {
    left: 8px
  }

  .ivu-switch-large {
    width: 60px
  }

  .ivu-switch-large:active:after {
    width: 32px
  }

  .ivu-switch-large.ivu-switch-checked:after {
    left: 41px
  }

  .ivu-switch-large:active.ivu-switch-checked:after {
    left: 25px
  }

  .ivu-switch-checked {
    border-color: #4a92ff;
    background-color: #4a92ff
  }

  .ivu-switch-checked .ivu-switch-inner {
    left: 8px
  }

  .ivu-switch-checked:after {
    left: 41px
  }

  .ivu-switch-checked:active:after {
    left: 19px
  }

  .ivu-switch-disabled {
    cursor: not-allowed;
    background: #f3f3f3;
    border-color: #f3f3f3
  }

  .ivu-switch-disabled:after {
    background: #ccc;
    cursor: not-allowed
  }

  .ivu-switch-disabled .ivu-switch-inner {
    color: #ccc
  }
</style>