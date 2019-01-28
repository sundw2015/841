<template>
  <div v-if="!multiple" class="select-con"
       onmousedown="event.preventDefault()"
       v-clickoutside="close"
       v-el:con
       v-bind:style="{width: width + 'px'}">
    <div class="select-input"
         v-bind:class="[show ? '' : '', filter ? 'filter' : '',global ? 'global' : '' ]">
      <div class="select-open-icon">
        <i @click="show ? close() : open()"
           class="ys-icon select-arrow"
           v-bind:class="[filter || global ? 'icon-arrow-filter' : 'icon-arrow-down']"
           v-bind:class="[show ? 'arrow-rotate' : '' ]"></i>
      </div>
      <span v-if="selected.name" @click="show ? close() : open()" class="select-text">{{ selected.name }}</span>
      <span v-else @click="show ? close() : open()" class="select-text">{{ placeholder }}</span>
    </div>
    <div v-show="show"
         class="select-body"
         v-bind:class="[global ? 'global' : '' ]"
         transition="slide">
      <div class="select-edit-box" v-show="searchable" @click="getFocus()">
        <input v-model="search"
               class="ys-input"
               v-el:search
               onmousedown="event.preventDefault()"
               @keyup="goSearch()"
               placeholder="输入内容搜索">
        <i class="ys-icon icon-search search-btn"></i>
      </div>
      <div class="select-box" v-bind:class="[searchable ? 'm-t-10' : '' ]">
        <div class="select-option"
             v-for="o in option"
             rack-by="$index"
             onmousedown="event.preventDefault()"
             @click="selectOption(o)"
             v-bind:class="[selected.id==o.id ? 'cur-select' : '' ]">{{ o.name }}</div>
        <div class="textC p-b-5" v-if="moreStatus"><loading-mini :show="true"></loading-mini></div>
      </div>
    </div>
    <div class="select-remark" v-if="remark.length>0">
      <i class="md md-info verticalM font16 m-r-3"></i>
      <span class="verticalM">{{remark}}</span>
    </div>
  </div>
  <div v-if="multiple"
       class="select-con"
       onmousedown="event.preventDefault()"
       @keyup.esc="close()"
       v-clickoutside="close"
       v-el:con
       v-bind:style="{width: width + 'px'}">
    <div class="multi-select-input" @click="show ? close() : open()">
      <span class="multi-label" v-if="selected.length == 0 || typeof selected == 'String'">未选择</span>
      <div class="multi-tag"
           v-for="i in selected"
           track-by="$index"
           @click="delSelect(i)">
        <span class="multi-tag-text verticalM">{{ i.name }}</span>
        <i class="md md-close m-l-3 verticalM text-cursor"></i>
      </div>
      <div class="multi-select-open" @click="show ? close() : open()">
        <i class="ys-icon select-arrow icon-arrow-down"
           v-bind:class="[show ? 'arrow-rotate' : '' ]"></i>
      </div>
    </div>
    <div v-show="show"
         class="multi-select-body"
         transition="slide">
      <div class="select-box">
        <div class="select-option"
             v-for="o in filterOption | filterBy search in 'name'"
             rack-by="$index"
             @click="addSelect(o)">{{ o.name }}</div>
      </div>
    </div>
    <div class="select-remark" v-if="remark.length>0">
      <i class="md md-info verticalM font16 m-r-3"></i>
      <span class="verticalM">{{remark}}</span>
    </div>
  </div>
