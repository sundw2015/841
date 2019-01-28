<template>
  <div class="domain-select-con"
       onmousedown="event.preventDefault()"
       v-clickoutside="close"
       v-el:con>
    <div class="select-input"
         v-bind:class="[show ? 'select-focus' : '' ]"
         @click="show ? close() : open()" >
      <div class="select-open-icon">
        <i class="ys-icon select-arrow icon-arrow-filter" v-bind:class="[show ? 'arrow-rotate' : '' ]"></i>
      </div>
      <span class="select-text" v-if="empty">未添加域名</span>
      <span class="select-text" v-else>{{curDomain.domain}}</span>
    </div>
    <div v-show="show"
         class="select-body"
         transition="slide">
      <div class="select-edit-box m-t-15">
        <input v-model="search"
               v-el:search
               class="ys-input"
               onmousedown="event.preventDefault()"/>
        <i class="glyphicon glyphicon-search search-btn"></i>
      </div>
      <div class="domain-select-box m-t-20">
        <div class="ys-row clearfix">
          <div class="col-md-6" v-for="domain in domainData.checkin | filterBy search in 'domain'">
            <div class="domain-box m-b-10 pos-r">
              <div class="domain-select-box-tag"
                   v-bind:class="domain.status_class">{{domain.status | statusFil}}</div>
              <div class="domain-box-con clearfix">
                <div style="float:left;width:145px;">
                  <div class="website-img m-l-10 textC m-t-5">
                    <span v-if="domain.screenshot==''">?</span>
                    <img v-else v-bind:src="domain.screenshot"/>
                  </div>
                </div>
                <div style="margin-left:150px;">
                  <p class="domain-box-title m-t-5 m-l-10">{{domain.domain}}</p>
                  <table class="m-t-10 m-l-10">
                    <tbody>
                    <tr>
                      <td class="ellipsis">服务套餐：</td>
                      <td class="ellipsis"><span>{{domain.service.server_name}}</span></td>
                    </tr>
                    <tr>
                      <td class="ellipsis">服务剩余期限：</td>
                      <td class="ellipsis"><span class="bold">{{domain.service.left_days}}天</span></td>
                    </tr>
                    </tbody>
                  </table>
                  <p class="m-t-10 m-l-10"><button class="ys-btn" @click="selectDomain(domain)">选择此域名</button></p>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6" v-for="domain in domainData.no_checkin | filterBy search in 'domain'">
            <div class="domain-box m-b-10 pos-r">
              <div class="domain-select-box-tag"
                   v-bind:class="domain.status_class">{{domain.status | statusFil}}</div>
              <div class="domain-box-con clearfix pos-r">
                <div style="float:left;width:145px;">
                  <div class="website-img m-l-10 textC m-t-5">
                    <span v-if="domain.screenshot==''">?</span>
                    <img v-else v-bind:src="domain.screenshot"/>
                  </div>
                </div>
                <div style="margin-left:150px;">
                  <p class="domain-box-title m-t-5 m-l-10">{{domain.domain}}</p>
                  <table class="m-t-10 m-l-10">
                    <tbody>
                    <tr>
                      <td>建议操作：</td>
                      <td v-if="domain.status==-4"><a @click="">提醒审核</a></td>
                      <td v-if="domain.status==4"><a @click="">切入</a></td>
                      <td v-if="domain.status!=4 && domain.status!=-4"><a @click="selJumpDomain(domain)">继续完成向导</a></td>
                    </tr>
                    </tbody>
                  </table>
                  <p class="m-t-20 m-l-10" v-if="domain.status!=3"><button class="ys-btn" @click="selectDomain(domain)">选择此域名</button></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <template v-if="empty">
    <button class="ys-btn m-l-10" v-link="{name:'domain-add'}">
      <i class="md md-add-circle-outline"></i>添加域名
    </button>
  </template>
  <template v-else>
    <a @click="delDomainStatus=!delDomainStatus" v-if="showDelStatus"><i class="ys-icon icon-trash m-l-5 font14"></i></a>
    <div class="d-i-b m-l-5">
      <div class="ys-tag m-l-10 fadeInLeft animated" v-if="curDomain.type==0">NS切入方式</div>
      <div class="ys-tag m-l-10 fadeInLeft animated" v-if="curDomain.type==1">CNAME切入方式</div>
      <div class="ys-tag m-l-10 fadeInLeft animated"
           v-if="curDomain.status==1 || curDomain.status==2 || curDomain.status==12">{{curDomain.service.server_name}}套餐</div>
      <div class="ys-tag m-l-10 fadeInLeft animated"
           v-if="curDomain.status==1 || curDomain.status==2 || curDomain.status==12">剩余服务天数{{curDomain.service.left_days}}天</div>
    </div>
  </template>
  <div class="tool-box tool-box-s" v-if="!curDomain.checkin && !empty">
    <section>
      <span v-if="curDomain.status==-4">
        当前域名的状态是等待审核，建议操作：<a @click="">提醒审核</a>
      </span>
      <span v-if="curDomain.status==4">
        当前域名的状态是未切入，建议操作：<a>切入</a>
      </span>
      <span v-if="curDomain.status==5">
        当前域名的状态是审核不通过
      </span>
      <span v-if="curDomain.status==3">
        当前域名没有完成切入向导，无法享受抗D服务，您可以选择 <a @click="selJumpDomain(curDomain)">进入切入向导</a>
      </span>
      <span v-if="curDomain.status!=-4 && curDomain.status!=4 && curDomain.status!=5 && curDomain.status!=3">
        当前域名没有完成切入向导，无法享受抗D服务，您可以选择 <a @click="selJumpDomain(curDomain)">进入切入向导</a>
      </span>
    </section>
  </div>
  <ys-modal :show.sync="delDomainStatus" :title="'请注意'" :width="'400px'">
    <div slot="content">
      <p>如果您删除该域名，您域名下的所有记录、配置选项和保护状态都会被删除。</p>
      <p class="m-t-20">您确定删除域名 <span class="ys-success-color">{{curDomain.domain}}</span> 吗？</p>
    </div>
    <div slot="footer">
      <button class="ys-btn" type="button">
        <span @click="delDomain()">确定</span>
      </button>
      <button class="ys-btn ys-btn-white m-l-10" type="button">
        <span @click="delDomainStatus=false">取消</span>
      </button>
    </div>
  </ys-modal>
