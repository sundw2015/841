<template>
  <div class="pos-r loop" v-bind:style="{width: width+'px', height:height+'px',}">
    <div v-show="status==0"
         class="textC"
         v-bind:style="{width: width+'px', height:height+'px',lineHeight:height+'px'}">
      <loading-normal :show="true"></loading-normal>
    </div>
    <div v-show="status==1"
         class="textC ys-info-color"
          v-bind:style="{width: width+'px', height:height+'px',lineHeight:height+'px'}">
      <div class="d-i-b verticalM">
        <p style="line-height:1"><i class="ys-icon icon-chart-no-data" style="margin-left:6px;color:rgba(154,188,238,0.25);font-size: 60px;"></i></p>
        <p style="line-height:1;color:rgba(154,188,238,0.7);" class="m-t-20">暂时没有数据</p>
      </div>
      <span style="display:none;">{{status}}</span>
    </div>
    <div v-show="status==2">
      <div v-bind:style="{width: width+'px',height:height+'px',}">
        <div :id="'loop-chart-'+id"
             v-bind:style="{width: width+'px',height:height+'px',}"
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
    name:"loop-chart",
    props: {
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
        default: "200"
      },
      color:{
        default:"#e96157"
      },
      listColor:{
        type: Array,
        default: function () {
         return ['#4993fd', '#3a9be5', '#27a6c6', '#12b2a3', '#03bb89']
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
        id:'',
        status:0,
        dataShadow:[],
        dataAdd:[],
        x:{ },
        y:{ },
      }
    },
    ready () {
      this.changeStatus()
    },
    methods:{
      initChart(){
        var str = "";
        for(var i =0;i<6;i++){
          var num = Math.random()*9;
          num = parseInt(num,10);
          str+=num;
        }
        this.id=this.type+"-loop-chart-"+str;
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('loop-chart-'+self.id)){
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
            var resizeDiv = document.getElementById('loop-chart-'+self.id);
            EleResize.on(resizeDiv, function(){self.handleResize()});
            clearInterval(repeat)
          }
        },300)
      },
      setChart(){
        let self=this;
        self.chart = echarts.init(document.getElementById('loop-chart-'+this.id));
        if(!this.datas){return false}
        let Xdata = [];
        let Ydata = [];

        //console.log(this.datas.x,this.datas.y)
        for(let key in this.datas.y){
          Xdata.push(key)
          let num = 0;
          for(let i=0;i<this.datas.y[key].length;i++){
            num += this.datas.y[key][i]
          }
          Ydata.push({name:key,value:num})
        }
        
        self.option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            color:['#4a8aed','#d95e56','#07b07f','#cbaf5f','#1263ed','#d7774e','#e96157','#4a92ff','#00bd85'],
            legend: {
                //orient: 'vertical',
                x: 'center',
                bottom:10,
                //right:20,
                data: Xdata,
                textStyle:{
                  color:"#93a6d8" 
                },
            },
            series: [
                {
                    name: self.name,
                    type:'pie',
                    radius: ['50%', '70%'],
                    center: ['50%', '40%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '14',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    itemStyle:{
                        normal:{
                            // color:function(params) {
                            //     return self.listColor[params.dataIndex];
                            // }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:Ydata
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
      changeStatus(){
        // 0 加载之前   1 加载后无数据   2 加载后有数据
        if(this.datas==undefined){
          this.status = 1;
        }else{
          if(this.datas.x===""){
            this.status = 0;
          }else{
            for(let key in this.datas.x){
              if(this.datas.x[key].length>0){
                this.initChart();
                this.status = 2;
              }else{
                this.status = 1;
              }
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
