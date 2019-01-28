<template>
  <div class="ys-transfer">
    <div class="transfer-con">
      <div class="transfer-title">
        <checkbox :show.sync="leftAllSel" class="m-l-10" :text="left"></checkbox>
        <span class="fRight m-r-5 ys-info-color">{{leftSelList.length}}/{{dataList.length}}</span>
      </div>
      <div class="transfer-body">
        <ul>
          <li class="transfer-item p-l-10" v-for="list in dataList" @click="list.selected=!list.selected">
            <checkbox :show.sync="list.selected"></checkbox>
            <span class="m-l-5 verticalM">{{list.name}}</span>
          </li>
        </ul>
      </div>
    </div>
    <div class="transfer-move">
      <button v-bind:class="[rightSelList.length>0 ? 'hasSel' : 'disabled' ]"
              type="button"
              @click="returnList()">
        <i class="ys-icon icon-arrow-left"></i>
      </button>
      <button v-bind:class="[leftSelList.length>0 ? 'hasSel' : 'disabled' ]"
              class="m-t-10"
              type="button"
              @click="addToSel()">
        <i class="ys-icon icon-arrow-right"></i>
      </button>
    </div>
    <div class="transfer-con">
      <div class="transfer-title">
        <checkbox :show.sync="rightAllSel" class="m-l-10" :text="right"></checkbox>
        <span class="fRight m-r-5 ys-info-color">{{rightSelList.length}}/{{targetList.length}}</span>
      </div>
      <div class="transfer-body">
        <ul>
          <li class="transfer-item p-l-10" v-for="list in targetList" @click="list.selected=!list.selected">
            <checkbox :show.sync="list.selected"></checkbox>
            <span class="m-l-5 verticalM">{{list.name}}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .disabled{
    opacity: 0.2!important;
  }
  .transfer-con {
    display: inline-block;
    width: 180px;
    height: 210px;
    font-size: 12px;
    vertical-align: middle;
    position: relative;
    border:1px solid rgba(74,146,255,0.2);
    background: rgba(0,0,0,0.2);
    border-radius: 3px;
    padding-top: 30px;
  }
  .transfer-move{
    display: inline-block;
    overflow: hidden;
    margin: 0 16px;
    vertical-align: middle;
  }
  .transfer-title{
    padding:6px 0px 6px 0px;
    background:rgba(74,146,255,0.12);
    position: absolute;
    width:100%;
    overflow: hidden;
    top:0px;
    left:0px;
  }
  .transfer-body{
    height: 100%;
    overflow: hidden;
  }
  .transfer-body ul{
    height: 100%;
    overflow: auto;
  }
  .transfer-item{
    padding:6px 0px;
    overflow: hidden;
    text-overflow: ellipsis;
    clear: both;
    white-space: nowrap;
    cursor: pointer;
  }
  .transfer-item:hover{
    background:rgba(0,0,0,0.25);
  }
  .transfer-move button{
    padding: 6px 7px;
    border-radius: 3px;
    background: none;
    border:1px solid #808080;
    display: block;
  }
  .hasSel{
    border:1px solid rgba(74,146,255,0.3)!important;
    color:#4a92ff;
  }
</style>
<script>
  import Checkbox from "./checkbox";

  export default {
    components: {Checkbox},
    props: {
      dataList: {
        default: []
      },
      url: {
        default: false
      },
      type: {
        default: 'post'
      },
      params: {
        default: false
      },
      targetList:{
        default :[]
      },
      left:{
        default :"选择列表"
      },
      right:{
        default :"已选"
      },
    },
    data () {
      return {
        leftSelList:[],
        rightSelList:[],
      }
    },
    computed: {
      leftAllSel:{
        get: function () {
          this.leftSelList=[];
          for(let x in this.dataList){
            if(this.dataList[x].selected){
              this.leftSelList.push(this.dataList[x]);
            }
          }
          if(this.dataList.length==0){
            return false;
          }else{
            return this.dataList.reduce(function(prev, curr) {
              return prev && curr.selected;
            },true);
          }
        },
        set: function (newValue) {
          this.dataList.forEach(function(list){
            list.selected = newValue;
          });
        }
      },
      rightAllSel:{
        get: function () {
          this.rightSelList=[];
          for(let x in this.targetList){
            if(this.targetList[x].selected){
              this.rightSelList.push(this.targetList[x]);
            }
          }
          if(this.targetList.length==0){
            return false;
          }else{
            return this.targetList.reduce(function(prev, curr) {
              return prev && curr.selected;
            },true);
          }
        },
        set: function (newValue) {
          this.targetList.forEach(function(list){
            list.selected = newValue;
          });
        }
      },
    },
    ready(){
      let self=this;
      if(this.url){
        this.getData()
      }
    },
    methods:{
      getData(){
        if(this.type == 'get'){
          this.$http.get(this.url, this.params).then(function (response) {
            this.dataList = response.data.items
          })
        }else {
          this.$http.post(this.url, this.params).then(function (response) {
            this.dataList = response.data.items
          })
        }
      },
      addToSel(){
        if(this.leftSelList==0){
          return false
        }else{
          for(let x in this.leftSelList){
            this.leftSelList[x].selected=false
            this.targetList.unshift(this.leftSelList[x])
            this.dataList.$remove(this.leftSelList[x])
          }
          this.leftSelList=[];
        }
      },
      returnList(){
        if(this.rightSelList==0){
          return false
        }else{
          for(let x in this.rightSelList){
            this.rightSelList[x].selected=false
            this.dataList.unshift(this.rightSelList[x])
            this.targetList.$remove(this.rightSelList[x])
          }
          this.rightSelList=[];
        }
      },
    },
    watch: {
      'url': function () {
        this.getData()
      },
      'params':function(){
        this.getData()
      },
    }
  }
</script>