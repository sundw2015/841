<template>
  <div
    v-show="show"
    v-bind:class="{
      'alert':		true,
      'alert-success':(type == 'success'),
      'alert-warning':(type == 'warning'),
      'alert-info':	(type == 'info'),
      'alert-danger':	(type == 'danger'),
      'top': 			(placement === 'top'),
      'top-right': 	(placement === 'top-right')
    }"
    transition="fade"
    v-bind:style="{width:width}"
    role="alert">
    <div class="alert-box">
      <span v-show="dismissable" class="closeAlert" @click="show = false">
        <span><i class="ys-icon icon-clear"></i></span>
      </span>
      <slot></slot>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'alert',
    props: {
      type: {
        type: String
      },
      dismissable: {
        type: Boolean,
        default: false,
      },
      show: {
        type: Boolean,
        default: true,
        twoWay: true
      },
      duration: {
        type: Number,
        default: 0
      },
      width: {
        type: String
      },
      placement: {
        type: String
      }
    },
    watch: {
      show(val) {
        if (this._timeout) clearTimeout(this._timeout)
        if (val && Boolean(this.duration)) {
          this._timeout = setTimeout(()=> this.show = false, this.duration)
        }
      }
    }
  }
</script>
<style scoped>
  .alert {
    padding:0px!important;
    margin-bottom: 20px;
    border: none;
    border-radius: 3px;
  }
  .alert-box{
    padding: 24px 12px 24px 12px;
    position:relative;
    height:100%;
  }
  .closeAlert{
    position:absolute;
    right:6px;
    top:6px;
  }
  .alert-success{
    color: #e4e6f1!important;
    background-color: #00bd85!important;
    border: none!important;
  }
  .alert-danger {
    color: #e4e6f1!important;
    background-color:#e96157!important;
    border:none!important;
  }
  .fade-transition {
    transition: opacity .3s ease;
  }
  .fade-enter, .fade-leave {
    height: 0;
    opacity: 0;
    display: none;
  }
  .alert.top {
    position: fixed;
    top: 30px;
    margin: 0 auto;
    left: 0;
    right: 0;
    z-index: 2;
  }
  .alert.top-right {
    position: fixed;
    top: 75px!important;
    right: 10px;
    z-index: 9999;

  }
</style>
