<template>
  <div class="select-con"
       v-clickoutside="close"
       v-bind:style="{width: width + 'px'}"
       v-bind:class="color">
    <div class="select-input" v-bind:class="[inputHigh==1 ? 'input-high' : '' ]">
      <input type="text" class="b-b-n ys-input" v-model="selected.name" style="width:100%" autofocus="autofocus">
      <div class="select-open-icon">
        <i @click="show ? close() : open()" class="md" v-bind:class="[show ? 'md-arrow-drop-up' : 'md-arrow-drop-down' ]"></i>
      </div>
    </div>
    <div v-show="show"
         class="select-body"
         transition="slide">
      <div class="select-box">
        <div class="select-option"
             v-for="o in option | filterBy search in 'name'"
             rack-by="$index"
             onmousedown="event.preventDefault()"
             @click="selectOption(o)"
             v-bind:class="[selected.id==o.id ? 'cur-select' : '' ]"
        >{{ o.name }}</div>
      </div>
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
  .ys-select-input .select-input:focus{
    border:1px solid red!important;
  }
  .select-con{
    display: inline-block;
    position: relative;
  }
  .ys-select-td .select-input{
    color:#f2f2f2;
    background:none;
  }
  .ys-select-fil .select-input{
    background: none;
    border: 1px solid #808080;
    color:#f2f2f2;
  }
  .ys-select-input .select-input{
    background: none;
    border: 1px solid #808080;
    color:#f2f2f2;
   }
  .ys-select-input-bg .select-input{
    background: none;
    border: 1px solid #808080;
    color:#f2f2f2;
  }
  .input-high{
    background:none;
    border: 1px solid #369eef!important;
    color:#c4bdd2!important;
  }
  .ys-select-modal .select-input{
    background: none;
    border: 1px solid #808080;
    color:#f2f2f2;
  }
  .select-input {
    width:100%;
    height: 30px;
    line-height: 30px;
    border-radius: 3px;
  }
  .select-input p{display: inline-block}
  .select-open-icon{
    position:relative;
  }
  .ys-select-fil .select-open-icon i{
    color:#f2f2f2;
  }
  .ys-select-input .select-open-icon i{
    color:#f2f2f2;
  }
  .ys-select-input-bg .select-open-icon i{
    color:#f2f2f2;
  }

  .ys-select-modal .select-open-icon i{
    color:#f2f2f2;
  }
  .select-open-icon i{
    position:absolute;
    right:5px;
    top:-28px;
    font-size:22px;
  }
  .select-body{
    width: 100%;
    position: absolute;
    z-index:3;
    top:32px;
    left:0px;
    background:rgba(0, 0, 0, 0.75);
    border:1px solid #c4bdd2;
    border-top:none;
    border-radius: 3px;
  }
  .select-box {
    margin-top:10px;
    width: 100%;
    padding-bottom:10px;
  }
  .select-option{
    padding-left:5px;
    height:26px;
    line-height:26px;
    cursor: pointer;
  }
  .select-option:hover{
    color:#f2f2f2;
    background:#369eef;
  }
</style>
<script>
  import clickoutside from 'src/directives/clickoutside';
  export default {
    directives: { clickoutside },
    props: {
      option: Array,
      url: {
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
      width: {
        default: 150
      },
      color: {
        default: "ys-select-td"
      },
      selected: {
        default : function () {
          return {
        }
        }
      },
      placeholder: {
        default: '未设置'
      },
    },
    data () {
      return {
        show: false,
        filterOption: [],
        inputHigh:0
      }
    },
    ready(){
      if(this.url){
        this.getData()
      }
      slimFunc()
      function slimFunc(){
        $('.select-box').slimScroll({
          height: '145',
          position: 'right',
          size: "5px",
          color: '#000',
          wheelStep: 5
        })
      }
      $(window).resize(function() {
        slimFunc()
      })
    },
    methods:{
      filterData(){ //多选,过滤已选
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
        if(this.type == 'get'){
          this.$http.get(this.url, this.params).then(function (response) {
            self.option = response.data.items
          })
        }else {
          this.$http.post(this.url, this.params).then(function (response) {
            self.option = response.data.items
          })
        }
      },
      open(){
        this.filterData()
        if (this.show) return
        this.show = true
        if(this.color=="ys-select-input" || this.color=="ys-select-input-bg"){
          this.inputHigh=1
        }
      },
      change(){

      },
      close(){
        this.show = false
        if(this.color=="ys-select-input" || this.color=="ys-select-input-bg"){
          this.inputHigh=0
        }
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
        this.selected= o
        this.$dispatch('change', o)
        this.close()
      },
      highLight(){
      }
    },
    watch: {
      'url': function (val, oldval) {
        this.getData()
      },
      'params': function (val, oldval) {
        this.getData()
      }
    }
  }
</script>
