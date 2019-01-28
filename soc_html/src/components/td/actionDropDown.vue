<template>
  <div class="edit-td" @click="show = !show" @blur="show = false">
    <span class="edit-icon" >
      <img src="../../assets/images/edit_icon.svg"/>
    </span>
    <div class="ys-edit-box " v-show="show">
      <p class="arrow-p"><i class="arrow1"></i></p>
      <div class="square1">
        <ul>
          <slot></slot>
          <div class="clearfix"></div>
        </ul>
      </div>
    </div>
  </div>
</template>
<style>
  .show {
    display: block;
  }
  .edit-td{
    display:inline-block;
    position:relative;
    line-height:0px;
  }
  .ys-edit-box{
    line-height:0px;
    width:100px;
    height:200px;
    z-index:2;
    position: absolute;
    top:20px;
    left:-42px;
  }
  .ys-edit-box ul{
    -webkit-padding-start: 0px;
    margin:0px;
  }
  .ys-edit-box ul li{
    list-style:none;
    height:24px;
    line-height:24px;
    cursor:pointer;
    color:#f2f2f2;
    font-size:12px;
    text-align: left!important;
  }
  .ys-edit-box ul li:hover{
    color:#5ca9e5;
  }
  .ys-edit-box ul li i{
    margin-right:3px;
  }
  .square1 {
    display: block;
    padding: 6px 8px;
    width: 100px;
    border-radius: 5px;
    background-color: rgba(0,0,0,0.6);
  }
  .arrow-p{
    height:20px!important;
    margin-top:-11px;
    position:relative;
  }
  .arrow1 {
    width: 0;
    height: 0;
    overflow: hidden;
    zoom: 1;
    border: 8px solid transparent;
    _border-color:tomato;
    _filter:chroma(color=tomato);
    border-bottom-color: rgba(0,0,0,0.6);
    position: absolute;
    top:4px;
    left:44px;
  }
</style>
<script>
  export default {
    props: {
      show: {
        default: false
      }
    },
    data() {
      return {
        old: {}
      }

    },
    ready: function () {
      this.old = Object.assign({}, this.row);
    }
  }

</script>