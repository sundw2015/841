<template>
  <div class="pos-r scatter" v-bind:style="{width: width+'px', height:height+'px',}">
    <div v-show="status==0"
         class="textC"
         v-bind:style="{width: width, height:height,lineHeight:height}">
      <loading-normal :show="true"></loading-normal>
    </div>
    <div v-show="status==1"
         class="textC ys-info-color"
         v-bind:style="{width: width, height:height,lineHeight:height}">
      <div class="d-i-b verticalM">
        <p style="line-height:1"><i class="ys-icon icon-chart-no-data" style="margin-left:6px;color:rgba(154,188,238,0.25);font-size: 60px;"></i></p>
        <p style="line-height:1;color:rgba(154,188,238,0.7);" class="m-t-20">暂时没有数据</p>
      </div>
      <span style="display:none;">{{status}}</span>
    </div>
    <div v-show="status==2">
      <div v-bind:style="{width: width+'px',height:height+'px',}">
        <div :id="'scatter-chart-'+id"
             v-bind:style="{width: width+'px',height:height+'px',}"
             v-on:resize="handleResize($event)">
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
<script>
  let echarts =  require('echarts/lib/echarts');
  export default {
    name: 'scatter-chart',
    props: {
      name:{
        default: ""
      },
      width:{
        default: "100%"
      },
      height:{
        default: "240"
      },
      color:{
        type:Array,
        default () {
          return ['#f1eb37','#f2607f','#3ab4cb','#f87461','#e7e4f1']
        }
      },
      datas:{
        type:Object,
        dafault: function(){
          return {
            x:{},
            y:{}
          }
        }
      },
      series:{
        default:function(){
            return []
        },
      },
      unit:{
        default: "number"
      },
      radius:{
        default:1
      }
    },
    data(){
      return {
          id:'',
          stateMax:0,
          status:2,
          legend: ['Punch Card1','Punch Card2'],
          dayschart:{
            hours:['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a','10a','11a',
                  '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p'],
                  days: [],
            list: {
              data0:[],
              data1:[],
              data2:[],
              data3:[],
              data4:[],
              data5:[],
              data6:[],
            }
          }
      }
    },
    ready () {
      this.initChart()
    },
    methods:{
      MaxSum (sumMaz) {
        let radius;
        if(sumMaz>this.stateMax/2){
          radius = 40
        }else if(sumMaz>this.stateMax/4){
          radius = 32
        }else if(sumMaz>this.stateMax/8){
          radius = 24
        }else if(sumMaz>this.stateMax/16){
          radius = 16
        }else if(sumMaz>this.stateMax/32){
          radius = 8
        }

        return radius;
      },
      initChart(){
        var str = "";
        for(var i =0;i<6;i++){
          var num = Math.random()*9;
          num = parseInt(num,10);
          str+=num;
        }
        this.id=this.type+"-scatter-chart-"+str;
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('scatter-chart-'+self.id)){
            self.setChart();
            window.addEventListener('resize', self.handleResize)
            var EleResize = {
              _handleResize: function (e) {
                var ele = e.target || e.srcElement;
                var trigger = ele.__resizeTrigger__;
                if (trigger) {
                  var handlers = trigger.__z_resizeListeners;
                  if (handlers) {
                    var size = handlers.length;
                    for (var i = 0; i < size; i++) {
                      var h = handlers[i];
                      var handler = h.handler;
                      var context = h.context;
                      handler.apply(context, [e]);
                    }
                  }
                }
              },
              _removeHandler: function (ele, handler, context) {
                var handlers = ele.__z_resizeListeners;
                if (handlers) {
                  var size = handlers.length;
                  for (var i = 0; i < size; i++) {
                    var h = handlers[i];
                    if (h.handler === handler && h.context === context) {
                      handlers.splice(i, 1);
                      return;
                    }
                  }
                }
              },
              _createResizeTrigger: function (ele) {
                var obj = document.createElement('object');
                obj.setAttribute('style',
                    'display: block; position: absolute; top: 0; left: 0; height: 100%; width: 100%; overflow: hidden;opacity: 0; pointer-events: none; z-index: -1;');
                obj.onload = EleResize._handleObjectLoad;
                obj.type = 'text/html';
                ele.appendChild(obj);
                obj.data = 'about:blank';
                return obj;
              },
              _handleObjectLoad: function (evt) {
                this.contentDocument.defaultView.__resizeTrigger__ = this.__resizeElement__;
                this.contentDocument.defaultView.addEventListener('resize', EleResize._handleResize);
              }
            };
            if (document.attachEvent) {//ie9-10
              EleResize.on = function (ele, handler, context) {
                var handlers = ele.__z_resizeListeners;
                if (!handlers) {
                  handlers = [];
                  ele.__z_resizeListeners = handlers;
                  ele.__resizeTrigger__ = ele;
                  ele.attachEvent('onresize', EleResize._handleResize);
                }
                handlers.push({
                  handler: handler,
                  context: context
                });
              };
              EleResize.off = function (ele, handler, context) {
                var handlers = ele.__z_resizeListeners;
                if (handlers) {
                  EleResize._removeHandler(ele, handler, context);
                  if (handlers.length === 0) {
                    ele.detachEvent('onresize', EleResize._handleResize);
                    delete  ele.__z_resizeListeners;
                  }
                }
              }
            } else {
              EleResize.on = function (ele, handler, context) {
                var handlers = ele.__z_resizeListeners;
                if (!handlers) {
                  handlers = [];
                  ele.__z_resizeListeners = handlers;

                  if (getComputedStyle(ele, null).position === 'static') {
                    ele.style.position = 'relative';
                  }
                  var obj = EleResize._createResizeTrigger(ele);
                  ele.__resizeTrigger__ = obj;
                  obj.__resizeElement__ = ele;
                }
                handlers.push({
                  handler: handler,
                  context: context
                });
              };
              EleResize.off = function (ele, handler, context) {
                var handlers = ele.__z_resizeListeners;
                if (handlers) {
                  EleResize._removeHandler(ele, handler, context);
                  if (handlers.length === 0) {
                    var trigger = ele.__resizeTrigger__;
                    if (trigger) {
                      trigger.contentDocument.defaultView.removeEventListener('resize', EleResize._handleResize);
                      ele.removeChild(trigger);
                      delete ele.__resizeTrigger__;
                    }
                    delete  ele.__z_resizeListeners;
                  }
                }
              }
            }
            var resizeDiv = document.getElementById('scatter-chart-'+self.id);
            EleResize.on(resizeDiv, function(){self.handleResize()});
            clearInterval(repeat)
          }
        },300)
      },
      setChart(){
        let self=this
        self.chart = echarts.init(document.getElementById('scatter-chart-'+this.id));
        if(!this.datas){return false}
        let Xdata = this.datas.x;
        let Ydata = this.datas.y;
        var hours = [], days = [], radius = this.radius;

        for(let key in Xdata){
          hours = Xdata[key] || [];
        }
        let arr2 = [],arr2Max = [];
        for(let key in Ydata){
          days.push(key)
          arr2.push(Ydata[key])
        }
        for(let i=0;i<arr2.length;i++){
          let max = Math.max.apply(null,arr2[i]);
          arr2Max.push(max)
        }
        this.stateMax = Math.max.apply(null,arr2Max);

        let hoursLen = hours.length,daysLen = days.length;

        var arr = [];
        for(let j=0;j<daysLen;j++){
          let temp = [];
          for( let i = 0;i<hoursLen;i++){
            temp.push([j,i,arr2[j][i]])
          }
          arr.push(temp)
        }
        for(let i = 0;i<arr.length;i++){
          self.dayschart.list['data'+i] = arr[i].map(function (item) {
              return [item[1], item[0], item[2]];
          });
        }
        self.legend = days;
        this.option = {
            legend: {
                data: self.legend,
                textStyle:{
                  color:"#93a6d8"
                },
                left: 'right',
            },
            tooltip: {
                position: 'top',
                formatter: function (params) {
                    //return params.value[2] + ' commits in ' + hours[params.value[0]] + ' of ' + days[params.value[1]];
                    if(self.unit == 'band'){
                        return days[params.value[1]]+" "+ hours[params.value[0]] + " :"+self.changeGbUnit(params.value[2]);
                    }else{
                        return days[params.value[1]]+" "+ hours[params.value[0]] + " :"+self.changeUnit(params.value[2]) + ' 次';
                    }
                }
            },
            grid: {
              top:40,
              bottom:10,
              left:20,
              right:20,
              containLabel: true
            },
            xAxis: {
                type: 'category',
                data: hours,
                boundaryGap: false,
                axisTick:{
                  show:false
                },
                splitLine: {
                  show: true,
                  lineStyle: {
                    color: 'rgba(70,87,142,0.5)',
                  }
                },
                axisLine: {
                  show: false
                },
                axisLabel:{textStyle:{color:"#93a6d8"}}
            },
            yAxis: {
              type: 'category',
              position:"left",
              offset:10,
              data: days,
              axisLine: {
                show: false
              },
              axisTick:{
                show:false
              },
              axisLabel:{textStyle:{color:"#93a6d8"}}
            },
            series: [
              {
                name: days[0],
                type: 'scatter',
                symbolSize: function (val) {
                  return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#965361"
                  }
                },
                data: self.dayschart.list.data0,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[1],
                type: 'scatter',
                symbolSize: function (val) {
                    return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#6c5143"
                  }
                },
                data: self.dayschart.list.data1,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[2],
                type: 'scatter',
                symbolSize: function (val) {
                   return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#8a5b8b"
                  }
                },
                data: self.dayschart.list.data2,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[3],
                type: 'scatter',
                symbolSize: function (val) {
                    return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#6d61a2"
                  }
                },
                data: self.dayschart.list.data3,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[4],
                type: 'scatter',
                symbolSize: function (val) {
                    return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#ad664e"
                  }
                },
                data: self.dayschart.list.data4,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[5],
                type: 'scatter',
                symbolSize: function (val) {
                    return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#a48d5a"
                  }
                },
                data: self.dayschart.list.data5,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
              {
                name: days[6],
                type: 'scatter',
                symbolSize: function (val) {
                    return self.MaxSum(val[2])
                },
                itemStyle:{
                  normal:{
                    color:"#ad5455"
                  }
                },
                data: self.dayschart.list.data6,
                animationDelay: function (idx) {
                    return idx * 5;
                }
              },
            ]

        };
        self.chart.setOption(self.option);
      },
      changeUnit(val){
        if(val<10000){
          return val
        }else if(val<100000000 && val>=10000){
          val = (val/10000).toFixed(1);
          return val+'万'
        }else if(val<1000000000000 && val>=100000000){
          val = (val/100000000).toFixed(1);
          return val+'亿'
        }else if(val>=1000000000000){
          val = (val/1000000000000).toFixed(1);
          return val+'万亿'
        }
      },
        changeGbUnit(val) {
                if (val < 1024) {
                    return val + "b"
                } else if (val >= 1024 && val < 1024 * 1024) {
                    val = (val / 1024).toFixed(1);
                    return val + "Kb"
                } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024)).toFixed(1);
                    return val + "Mb"
                } else if (val >= 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024 * 1024)).toFixed(1);
                    return val + "Gb"
                }
            },
      handleResize(){
        this.chart.resize();
      },
      changeStatus(){
        // 0 加载之前   1 加载后无数据   2 加载后有数据
        if(this.datas.x===""){
          this.status = 0;
        }else{
          for(let key in this.datas.x){
            if(this.datas.x[key].length>0){
              this.status = 2;
              this.$nextTick(()=>{
                  this.initChart();
              })
            }else{
              this.status = 1;
            }
          }

        }
      },
    },
    watch: {
      'datas': function(){
          this.changeStatus();
      },
    }
  }
</script>
