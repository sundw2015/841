<template type="text/template" id="template_pagination">
  <section class="pages-wrap" v-bind:class="[place=='center' ? 'textC' : 'textR']">
    <ul class="pagination clearfix">
      <li v-if="jumpStatus">
        <span class="jumpText">跳转到第</span>
        <input class="jumpPage" type="number" @keyup.13="goJump" placeholder="页数" v-model.number="jumpPage"/>
        <a class="jumpGo" @click="goJump()">GO</a>
      </li>
      <li :class="{'disabled': pageInfo.current == 1}" v-if="pageInfo.current != 1"><a href="javascript:;" class="ys-page-num" @click="clickCurrent(1)" style="margin-right:10px;"> <i class="ys-icon icon-prev"></i> </a></li>
      <li :class="{'disabled': pageInfo.current == 1}" v-if="pageInfo.current != 1"><a href="javascript:;" class="ys-page-num" @click="clickCurrent(pageInfo.current - 1)"> <i class="ys-icon icon-arrow-left"></i></a></li>
      <li v-for="p in setList" :class="{'active': pageInfo.current == p.val}" >
        <a href="javascript:;" class="ys-page-num" v-if="pageInfo.current == p.val" class="on" @click="clickCurrent(p.val)"> {{ p.text }} </a>
        <a href="javascript:;" class="ys-page-num" v-else  @click="clickCurrent(p.val)"> {{ p.text }} </a>
      </li>
      <li :class="{'disabled': pageInfo.current == pageInfo.page}" v-if="page !=1 "><a href="javascript:;" class="ys-page-num" @click="clickCurrent(pageInfo.current + 1)"> <i class="ys-icon icon-arrow-right"></i></a></li>
      <li :class="{'disabled': pageInfo.current == pageInfo.page}" v-if="page !=1 "><a href="javascript:;" class="ys-page-num" @click="clickCurrent(pageInfo.page)" style="margin-left:10px;"> <i class="ys-icon icon-next"></i> </a></li>
      <li v-if="editPage">
        <input class="jumpPage m-l-3" type="number" @input="changeNumber" @keyup.13="change" @change="changeNumber" v-model.number="tableLength"
               placeholder="条数"><span class="d-i-b verticalM m-l-3">条/页</span>
      </li>
    </ul>
  </section>
</template>
<script>
  import Vue from 'vue'
  export default {
    props:['pageInfo','jumpStatus','place','tableLength','editPage'],
    computed: {
      page:function() {
        return Math.ceil(this.pageInfo.total / this.pageInfo.pagenum);
      },
      setList:function(){
        var len = this.page , temp = [], list = [], count = Math.floor(this.pageInfo.pagegroup / 2) ,center = this.pageInfo.current;
        if( len <= this.pageInfo.pagegroup ){
          while(len--){ temp.push({text:this.page-len,val:this.page-len});};
          return temp;
        }
        while(len--){ temp.push(this.page - len);};
        var idx = temp.indexOf(center);
        (idx < count) && ( center = center + count - idx);
        (this.pageInfo.current > this.page - count) && ( center = this.page - count);
        temp = temp.splice(center - count -1, this.pageInfo.pagegroup);
        do {
          var t = temp.shift();
          list.push({
            text: t,
            val: t
          });
        }while(temp.length);
        if( this.page > this.pageInfo.pagegroup ){
          (this.pageInfo.current > count + 1) && list.unshift({ text:'...',val: list[0].val - 1 });
          (this.pageInfo.current < this.page - count) && list.push({ text:'...',val: list[list.length - 1].val + 1 });
        }
        return list;
      }
    },
    created:function (argument) {
    },
    data () {
      return {
        jumpPage:""
      }
    },
    ready(){
    },
    methods: {
        change(){
            this.$emit('table',this.tableLength);
        },
        changeNumber:function(){
            if(parseInt(this.tableLength)<=1){
                this.tableLength = 1;
            }else if(parseInt(this.tableLength)>=50){
                this.tableLength = 50;
            }
        },
      clickCurrent: function(idx) {
        if( this.pageInfo.current != idx && idx > 0 && idx < this.page + 1) {
          this.pageInfo.current = Number(idx);
          this.$emit('change',this.pageInfo.current);
        }
      },
      goJump:function(){
        if(this.jumpPage>this.pageInfo.page){
          this.jumpPage=this.pageInfo.page
        }else if(this.jumpPage<1){
          this.jumpPage=1
        }else{
          this.clickCurrent(this.jumpPage)
        }
      }
    }
  }
</script>
<style scoped>
  .pages-wrap {
    text-align: right;
  }
  .pagination {
    display: inline-block;
    padding-left: 0;
    margin-top:8px;
    border-radius: 4px;
  }
  .pagination>li {
    display: inline;
  }
  .pagination>.active>a, .pagination>.active>a:hover, .pagination>.active>span,  .pagination>.active>span:hover {
    z-index: 3;
    color: #fff;
    cursor: default;
    background-color: #337ab7;
  }
  .pagination>.disabled>a, .pagination>.disabled>a:hover, .pagination>.disabled>span, .pagination>.disabled>span:hover {
    color: #777;
    cursor: not-allowed;
    background-color: rgba(0,0,0,0.2);
  }
  .pagination>li>a:hover,.pagination>li>span:hover {
    z-index: 2;
    color: #fff;
    background-color: rgba(74,146,255,0.2);
    transition-property: width, height, background-color, opacity, left, border-color, color;
    transition-duration: 300ms;
  }
  .pagination>li>a, .pagination>li>span {
    position: relative;
    float: left;
    padding: 0px 9px;
    height:26px;
    line-height: 26px;
    color: #4a92ff;
    text-decoration: none;
    background-color: rgba(0,0,0,0.2);
    border:none;
    margin:0px 2px;
    border-radius: 3px;
  }
  .pagination .active a.on{
    background:#4a92ff;
    color:#fff;
  }
  .pagination .active a.on:hover{
    color: #fff!important;
    background: #4a92ff!important;
  }
  .jumpText{
    background: none!important;
    color:#6591d2!important;
    padding-right:3px!important;
  }
  .jumpText:hover{
    background: none!important;
    color:#6591d2!important;
  }
  .jumpPage{
    width:44px;
    border:none;
    float:left;
    background: rgba(0,0,0,0.2);
    padding:0px 3px 0px 3px;
    height:26px;
    border-radius: 3px;
    line-height: 26px;
  }
</style>