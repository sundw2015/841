<template>
  <poptip @click="on=true" @on-popper-hide="on=false" :placement="'bottom'">
  <i class="glyphicon glyphicon-filter" v-bind:class="{on: selected}"></i>
  <div slot="content">
   <ul>
    <li v-for="item in option" class="select-option"
        v-bind:class="{'select-option-on': selected==item}"
        @click="selItem(item)">{{ item.name}}</li>
   </ul>
  </div>
 </poptip>
</template>

<style scoped>
 .on {
  color: rgba(44,126,191,0.75);
 }
 .select-option-on {
    color:#f2f2f2;
    background:#369eef;
 }
 .select-option{
    min-width: 100px;
    color:#f2f2f2;
    padding-left:5px;
    height:26px;
    line-height:26px;
    cursor: pointer;
    overflow: hidden;
  }
  .select-option:hover{
    color:#f2f2f2;
    background:#369eef;
  }
</style>
<script>
  import Api from 'src/lib/api'
  import poptip from './poptip.vue'
  export default {
    props: {
      option: {
        type: Array,
        default: function () {
          return []
        }
      },
      multiple: { //多选
        default: false
      },
      url: { // 请求接口
        default: false
      }
    },
    data () {
      return {
        on: false,
        selected: false
      }
    },
    computed: {
    },
    ready: function () {
      this.url && this.fetchOption()
    },
    methods: {
      selItem(item) {
        if(this.selected == item){
          this.selected = false
          this.$dispatch('change', {"id":0})
        }else {
          this.selected=item
          this.$dispatch('change', item)
        }
      },
      fetchOption(){
        this.$http.post(this.url, {'all': 1}).then(function (response) {
          this.option = response.data.items
        }, function (response) {
          Api.user.requestFalse(response)
        })
      }
    },
    components: {
      poptip
    }

  }
</script>