</template>
<style scoped>
  .slide-transition {
    display: inline-block; /* 否则 scale 动画不起作用 */
  }
  .slide-enter {
    animation: antSlideUpIn .5s;
  }
  .slide-leave {
    animation: antSlideUpOut .5s;
  }
  @-webkit-keyframes antSlideUpIn {
    0% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
    100% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }
  @keyframes antSlideUpIn {
    0% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
    100% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }
  @-webkit-keyframes antSlideUpOut {
    0% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
    100% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
  }
  @keyframes antSlideUpOut {
    0% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
    100% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
  }
  .arrow-rotate{
    transform: rotate(180deg);
  }
  .select-focus{
    border:1px solid #7e9fd0!important;
    box-shadow: 0px 0px 5px 1px #7e9fd0;
    -moz-box-shadow:0px 0px 5px 1px #7e9fd0;
    -webkit-box-shadow:0px 0px 5px 1px #7e9fd0;
    transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
    -moz-transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
    -webkit-transition: border .2s ease-in-out,box-shadow .2s ease-in-out;
  }
  .select-con{
    width:130px;
    display: inline-block;
    box-sizing: border-box;
    vertical-align: middle;
    color: #f2f2f2;
    font-size: 12px;
    line-height: normal;
    cursor:pointer;
    position: relative;
  }
  .select-input {
    height: 26px;
    background:rgba(0,0,0,0.2);
    position: relative;
    display: block;
    box-sizing: border-box;
    outline: 0;
    -moz-user-select: none;
    user-select: none;
    cursor: pointer;
    border-radius: 3px;
    box-shadow: inset 1px 1px 3px 0px rgba(0,0,0,0.2);
    border:1px solid rgba(74,146,255,0.2);
  }
  .select-input:focus
  {

  }
  .select-input p{
    margin-right:22px;
    width:100%;
  }

  .select-input.filter{
    border:none;
    background:none;
    box-shadow: none;
  }
  .select-input.filter .select-text{
    text-align:right;
    padding-right:22px;
    line-height:26px;
  }
  .select-input.global{
    height:36px;
  }
  .select-input.global .select-text{
    height:36px;
    line-height:34px;
    font-size:16px;
    padding-left:12px;
  }
  .select-input.global .select-open-icon i{
    right: 10px;
    top: 4px;
  }
  .select-arrow{
    transition: all .3s ease-in-out;
  }

  .multi-select-open{
    position: absolute;
    top: 50%;
    right: 3px;
    line-height: 1;
    margin-top: -5px;
    color: #f2f2f2;
    transition: all .2s ease-in-out;
  }
  .multi-label{
    display: block;
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding-left: 0px;
    padding-right: 22px;
    padding-top:3px;
    text-align: left!important;
  }
  .multi-tag{
    display: inline-block;
    height: 20px;
    line-height: 20px;
    margin: 3px 3px 3px 0;
    padding: 0 6px;
    border-radius: 3px;
    background: rgba(74, 146, 255, 1);
    vertical-align: middle;
    overflow: hidden;
    cursor: pointer;
  }
  .multi-select-input{
    padding: 0 24px 0px 6px;
    min-height: 26px;
    background:rgba(0,0,0,0.2);
    border: 1px solid #7e9fd0;
    color:#f2f2f2;
    border:1px solid rgba(74,146,255,0.2);
    border-radius: 3px;
    text-align: left!important;
  }

  .select-input .select-open-icon{
    float:right;
    width:20px;
  }
  .select-open-icon{
    position:relative;
  }
  .select-open-icon i{
    position:absolute;
    right:8px;
    top:-1px;
    cursor:pointer;
    line-height:26px;
    color:#4a92ff;
  }
  .select-input.filter .select-open-icon i{
    top:0px;
  }
  .select-text{
    display: block;
    height: 26px;
    line-height: 24px;
    font-size: 12px;
    overflow: hidden;
    padding-left:6px;
    padding-right: 16px;
    text-align: left;
  }
  .select-body{
    width: 100%;
    position: absolute;
    z-index:9999;
    top:26px;
    right:0px;
    background:#161a2f;
    background: linear-gradient(to right, #1c1c2d 0%, #2d2831 100%);
    padding-bottom:10px;
    border-top:none;
    border-radius: 3px;
    box-shadow: 2px 2px 5px 1px rgba(0,0,0,0.3);
  }
  .select-body.global{
    top:36px;
  }
  .multi-select-body{
    width: 100%;
    position: absolute;
    z-index:3;
    left:0px;
    transform-origin: center top 0px;
    background:#161a2f;
    background: linear-gradient(to right, #1c1c2d 0%, #2d2831 100%);
    border-radius: 3px;
  }
  .select-remark{
    width: 500px;
    position: absolute;
    z-index:2;
    top:33px;
    left:0px;
    color:#f2f2f2;
    font-size:12px;
  }
  .select-edit-box{
    position:relative;
    margin:auto;
    padding:3px 8px;
    margin-top:5px;
  }
  .search-btn{
    color:#3a82ed;
  }
  .select-edit-box input{
    width:100%;
    background:none;
    height:26px;
    line-height:26px;
  }
  .select-edit-box i{
    position:absolute;
    top:11px;
    right:12px;
    cursor:pointer;
  }
  .select-box {
    width: 100%;
  }
  .select-option{
    color:#6591d2;
    padding-left:6px;
    height:26px;
    line-height:26px;
    cursor: pointer;
    overflow: hidden;
    text-align:left;
  }
  .select-option:hover{
    color:#6591d2;
    background: rgba(74, 146, 255, 0.2);
  }
  .cur-select{
    color:#ffffff;
    background:#4a92ff;
  }
  .cur-select:hover{
    color:#ffffff;
    background:#4a92ff;
  }
</style>
<script>
import clickoutside from 'src/directives/clickoutside';
import LoadingMini from "./loading-mini";
export default {
  components: {LoadingMini},
  name: 'ys-select',
  directives: { clickoutside },
  props: {
    option: Array,
    url: {
      default: false
    },
    more:{
      default: false
    },
    type: {
      default: 'post'
    },
    params: {
      default: function () {
        return {'all': 1}
      }
    },
    global:{
      default: false
    },
    filter:{
      default: false
    },
    width: {
      default: ""
    },
    remark: {
      default: ""
    },
    selected: {
      default : function () {
        return {}
      }
    },
    selectId: {
      default : ""
    },
    placeholder: {
      default: '未选择'
    },
    multiple: {
      type: Boolean,
      default: false
    },
    searchable: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      search: "",
      show: false,
      filterOption: [],
      inputHigh:0,
      page:1,
      moreStatus:false,
    }
  },
  ready(){
    let self=this;
    if(this.selectId){
      this.selectOptionId(this.selectId)
    }
    slimFunc()
    function slimFunc(){
      $('.select-box').slimScroll({
        height: '210',
        position: 'right',
        size: "5px",
        color: '#4a92ff',
        opacity: 1,
        railColor: '#232027',
        railOpacity: 1,
        wheelStep: 5
      })
      $(".select-box").slimScroll().bind('slimscroll', function(e, pos){
        if(self.more && pos=='bottom'){
          self.moreStatus=true;
          let data=self.params;
          data.page=self.page;
          data.all=0;
          data.page++;
          self.$http.post(self.url, data).then(function (response) {
            for(let x in response.data.items){
              self.option.push(response.data.items[x]);
            }
            self.moreStatus=false;
          })
        }
      });
    }
    $(window).resize(function() {
      slimFunc()
    })
    if(this.url){
      this.getData();
    }
  },
  methods:{
    goSearch(){
      let data=this.params;
      data.page=1;
      data.q=this.search;
      this.option=[];
      this.$http.post(this.url, data).then(function (response) {
        for(let x in response.data.items){
          this.option.push(response.data.items[x]);
        }
        this.moreStatus=false;
      })
    },
    getFocus(){
      this.$els.search.focus()
    },
    selectOptionId(Id) {
      if(!Id){
        return false
      }
      this.option.forEach( (item) => {
        if(item.id == Id){
          this.selectOption(item)
        }
      })
    },
    filterData(){ //多选,过滤已选
      if(!this.multiple){
        return
      }
      var Op = this.option
      var Se = this.selected
      this.filterOption = []
      var selectList = []
      for(let s in Se){
        selectList.push(Se[s].id)
      }
      for(let o in Op){
        if(selectList.includes(Op[o].id) == false){
          this.filterOption.push(Op[o])
        }
      }
    },
    getData(){
      var self = this
      if(!this.url){
        return false
      }
      if(this.type == 'get'){
        if(this.more){this.params.page=this.page;this.params.all=0}
        this.$http.get(this.url, this.params).then(function (response) {
          self.option = response.data.items
          self.selected = response.data.items[0]
        })
      }else {
        if(this.more){this.params.page=this.page;this.params.all=0;this.params.page_size=10}
        this.$http.post(this.url, this.params).then(function (response) {
          self.option = response.data.items
          self.selected = response.data.items[0]
        })
      }
    },
    open(){
      this.filterData()
      this.search = '';
      this.show = true;
    },
    change(){},
    close(){
      this.show = false
    },
    addSelect(o){
      this.selected.push(o)
      this.filterData()
    },
    delSelect(o){
      this.selected.$remove(o)
      this.filterData()
    },
    selectOption(o){
      if(o==this.selected){
        return false
      }
      this.selected= o
      this.selectId= o.id
      this.$dispatch('change', o)
      this.close()
    },
  },
  watch: {
    'url': function (val, oldval) {
      this.getData()
    },
    'params': function (val, oldval) {
      this.getData()
    },
    'selectId': function (val, oldval) {
      if (val) {
        this.selectOptionId(this.selectId)
      }
    },
    'selected': function (val, oldval) {
      this.selectOption(val)
    },
    'option':function () {
      this.selectOptionId(this.selectId)
      if(this.option && this.option.length>10){
        slimFunc()
        function slimFunc(){
          $('.select-box').slimScroll({
            height: '210',
            position: 'right',
            size: "5px",
            color: '#7e9fd0',
            wheelStep: 5
          })
        }
        $(window).resize(function() {
          slimFunc()
        })
      }
    },
  }
}
</script>
