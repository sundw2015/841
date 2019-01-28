<template>
  <div class="textC">
      <div class="loading"
           v-show="loading && loadSet"
           v-bind:style="{ height: 38*tableLength + 'px', lineHeight: 38*tableLength + 'px' }">
        <div class="font12">
          <loading-normal :show.sync="loading"></loading-normal>
        </div>
      </div>
      <div class="table-empty" v-show="data.length == 0 && loading == false">
        <div v-bind:style="{ height: 38*tableEmptyLength + 'px', lineHeight: 38*tableEmptyLength + 'px' }">
          <span class="ys-info-color"><i class="ys-icon icon-info-outline m-r-5"></i>查询不到相关数据</span>
        </div>
      </div>
      <div v-if="!all">
        <pagination :page-info="pageInfo"
                    :jump-status="jump"
                    :edit-page="editPage"
                    :table-length.sync="tableLength"
                    :place="pagePlace"
                    @table="initTable"
                    @change="changePage"></pagination>
      </div>
    </div>
</template>
<style scoped>
  .loading {
    background: rgba(0, 0, 0, 0.2);
    color: #f2f2f2;
    height: 40px;
    line-height:40px;
  }
  .table-empty>div{
    background: rgba(0, 0, 0, 0.2);
    height:36px;
    line-height:36px;
    margin-bottom:2px;
  }
</style>

<script>
import Api from 'src/lib/api'
import loadingNormal from 'src/components/loading-normal.vue'
import pagination from 'src/components/page.vue'
export default {
  name: 'table-data',
  props: {
    url: {
      default: false,
      toway: true
    },
    data: {
      required: true
    },
    whole: {
      default: 0
    },
    search: {
      default: ""
    },
    filter: {
      default: function () {
        return []
      }
    },
    tableLength:{
      default: 10,
    },
    all:{
      default: false,
    },
    jump:{
      default: true,
    },
      editPage:{
         default: false,
      },
    pagePlace:{
      default: "right",
    },
    loadSet:{
      default: true,
    },
    hand:{
      default:true
    }
  },
  computed: {
    tableEmptyLength:function(){
      if(this.tableLength==-1){
        return 10
      }else{
        return this.tableLength
      }
    },
  },
  data () {
    return {
      total: 0,

      // 分页
      tableStart: 0,
      tablePage: 0,
      tableTotal: 0,

      loading: true,

      pageInfo:{
        total:0,  // 记录总条数   默认空，如果小于pageNum则组件不显示   类型Number
        current:1,  // 当前页数，   默认为1                             类型Number
        pagenum:10, // 每页显示条数,默认10                              类型Number
        pagegroup:5,    // 分页条数     默认为5，需传入奇数                 类型Number
      },
      searchStatus:false
    }
  },
  ready(){
    if(!this.url){
      return
    }
    if(this.hand){
      this.initTable()
    }
  },
  methods:{
    showPage(page){
      var now_page = this.tableStart/this.tableLength
      if((page - now_page) > -3 && (page - now_page) < 3){
        return true
      }
      if(now_page < 3 && page < 5){
          return true
      }
      if((this.tablePage-page)<6 && (now_page - page) > 2){
        return true
      }

    },
    initTable(){
      if(this.all){this.tableLength=-1}
      var data = {
          "start": this.tableStart,
          "length": parseInt(this.tableLength),
          "order[0][column]": 1,
          "order[0][dir]": "desc",
          "search[value]": this.search,
        }
        let num = 0;
        for(let i in this.filter){
          data[i] = this.filter[i].id
          if(this.filter[i].id){
            num++
          }
        }
        // if( num>0 || this.search!=""){
        //   this.tableStart=0
        //   data.start=0
        // }

        if(this.url){
          var resource = this.$resource(this.url);
          this.data = []
          this.loading = true;
          this.pageInfo.pagenum=this.tableLength;
          resource.save(data).then(function (response) {
            this.loading = false
              if(response.data.status == '500'){
                this.$root.alertError = true;
                this.$root.errorMsg = response.data.msg;
                return false;
              }
            for(let x in response.data.data){
              response.data.data[x].selected=false
            }
            this.data = response.data.data
            this.whole=response.data.recordsTotal
            this.tableTotal = response.data.recordsFiltered
            if(response.data.recordsTotal==response.data.recordsFiltered){
              this.tableTotal=response.data.recordsTotal;
            }else if(response.data.recordsFiltered<response.data.recordsTotal){
              this.tableTotal=response.data.recordsFiltered;
            }
            this.tablePage= this.tableTotal % this.tableLength==0 ? this.tableTotal/this.tableLength : Math.floor(this.tableTotal/this.tableLength)+1;

            if(response.data.recordsTotal==response.data.recordsFiltered){
              this.pageInfo.total=response.data.recordsTotal;
            }else if(response.data.recordsFiltered<response.data.recordsTotal){
              this.pageInfo.total=response.data.recordsFiltered;
            }

            this.pageInfo.page=this.tablePage;
                //start 此情况下start为-10 故注释
//            if(this.data.length==0 && response.data.recordsTotal>0){
//              this.tableStart=this.tableStart-this.tableLength;
//              this.pageInfo.current=this.pageInfo.current-1;
//              this.initTable()
//            }//删除时 往回倒一页

          },function (response) {
            Api.user.requestFalse(response,this);
          })
        }else {
            this.tableTotal = this.data.length
            this.tablePage= this.tableTotal % this.tableLength==0 ? this.tableTotal/this.tableLength : Math.floor(this.tableTotal/this.tableLength)+1
        }

    },
    Re(url){
      if(url){
        this.url=url;
      }
      this.initTable()
    },
    Download(download_numbers){
        var data = {
          "start": this.tableStart,
          "length": this.tableLength,
          "order[0][column]": 1,
          "order[0][dir]": "desc",
          "search[value]": this.search,
        }
        for(let i in this.filter){
          data[i] = this.filter[i].id
        }
        data["dts_download"] = 1;
        data["download_numbers"] = download_numbers
        var json_data = JSON.stringify(data);
        this.$http.post(this.url, json_data).then(function (response) {
          if(response.data.status==200){
            var file_path = response.data.file_path;
            this.$root.alertSuccess=true;
            window.open(file_path);
          }else{
            this.$root.alertError=true;
          }
          this.$root.errorMsg=response.data.msg;
        },function(response){
          Api.user.requestFalse(response,this);
        });

      },
    changePage(page){
      var page=page-1;
      if(page >=0 && this.tablePage>page){
        this.tableStart = page*this.tableLength
        this.initTable()
      }
    },
    changeEdit(id){
        this.editId = id
      }
  },
  components:{
    loadingNormal,
    pagination
  }
}
</script>