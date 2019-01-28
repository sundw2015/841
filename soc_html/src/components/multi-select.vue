<template>
  <div class="ys-multi-select">
    <div class="leftText">{{left}}</div>
    <div class="leftSelect">
      <ul>
        <template v-for="list in dataList">
          <li @click="addToSel(list,$index)" class="line">{{list.name}}</li>
        </template>
      </ul>
    </div>
    <div class="changeIcon"><i class="md md-swap-horiz"></i></div>
    <div class="rightText">已选</div>
    <div class="rightSelect">
      <ul>
        <template v-for="list in selected">
          <li @click="returnList(list,$index)" class="line">{{list.name}}</li>
        </template>
      </ul>
    </div>
    <div class="clearfix"></div>
  </div>
</template>
<style scoped>
  .ys-multi-select{
    display: inline-block;
  }
  .ys-multi-select>div{
    float:left;
    display: inline-block;
  }
  .ys-multi-select .leftText,.ys-multi-select .rightText{
    padding-right:13px;
  }
  .ys-multi-select .leftText{
    width:115px;
    text-align:right;
  }
  .leftSelect,.rightSelect{
    width:220px;
    height:400px;
    border: 1px solid #808080;
    border-radius: 3px;
    color: #000;
    padding: 12px 2px 12px 12px;
  }
  .changeIcon{
    text-align: center;
    line-height:400px;
    font-size: 38px;
    margin-left: 20px;
    margin-right: -8px;
    color: #369eef;
  }
  .ys-multi-select .line{
    line-height:22px;
  }
  .ys-multi-select .line:hover{
    cursor:pointer;
    color:#c4bdd2;
  }
</style>
<script>
  export default {
    props: {
      left: {
        default: '选择列表'
      },
      option: Array,
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
        default:{}
      },
      selected:{
        default : function () {
          return {}
        }
      },
    },
    data () {
      return {
      }
    },
    ready(){
      let self=this
      if(this.url){
        this.getData()
      }
      this.slimFunc()
      $(window).resize(function() {
        self.slimFunc()
      })
    },
    methods:{
      slimFunc(){
        $('.leftSelect>ul').slimScroll({
          height: '390',
          position: 'right',
          size: "5px",
          color: '#000',
          wheelStep: 5
        })
        $('.rightSelect>ul').slimScroll({
          height: '390',
          position: 'right',
          size: "5px",
          color: '#000',
          wheelStep: 5
        })
      },
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
      addToSel(list,index){
        this.selected.push(list)
        this.dataList.splice(index,1);
      },
      returnList(list,index){
        this.dataList.push(list)
        this.selected.splice(index,1);
      },
      open(){
        this.filterData()
        var self = this
        if (this.show) return
        this.search = ''
        this.show = true
        if(this.color=="ys-select-input" || this.color=="ys-select-input-bg"){
          this.inputHigh=1
        }
        setTimeout(function () {
          self.$els.search.focus()
        }, 300)
      },
      change(){

      },
      close(){
        this.searchable = false
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
    },
    watch: {
      'url': function () {
        this.getData()
      },
      'params':function(){
        this.getData()
      }
    }
  }
</script>