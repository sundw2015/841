<template>
  <div class="ys-valid">
    <div @click="startValid()">
      <slot></slot>
    </div>
    <div class="ys-valid-popper ys-error-color"
         v-el:popper
         v-show="show"
         transition="fade">
      <slot name="content" class="content">{{errorText}}</slot>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'valid',
    props: {
      value:{},
      show: {
        default: false
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
      result:{
        type: Boolean,
        default: false
      }
    },
    data () {
      return {
        visible:false,
        validStatus:false,
        errorText:""
      };
    },
    ready(){

    },
    computed: {
      errorText:function(){
        if(this.validStatus){
          let reg=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])(\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])){3}$/;
          if(reg.test(this.value)){
            this.show=false;
            this.result=true;
          }else{
            if(this.value==""){
              this.show=false;
              this.result=false;
              return ""
            }else{
              this.show=true;
              this.result=false;
              return "请输入正确的IP地址";
            }
          }
        }else{
          this.show=false;
          this.result=false;
          return ""
        }

      },
    },
    methods: {
      startValid(){
        this.validStatus=true;
      }
    }
  };
</script>
<style scoped>
  .ys-valid{
    display: inline-block;
    position:relative;
  }
  .ys-valid-popper{
    display: block;
    font-size: 12px;
    position: absolute;
    visibility: visible;
    line-height: 1.5;
    z-index: 1060;
    top:32px;
    width: 100%;
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