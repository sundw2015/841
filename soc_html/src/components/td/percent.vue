<template>
  <div v-if="data==0" class="percent-box" @mouseover="show = true" @mouseout="show = false" v-bind:style="{width: width}">
    <span class="percent-value" style="border-radius: 5px;width:100%;"></span>
    <div class="percent-arrow" v-bind:style="{left: left_num}" v-show="show">
      <span>{{ data }}%</span>
      <p><i class="md md-arrow-drop-down"></i></p>
    </div>
  </div>
  <div v-if="data<3 && data>0" class="percent-box" @mouseover="show = true" @mouseout="show = false" v-bind:style="{width: width}">
    <span class="percent-up"></span>
    <span class="percent-value" style="width:98%"></span>
    <div class="percent-arrow" v-bind:style="{left: left_num}" v-show="show">
      <span>{{ data }}%</span>
      <p><i class="md md-arrow-drop-down"></i></p>
    </div>
  </div>
  <div v-if="data>=3 && data!=99" class="percent-box" @mouseover="show = true" @mouseout="show = false" v-bind:style="{width: width}">
    <span class="percent-up"></span>
    <span class="percent-value" v-bind:style="{width: (100-data) +'%' }"></span>
    <div class="percent-arrow" v-bind:style="{left: left_num}" v-show="show">
      <span>{{ data }}%</span>
      <p><i class="md md-arrow-drop-down"></i></p>
    </div>
  </div>
  <div v-if="data==99" class="percent-box" @mouseover="show = true" @mouseout="show = false" v-bind:style="{width: width}">
    <span class="percent-up"></span>
    <span class="percent-value" style="width:2%;border-radius: 20px;"></span>
    <div class="percent-arrow" v-bind:style="{left: left_num}" v-show="show">
      <span>{{ data }}%</span>
      <p><i class="md md-arrow-drop-down"></i></p>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'percent',
    props: {
      data: {
        default: 100
      },
      width: {
        default: "150px"
      }
    },
    computed: {
      left_num: {
        get: function () {
          if(this.width=="100%"){
            let width=this.data
            return width+"%"
          }else{
            let curWidth=this.width.substring(0,this.width.length-2);
            let width=(this.data/100)*curWidth
            return width+"px"
          }
        }
      }
    },
    data: function () {
      return {
        show: false
      }
    },
  }
</script>
<style scoped>
  .percent-box{
    width:150px;  
    position:relative;
    display: inline-block;
    padding: 5px;
  }
  .percent-up{
    width: 100%;
    height: 4px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius:5px;
    -khtml-border-radius: 5px;
    background: #00bd85;
    display: inline-block;
    position:absolute;
    top:3px;
    right:0px;
    z-index:1
  }
  .percent-value{
    position: absolute;
    top:3px;
    right:-1px;
    height: 4px;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background: #46578e;
    width:30px;
    z-index:2
  }
  .percent-arrow{
    position:absolute;
    top:-24px;
    left:20px;
    width:40px;
    height:20px;
    margin-left:-20px;
    line-height:20px;
    background:#edebf1;
    border-radius: 3px;
    font-size:12px;
    color:#000;
    text-align:center;
  }
  .percent-arrow p{
    position:relative;
  }
  .percent-arrow p i{
    position:absolute;
    top: -12px;
    left: 7px;
    color: #edebf1;
    font-size: 28px;
  }
  .percent-prev-value{
    width: 1%;
    height: 10px;
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
    background: #5fb433;
    display: inline-block;
    position:absolute;
    top:3px;
    left:0px;
    z-index:2
  }
  .percent-prev-bottom{
    position: absolute;
    top:3px;
    right:0px;
    height: 10px;
    border-radius: 20px;
    background: #d0d0d0;
    width:100%;
    z-index:1
  }
</style>