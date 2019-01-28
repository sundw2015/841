<template>
  <div class="select-con verticalM"
       tabindex="0"
       onmousedown="event.preventDefault()"
       @keyup.esc="close()"
       @blur="searchable ? false : close()"
       v-el:con
       v-bind:style="{width: width + 'px'}"
  >
    <div class="select-input">
      <div class="select-open-icon">
        <i @click="show ? close() : open()" class="md md-arrow-drop-down select-arrow" v-bind:class="[show ? 'arrow-rotate' : '' ]"></i>
      </div>
      <div v-if="selected.name"
           @click="show ? close() : open()"
           class="select-text">
        <i class="md md-location-on verticalM font16 m-r-3"></i>{{ selected.name }}
      </div>
      <div v-else
           @click="show ? close() : open()"
           class="select-text">{{ placeholder }}
      </div>
    </div>
    <div v-show="show"
         class="select-body">
      <div class="select-box">
        <div class="select-option"
             v-for="o in option | filterBy search in 'name'"
             rack-by="$index"
             onmousedown="event.preventDefault()"
             @click="selectOption(o)"
             v-bind:class="[selected.id==o.id ? 'cur-select' : '' ]">{{ o.name }}</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .arrow-rotate{
    transform: rotate(180deg);
  }
  .select-arrow{
    transition: all .3s ease-in-out;
  }
  .select-con{
    display: inline-block;
    position: relative;
  }
  .select-input {
    width:100%;
    height: 30px;
    line-height: 30px;
    padding-left: 20px;
    border-radius: 3px;
    background:none;
    color:#f2f2f2;
  }
  .select-input p{
    margin-right:22px;
    width:100%;
  }
  .select-input .select-open-icon{
    float:right;
    width:20px;
    height:30px;
  }
  .select-open-icon{
    position:relative;
  }
  .select-open-icon i{
    position:absolute;
    right:3px;
    top:-1px;
    font-size:22px;
    cursor:pointer;
    color:#f2f2f2;
  }
  .select-text{
    overflow: hidden;
    height:30px;
    line-height: 27px;
    padding-right:10px;
  }

  .select-body{
    width:156px;
    padding-bottom:10px;
    position: absolute;
    z-index:3;
    top:30px;
    left:20px;
    transform-origin: center top 0px;
    background:rgba(0, 0, 0, 0.75);
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
    overflow: hidden;
    color:#f2f2f2;
  }

  .select-option:hover{
    color:#fff;
    background:#369eef;
  }

  .cur-select{
    color:#fff;
    background:#369eef;
  }
</style>
<script>
export default {
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
      default: ""
    },
    selected: {
      default : function () {
        return {}
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
    }
  },
  ready(){
    if(this.url){
      this.getData()
    }
    slimFunc()
    function slimFunc(){
      $('.select-box').slimScroll({
        height: '210',
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
      var self = this
      if (this.show) return
      this.show = true
    },
    change(){},
    close(){
      this.show = false
    },
    selectOption(o){
      this.selected= o
      this.$dispatch('change', o)
      this.close()
    },
    highLight(){}
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
