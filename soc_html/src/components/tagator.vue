<template>
  <div class="tagator-box"  v-bind:style="{width: width + 'px'}">
    <span v-for="tag in list"
          class="tagator-tag"
          track-by="$index"
          v-on:mouseenter="mouseOver($index)"
          v-on:mouseleave="mouseOut($index)">
      {{tag}}
      <span class="tag-del ys-error-color" v-if="curIndex==$index" @click="delTag($index,tag)"><i class="ys-icon icon-clear-circle"></i></span>
    </span>
    <input type="text" class="tagator-input" :placeholder="text" v-model="value"/>
  </div>
</template>
<script>
  export default {
    name: 'tagator',
    props: {
      show: {
        type: String,
        default: 'right'
      },
      width: {
        default: '300'
      },
      placement: {
        type: String,
        default: 'right'
      },
      text:{
        default:"例如:\'rar\',回车或者Enter添加"
      },
      list:{
        type: Array,
        default:[]
      }
    },
    data() {
      return {
        value:"",
        curIndex:-1,
      }
    },
    ready:function(){
      let self=this;
      //let re = /^[A-Za-z0-9]+$/g
      window.addEventListener('keydown', function(e){
        if(e.keyCode==13 || e.keyCode==32){
          if( self.list.includes(self.value) || self.value=="" || self.value.indexOf(" ") != -1){
            return false;
          }else{
            self.list.push(self.value);
            self.value="";
          }
        }
      })
    },
    methods: {
      close() {
        this.show = false
      },
      mouseOver(index){
        this.curIndex=index;
      },
      mouseOut(){
        this.curIndex=-1;
      },
      delTag(index){
        this.list.splice(index, 1);
      }
    }
  }
</script>

<style scoped>
  .tagator-box{
    border-radius: 3px;
    border: 1px solid rgba(74,146,255,0.2);
    box-shadow: inset 1px 1px 3px 0px rgba(0,0,0,0.2);
    background: rgba(0,0,0,0.2);
    min-height:32px;
    padding:0px 5px;

    overflow: hidden;
    display: inline-block;
    white-space: normal !important;
    word-break: break-all;
    word-wrap: break-word;
    cursor: text;
    position:relative;
  }
  .tagator-input{
    position:absolute;
    width:160px;
    border:none;
    background: none;
    height:32px;
    line-height:32px;
    vertical-align: middle;
  }
  .tagator-tag{
    display: inline-block;
    position: relative;
    z-index: 0;
    border: 1px solid rgba(74,146,255,0.3);
    background:rgba(0,0,0,0.25);
    border-radius: 3px;
    padding: 0 0.7em 0 0.7em;
    line-height: 1.5em;
    margin: 5px 2px;
    cursor: pointer;
  }
  .tagator-tag .tag-del{
    display: block;
    position: absolute;
    background:rgba(0,0,0,0.85);
    z-index: 1;
    right: -5px;
    top: -3px;
    font-size: 12px;
    width:12px;
    height:12px;
    line-height:12px;
    text-align: center;
    cursor: pointer;
    border-radius: 50%;
    transition-property: color;
    transition-duration: 300ms;
  }
</style>