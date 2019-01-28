<template>
  <div>
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
      <div v-bind:style="{width: width,height:height}">
        <div :id="'ling-bar-chart-'+id"
             v-bind:style="{width: width,height:height}"
             v-on:resize="handleResize($event)">
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
</style>
<script>
  let echarts =  require('echarts/lib/echarts');
  var collect = require('collect.js')
  export default {
    name:"ling-bar-chart",
    props: {
      id: {
        default: 0
      },
      name:{
        default: ""
      },
      tipname:{
        default: "使用数"
      },
      width:{
        default: "100%"
      },
      height:{
        default: "200px"
      },
      color:{
        default:"#e96157"
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
      unit: {
        default: ''
      },
      time:{
        default: function () {
          return []
        }
      }
    },
    data() {
      return {
        dataShadow:[],
        dataAdd:[],
        x:{ },
        y:{ },
      }
    },
    computed: {
      status:function(){
        // 0 加载之前   1 加载后无数据   2 加载后有数据
        this.x = this.datas.y.reverse();
        this.y = this.datas.x.reverse();
        if(this.x===""){
          return 0
        }else{
          if(this.x.length>0){
            this.initChart();
            return 2
          }else{
            return 1
          }
        }
      }
    },
    methods:{
      initChart(){
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('ling-bar-chart-'+self.id)){
            if(self.y.length<5){
              for(var i=0;i<5-self.y.length;i++){
                //self.y.unshift("")
                //self.x.unshift(0)
              }
            }
            self.dataShadow=[];
            self.dataAdd=[];
            self.xData=[];
            self.yData=[];
            let num=0;
            for (var i = 0; i < self.y.length; i++) {
              self.dataShadow.push(collect(self.x).max());
              let width=$('#ling-bar-chart-'+self.id).width();
              self.dataAdd.push(collect(self.x).max()/width)
              self.xData.push(self.x[i])
              self.yData.push(self.y[i])
              if(self.x[i]==0){num++}
            }
            if(num>=5){
              self.dataShadow=[];
              self.dataAdd=[];
              for (var i = 0; i < self.y.length; i++) {
                self.dataShadow.push(1);
                self.dataAdd.push(0)
              }
            }//如果返回数据都是0的情况
            self.setChart();
            window.addEventListener('resize', self.handleResize)
            clearInterval(repeat)
          }
        },300)
        let resizeRepeat=setInterval(function(){
          if(document.getElementById('ling-bar-chart-'+self.id)){
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
            var resizeDiv = document.getElementById('ling-bar-chart-'+self.id);
            EleResize.on(resizeDiv, function(){self.handleResize()});
            clearInterval(resizeRepeat)
          }
        },300)
      },
      setChart(){
        let self=this;
        self.chart = echarts.init(document.getElementById('ling-bar-chart-'+this.id));
        self.option = {
          tooltip : {
            trigger: 'axis',
            axisPointer : {
              type : 'shadow'
            },
            formatter: function (params) {
              let str=params[0].name
              return str
            },
          },
          grid: {
            show:false,
            top: 0,
            left:0,
            right:"0%",
            bottom:0
          },
          yAxis : [
            {
              type : 'category',
              data : self.y,
              axisLine:{
                show:false,
              },
              axisTick: {
                show:false,
              },
              axisLabel:{
                show:false,
              }
            }
          ],
          xAxis : [
            {
              type : 'value',
              axisLine:{
                show:false,
              },
              axisTick: {
                show:false,
              },
              splitNumber:10,
              axisLabel:{
                show:false,
              },//y轴坐标的字颜色
              splitLine:{
                show:false,
              },
              max:"dataMax"
            }
          ],
          series : [
            {
              type: 'bar',
              itemStyle: {
                normal: {color: "rgba(0,0,0,0.15)"}
              },
              barGap:'-100%',
              barWidth: '24',
              barCategoryGap:'30%',
              data:self.dataShadow,
              animation: false,
              label:{
                normal:{
                  show:true,
                  position: "insideRight",
                  color:"#fff",
                  formatter: function (params) {
                    let value=self.x[params.dataIndex]
                    let str='';
                    if(self.unit=='band'){
                       str=self.changeUnit(value)
                    }else{
                      str=value+self.unit
                    }
                    return str
                  },
                }
              },
            },
            {
              name:self.tipname,
              type:'bar',
              stack: '总量',
              itemStyle: {
                normal: {
                  color: self.hexToRgba(self.color,18).rgba
                }
              },
              label:{
                normal:{
                  show:true,
                  position: [10, 7],
                  color:self.color,
                  formatter: function (params) {
                    let value=self.y[params.dataIndex]
                    return value
                  },
                }
              },
              barWidth: '24',
              data:self.x,
              markPoint:{
                data:[{}]
              }
            },
            {
              name: '搜索引擎',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: false,
                  position: 'insideRight'
                }
              },
              itemStyle: {
                normal: {
                  color: self.color
                }
              },
              barWidth: 1,
              data: self.dataAdd,
              barMaxWidth:1
            }
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
      handleResize(){
        this.chart.resize();
      },
      hexToRgba(hex, al){
        var hexColor = /^#/.test(hex) ? hex.slice(1) : hex, alp = hex === 'transparent' ? 0 : Math.ceil(al), r, g, b; hexColor = /^[0-9a-f]{3}|[0-9a-f]{6}$/i.test(hexColor) ? hexColor : 'fffff'; if (hexColor.length === 3) { hexColor = hexColor.replace(/(\w)(\w)(\w)/gi, '$1$1$2$2$3$3'); } r = hexColor.slice(0, 2); g = hexColor.slice(2, 4); b = hexColor.slice(4, 6); r = parseInt(r, 16); g = parseInt(g, 16); b = parseInt(b, 16); return { hex: '#' + hexColor, alpha: alp, rgba: 'rgba(' + r + ', ' + g + ', ' + b + ', ' + (alp / 100).toFixed(2) + ')' };
      },
    },
  }
</script>
