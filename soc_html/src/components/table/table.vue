
<style scoped>
  .ys-table-foot {
    line-height: 40px;
    padding-left: 10px;
    background: rgba(0, 0, 0, 0.4);
    border-radius: 3px;
  }
  .loading {
    background: rgba(0, 0, 0, 0.25);
    color: #f2f2f2;
    height: 40px;
  }
</style>
<script>
  import Api from 'src/lib/api'
  export default {
    props: {
      url: {
        required: true
      },
      search: {
        default: ""
      },
      filter: {
        default: function () {
          return []
        }
      },
      scroll: {
        default: false
      },
      server: {
        // 服务端分页模式， 默认开启
        default: true
      },
      data: {
        default: function () {
          return []
        }
      }
    },
    data () {
      let randomId = Math.random().toString(16).substr(2);
      return {
        loading: false,
        randomId: randomId,
        wrapperClass: randomId + 'wrapperClass',
        loadIngId: randomId + 'loadIngId',
        NoDataId: randomId + 'NoDataId',
        tableList:[],
        total: 0,

        // 分页
        tableStart: 0,
        tableLength: 30,
        tablePage: 0,
        tableTotal: 0,
        timer: {}
      }
    },
    ready(){
      this.initTable()
      if (this.scroll) {
        this.setScroll()
      }
    },
    methods:{
      fetchData(collback){
        this.setLoading()
        let data = {}
        if (this.server) {
          let data = {
            "start": this.tableStart,
            "length": this.tableLength,
            "order[0][column]": 1,
            "order[0][dir]": "desc",
            "search[value]": this.search,
          }
          for (let i in this.filter) {
            data[i] = this.filter[i].id
          }
          let resource = this.$resource(this.url)
          resource.save(data).then(function (response) {
            for(let x in response.data.data){
              response.data.data[x].selected=false
            }
            this.removeLoading()
            this.tableTotal = response.data.recordsFiltered
            this.tablePage = this.tableTotal % this.tableLength == 0 ? this.tableTotal / this.tableLength : Math.floor(this.tableTotal / this.tableLength) + 1
            collback(response.data.data)
          },function (response) {
            console.log('remove')
            this.removeLoading()
          }, function (response) {
            Api.user.requestFalse(response)
          })
        }
        else {
          let d = this.data.slice(this.tableStart, this.tableStart+this.tableLength)
          collback(d)
        }

      },
      initTable(){
        let self = this
        let data = this.fetchData(function (data) {
          self.tableList = data
        })
      },
      Re(){
          this.tableStart = 0
          this.initTable()
          this.setHeight(380)
        },
      changePage(page){
        if(page >=0 && this.tablePage>page){
          this.tableStart = page*10
          this.initTable()
        }

      },
      changeEdit(id){
          this.editId = id
        },
      loadMore(){
        let self = this
        this.tableStart = this.tableList.length
        if (this.tableStart == this.tableTotal) { // 到底了
          return
        }
        let data = this.fetchData(function (data) {
          data.forEach(function (d) {
            self.tableList.push(d)
          })
          self.$dispatch('load-more')

        })
      },
      // 滚动加载
      setScroll () {
        let self = this
        $('.table-body').slimScroll({
          height: '38px',
          position: 'right',
          size: "5px",
          wheelStep: 5,
          wrapperClass: self.wrapperClass
        }).bind('slimscroll', function (e, pos) {
          self.loadMore()
        }).bind('DOMNodeInserted', function () {
          self.delay_till_last(self, 'tableResize', function() {
              self.tableResize()
          }, 100);
        }).bind('DOMNodeRemoved', function () {
          self.delay_till_last(self, 'tableResize', function() {
              self.tableResize()
          }, 100);
        })
      },
      tableResize(){
        let self = this
        let h = 0
        for (let i = 0; i < $(".table-body tr").length; i++) {
          h += $(".table-body tr").eq(i).height()
        }
        let max_height = this.getClientHeight() - 220
        let height = h - 35
        if (height > max_height) {
          height = max_height
        }
        if (height < 38) {
          height = 40
        }
        this.setHeight(height)
        if (self.tableList.length > 0) {
          self.removeNoData()
          for (var i = 0; i < $("#ys-table-body thead tr").find("th").length; i++) {
            $("#ys-table-head tr th").eq(i).width($("#ys-table-body thead tr").find("th").eq(i).width());
          }
        } else {
          self.setNoData()
        }
      },
      delay_till_last(self, id, fn, wait) {
          if (self.timer[id]) {
              window.clearTimeout(self.timer[id])
              delete self.timer[id]
          }
          return self.timer[id] = window.setTimeout(function() {
              fn()
              delete self.timer[id]
          }, wait)
      },
      getClientHeight() {
        let clientHeight = 0
        //获取窗口高度
        if (window.innerHeight) {
          clientHeight = window.innerHeight
        } else if ((document.body) && (document.body.clientHeight)) {
          clientHeight = document.body.clientHeight
        }
        return clientHeight
      },
      setHeight(height){
        $('.table-body').height(height)
        $('.' + this.wrapperClass).height(height)
      },
      setLoading () {
        let self = this
        if($('#'+ self.loadIngId).length > 0){
          return
        }
        $('.table-body').prepend(
          '<div class="loading textC" id="'+ self.loadIngId +'">' +
            '<div class="font12">' +
              '<i class="fa fa-spin fa-cog m-r-5 font16 verticalM" ></i>加载中...' +
            '</div>'+
          '</div>'
        )
      },
      setNoData(){
        let self = this
        if($('#'+ self.NoDataId).length > 0){
          return
        }
        $('.table-body').prepend(
          '<div class="loading textC" id="'+ self.NoDataId +'">' +
            '<div class="font12">查询不到任何相关数据</div>' +
          '</div>'
        )
      },
      removeNoData(){
        let self = this
        $('#' + self.NoDataId).remove()
      },
      removeLoading(){
        let self = this
        $('#' + self.loadIngId).remove()
      }

    },
    components: {
      Api,
    },
    watch: {
      tableList () {

      }
    }
  }
</script>
