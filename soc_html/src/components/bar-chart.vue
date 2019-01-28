<template>
  <div class="pos-r" v-bind:style="{width: width, height:height}">
    <div v-show="status==0"
         class="textC"
         v-bind:style="{width: width, height:height,lineHeight:height}">
      <loading-normal :show.sync="true"></loading-normal>
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
        <div id="feng-bar-chart-{{ id }}"
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
  export default {
    name:"feng-bar-chart",
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
        default: ""
      },
      x:{
        default: ""
      },
      y:{
        default: ""
      },
      unit: {
        default: ''
      }
    },
    data() {
      return {
        barColor:['#4993fd','#3a9be5','#27a6c6','#12b2a3','#03bb89'],
      }
    },
    computed: {
      status:function(){
        // 0 加载之前   1 加载后无数据   2 加载后有数据
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
      },
    },
    methods:{
      initChart(){
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('feng-bar-chart-'+self.id)){
            self.setChart();
            window.addEventListener('resize', self.handleResize)
            clearInterval(repeat)
          }
        },300)
        let resizeRepeat=setInterval(function(){
          if(document.getElementById('feng-bar-chart-'+self.id)){
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
            var resizeDiv = document.getElementById('feng-bar-chart-'+self.id);
            EleResize.on(resizeDiv, function(){
              self.handleResize();
            });
            clearInterval(resizeRepeat)
          }
        },300)
      },
      setChart(){
        let self=this;
        self.chart = echarts.init(document.getElementById('feng-bar-chart-'+this.id));
        self.option = {
          tooltip : {
            trigger: 'axis',
            axisPointer : {
              type : 'shadow'
            },
            formatter: function (params) {
              let str=params[0].name
              for(var i=0;i<params.length;i++){
                if(self.unit=="band"){
                  str += "<br/>"+params[i].seriesName+":"+self.changeUnit(params[i].value)
                }
                else if(self.unit=='kw'){
                  str += "<br/>"+params[i].seriesName+":"+self.KWUnit(params[i].value)
                }else if(self.unit=="wan"){
                  str += "<br/>"+self.tipname+":"+self.changeWanUnit(params[i].value)
                }else{
                  if(self.tipname==""){
                    str += "<br/>"+params[i].seriesName+":"+params[i].value
                  }else{
                    str += "<br/>"+self.tipname+":"+params[i].value
                  }
                }
              }
              return str
            },
          },
          grid: {
            top: '10',
            bottom:'20',
            left:10,
            right:10,
            containLabel: true
          },
          xAxis : [
            {
              type : 'category',
              data : self.x,
              axisLine:{
                show:true,
                lineStyle:{
                  color:"#46578e",
                  opacity:"0.75"
                }
              },
              axisTick: {
                show:false,
              },
              axisLabel:{textStyle:{color:"#dfdfe7"}},//x轴坐标的字颜色
            }
          ],
          yAxis : [
            {
              type : 'value',
              axisLine:{
                show:true,
                lineStyle:{
                  color:"#46578e",
                  opacity:"0.75"
                }
              },
              axisTick: {
                show:false,
              },
              splitNumber:5,
              axisLabel:{
              textStyle:{color:"#dfdfe7"},
                formatter: function(value){
                  if(self.unit=="band"){
                    return self.changeUnit(value)
                  }else if(self.unit=='kw'){
                    return self.KWUnit(value)
                  }else if(self.unit=="wan"){
                    if(value<10000){
                      return value
                    }else{
                      return (value / 10000).toFixed(2)+"万"
                    }
                  }else{
                    return value
                  }
                },
              },//y轴坐标的字颜色
              splitLine:{
                lineStyle:{
                  color:"#46578e",
                  opacity:"0.75"
                }
              }
            }
          ],
          series : [
            {
              name:self.tipname,
              type:'bar',
              itemStyle: {
                normal: {
                  color: function(params) {
                    return self.barColor[params.dataIndex];
                  },
                  opacity:1
                }
              },
              barWidth: '25',
              data:self.y
            }
          ]
        };
        self.chart.setOption(self.option);
      },
      changeWanUnit(val){
        if(val<10000){
          return val+"条"
        }else{
          val = (val / 10000).toFixed(2);
          return val+"万条"
        }
      },
      changeUnit(val){
        if(val<1024){
          return  val + "b"
        }else if(val>=1024 && val<1024*1024){
          val=(val/1024).toFixed(1);
          return  val + "Kb"
        }else if(val>=1024*1024 && val<1024*1024*1024){
          val=(val/(1024*1024)).toFixed(1);
          return  val + "Mb"
        }else if(val>=1024*1024*1024){
          val=(val/(1024*1024*1024)).toFixed(1);
          return  val + "Gb"
        }
      },
      handleResize(){
        this.chart.resize();
      },
    },
  }
</script>