</template>
<style scoped>
  .ellipsis {
    width: inherit;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .ys-tag{
    position:relative;
    background:rgba(74,146,255,0.4);
    background:linear-gradient(-135deg,transparent 10px,rgba(74,146,255,0.4) 0);
    border-top-left-radius:3px;
    border-bottom-right-radius:3px;
    border-bottom-left-radius:3px;
    height:30px;
    padding:0px 20px 0px 15px;
    display: inline-block;
    line-height:30px;
    font-size:12px;
  }
  .ys-tag:before{
    content:'';
    position:absolute;
    top:-0.5px;
    right:-0.5px;
    background:linear-gradient(to left bottom,transparent 50%,#4a92ff 0,#4a92ff) 100% 0 no-repeat;
    width:16px;
    height:16px;
    transform:translateY(0px) rotate(0deg);
    transform-origin:bottom right;
    border-bottom-left-radius:inherit;
    box-shadow:-.2em .2em .3em -.1em rgba(0,0,0,.15);
  }
  .domain-box{
    width:340px;
    height:136px;
    border:1px solid #3663a6;
  }
  .domain-box-title{
    font-size:14px;
  }
  .domain-box-con{
    padding-top:10px;
  }
  .domain-select-box-tag{
    position:absolute;
    z-index:99;
    width:150px;
    overflow: hidden;
    height:30px;
    background:#00bd85;
    background:linear-gradient(-106deg,transparent 1.2em,#00bd85 0);
    left:0px;
    bottom:15px;
    line-height:30px;
    padding:0px 10px;
    overflow:hidden;
    white-space:nowrap;
    text-overflow:ellipsis;
  }
  .domain-box-tag-green{
    background:linear-gradient(-111deg,transparent 1.1em,#00bd85 0);
  }
  .domain-box-tag-blue{
    background:linear-gradient(-111deg,transparent 1.1em,#4a92ff 0);
  }
  .domain-box-tag-yellow{
    background:linear-gradient(-111deg,transparent 1.1em,#e0bb56 0);
  }
  .domain-box-tag-red{
    background:linear-gradient(-111deg,transparent 1.1em,#e96157 0);
  }
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
  .domain-select-con{
    display: inline-block;
    box-sizing: border-box;
    vertical-align: middle;
    color: #f2f2f2;
    font-size: 12px;
    line-height: normal;
    cursor:pointer;
    position:relative;
  }

  .select-input {
    height: 40px;
    position: relative;
    display: inline-block;
    box-sizing: border-box;
    outline: 0;
    -moz-user-select: none;
    user-select: none;
    cursor: pointer;
    position: relative;
    background: rgba(0,0,0,0.2);
    border-radius: 3px;
    border: 1px solid rgba(74,146,255,0.2);
  }
  .select-input:focus {
    border:1px solid #7e9fd0;
  }
  .select-input p{
    margin-right:22px;
    width:100%;
  }
  .select-arrow{
    transition: all .3s ease-in-out;
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
    right:6px;
    top:6px;
    cursor:pointer;
    line-height:28px;
    color: #4a92ff;
  }
  .select-text{
    display: block;
    height: 40px;
    line-height: 39px;
    font-size: 16px;
    overflow: hidden;
    white-space: nowrap;
    padding-left:8px;
    padding-right: 16px;
  }
  .select-body{
    width:700px;
    position: absolute;
    height:500px;
    z-index:9999;
    top:40px;
    left:0px;
    background: linear-gradient(145deg, #234981 0%, #90776a 100%);
    border-radius: 3px;
  }
  .select-body:before{
    width:100%;
    height:500px;
    background:rgba(0, 0, 0, 0.6);
    position:absolute;
    content: "";
    display: block;
    z-index: -1;
    top: 0;
    right: 0;
    bottom: 0;
    border-radius: 3px;
  }
  .select-edit-box{
    width:50%;
    position:relative;
    height:26px;
    line-height:26px;
    padding:3px 5px;
  }
  .search-btn{
    color:#f2f2f2;
  }
  .select-edit-box input{
    width:100%;
  }
  .select-edit-box i{
    position:absolute;
    top:11px;
    right:10px;
    cursor:pointer;
  }
  .domain-select-box {
    margin-top:10px;
    width: 100%;
    padding-bottom:10px;
  }
</style>
<script>
  import { changeDomain } from 'src/lib/actions'
  import { changeDomainList } from 'src/lib/actions'
  import { getDomain } from 'src/lib/getter'
  import { getDomainList } from 'src/lib/getter'
  import Api from 'src/lib/api'
  import clickoutside from 'src/directives/clickoutside';
  import ysModal from 'src/components/modal.vue'
  export default {
    directives: { clickoutside },
    vuex: {
      getters: {
        curDomain: getDomain,
        domainData:getDomainList
      },
      actions: {
        changeDomain,
        changeDomainList
      }
    },
    data () {
      return {
        empty:false,
        search: "",
        show: false,
        filterOption: [],
        inputHigh:0,
        domainList:{
          checkin:[{
            service:{
              server_name:""
            },
            waf_service:{},
          }],
          no_checkin:[{
            service:{},
            waf_service:{},
          }],

        },
        delDomainStatus:false,
      }
    },
    computed: {
      showDelStatus:function(){
        if(this.$route.topic=="waf"){
          return false;
        }else{
          return true;
        }
      }
    },
    filters: {
      statusFil:function(value){
        switch(value){
          case -4 :return '等待审核';
            break;
          case -3 :return '已经提交测试审核,还未审核,等待测试审核';
            break;
          case -2 :return '已经测试过,不能再申请';
            break;
          case -1:return '已经提交过测试域名申请,未通,不能再次申请';
            break;
          case 0 :return '未购买服务或者已经到期';
            break;
          case 1 :return '购买服务并且已经开启';
            break;
          case 2 :return '购买服务未开启';
            break;
          case 3 :return '切入未完成';
            break;
          case 4 :return '未切入';
            break;
          case 5 :return '审核不通过';
            break;
          case 6 :return '审核已经通过, 但未进行测试';
            break;
          case 7 :return '测试中';
            break;
          case 11 :return '未购买服务或已到期';
            break;
          case 12 :return '购买服务未开启';
            break;
          default : return "--";
            break;
        }
      }
    },
    ready(){
      if(this.domainData.checkin.length>0 || this.domainData.no_checkin.length>0){
      }else{
        this.getData()
      }
      slimFunc()
      function slimFunc(){
        $('.domain-select-box').slimScroll({
          height: '450',
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
      getData(){
        this.$http.get('/api/cloud/domain/list').then(function (response) {
          if(response.data.status==200){
            this.domainList=response.data.data;
            if(this.domainList.checkin.length==0&&this.domainList.no_checkin.length==0){
              this.empty=true
            }else{
              this.setDomainList();
              this.getDomainImg()
            }
          }else{
            this.$root.alertError=true;
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      goNewDomainAndGo(domain_str, go_route_name){
        this.$http.get('/api/cloud/domain/list').then(function (response) {
          if (response.data.status == 200) {
            this.domainList = response.data.data;
            if (this.domainList.checkin.length == 0 && this.domainList.no_checkin.length == 0) {
              this.empty = true
            } else {
              let list = [];
              let self = this;
              this.domainList.list = [];
              for (let x in this.domainList) {
                for (let y in this.domainList[x]) {
                  let status = this.domainList[x][y].status;
                  if (status == 1) {
                    status = "domain-box-tag-green";
                  } else if (status == 2 || status == 12) {
                    status = "domain-box-tag-blue";
                  } else if (status == -1 || status == 0 || status == 5 || status == 11) {
                    status = "domain-box-tag-red";
                  } else {
                    status = "domain-box-tag-yellow";
                  }
                  this.domainList[x][y].status_class = status;
                  if (x == 'checkin') {
                    this.domainList[x][y].checkin = true;
                  } else if (x == 'no_checkin') {
                    this.domainList[x][y].checkin = false;
                  }
                  //判断页面是否是disable状态
                  if (this.domainList[x][y].status == 1 || this.domainList[x][y].status == 2 || this.domainList[x][y].status == 12) {
                    this.domainList[x][y].enable = true;
                  } else {
                    this.domainList[x][y].enable = false;
                  }
                  //判断页面是否是disable状态
                  if (!this.domainList[x][y].service) {
                    this.domainList[x][y].service = {
                      left_days: '',
                      server_name: ''
                    }
                  }
                  list.push(this.domainList[x][y]);
                }
              }
              this.domainList.list = list;
              this.changeDomainList(this.domainList);
              this.domainList.list.forEach(function (domain) {
                if (domain.domain == domain_str) {
                  self.changeDomain(domain)
                  self.$router.go({name: go_route_name})
                }
              })
            }
          } else {
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      getDomainImg(){
        let data={domains:[]};
        for(let x in this.domainList){
          for(let y in this.domainList[x]) {
            data.domains.push(this.domainList[x][y].domain)
          }
        }
        this.$http.post('/api/cloud/domain/multi_screenshot',data).then(function (response) {
          if(response.data.status==200){
            let imgList=response.data.data;
            for(let a in imgList){
              for(let x in this.domainList){
                for(let y in this.domainList[x]) {
                  if(this.domainList[x][y].domain==a){
                    this.domainList[x][y].screenshot=imgList[a].thumbnail;
                  }
                }
              }
            }
            this.setDomainList();
          }else{
            this.$root.alertError=true;
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      setDomainList(){
        let list=[];
        this.domainList.list=[];
        for(let x in this.domainList){
          for(let y in this.domainList[x]){
            let status=this.domainList[x][y].status;
            if(status==1){
              status="domain-box-tag-green";
            }else if(status==2 || status==12){
              status="domain-box-tag-blue";
            }else if(status==-1 || status==0 || status==5 || status==11){
              status="domain-box-tag-red";
            }else{
              status="domain-box-tag-yellow";
            }
            this.domainList[x][y].status_class=status;
            if(x=='checkin'){
              this.domainList[x][y].checkin=true;
            }else if(x=='no_checkin'){
              this.domainList[x][y].checkin=false;
            }
            //判断页面是否是disable状态
            if(this.domainList[x][y].status==1 || this.domainList[x][y].status==2 || this.domainList[x][y].status==12){
              this.domainList[x][y].enable=true;
            }else{
              this.domainList[x][y].enable=false;
            }
            //判断页面是否是disable状态
            if(!this.domainList[x][y].service){
              this.domainList[x][y].service = {
                left_days: '',
                server_name: ''
              }
            }
            list.push(this.domainList[x][y]);
          }
        }
        this.domainList.list=list;
        this.changeDomainList(this.domainList);
        this.setCurDomain();
      },
      setCurDomain(){
        let self = this;
        if(this.curDomain.domain){
          this.domainList.list.forEach(function (domain) {
              if(domain.domain == self.curDomain.domain){
                self.changeDomain(domain)
              }
            })
        } else {
          if (this.domainList.checkin.length > 0) {
            this.changeDomain(this.domainList.checkin[0]);
          } else {
            this.changeDomain(this.domainList.no_checkin[0]);
          }
        }

      },
      open(){
        var self = this
        if (this.show) return
        this.search = ''
        this.show = true
        setTimeout(function () {
          self.$els.search.focus()
        }, 300)
      },
      close(){
        this.searchable = false
        this.show = false
      },
      selectDomain(domain){
        this.changeDomain(domain);
        this.close()
      },
      selJumpDomain(domain){
        this.selectDomain(domain);
        this.close();
        this.$router.go({name:'domain-add-step',params:{'domain':1}})
      },
      reDomain(){
        this.getData()
      },
      delDomain(){
        let data={domain:this.curDomain.domain}
        this.delDomainStatus=false
        this.$http.delete('/api/cloud/domain',data).then(function (response) {
          if(response.data.status==200){
            this.$root.alertSuccess=true;
            this.changeDomain({});
            this.getData()
          }else{
            this.$root.alertError=true;
          }
          this.$root.errorMsg=response.data.msg;
        },function(response){
          Api.user.requestFalse(response,this);
        })
      }
    },
    components: {
      ysModal
    }
  }
</script>
