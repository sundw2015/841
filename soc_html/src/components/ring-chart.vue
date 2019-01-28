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
      <div v-bind:style="{width: width, height:height}">
        <div id="ring-chart-{{ id }}"
             v-bind:style="{width: width, height:height}"
             v-on:resize="handleResize($event)">
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  let echarts =  require('echarts/lib/echarts');
  export default {
    name:"ringChart",
    props: {
      id: {
        default: 0
      },
      name:{
        default: ""
      },
      color:{
        default: 1
      },
      width:{
        default: "100%"
      },
      height:{
        default: "200px"
      },
      y:{
        default: ""
      },
      turn:false
    },
    computed: {
      status:function(){
        // 0 加载之前   1 加载后无数据   2 加载后有数据
        if(this.y===""){
          return 0
        }else{
          if(this.y>=0){
            this.initChart();
            return 2
          }else{
            return 1
          }
        }
      }
    },
    data() {
      return {
        chart: "",
        option:{},
        colorData:[
          ['#00bd85','#379de0'],//配色方案1 小于50
          ['#e1905c','#e96257'] //配色方案2 大于50
        ],
        fontColor:"",
        pieColor:[]
      }
    },
    ready(){

    },
    methods:{
      initChart(){
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('ring-chart-'+self.id)){
            self.setChart();
            window.addEventListener('resize', self.handleResize)
            clearInterval(repeat)
          }
        },300)
        let resizeRepeat=setInterval(function(){
          if(document.getElementById('ring-chart-'+self.id)){
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
            var resizeDiv = document.getElementById('ring-chart-'+self.id);
            EleResize.on(resizeDiv, function(){
              self.handleResize();
            });
            clearInterval(resizeRepeat)
          }
        },300)
      },
      setChart(){
        let self=this;
        if(self.turn){
          if(self.y>50){
            this.pieColor=this.colorData[0]
            this.fontColor="#00bd85"
          }else{
            this.pieColor=this.colorData[1]
            this.fontColor="#e96257"
          }
        }else{
          if(self.y>50){
            this.pieColor=this.colorData[1]
            this.fontColor="#e96257"
          }else{
            this.pieColor=this.colorData[0]
            this.fontColor="#00bd85"
          }
        }

        self.chart = echarts.init(document.getElementById('ring-chart-'+this.id));
        self.option = {
          color:[{
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0, color: this.pieColor[0] // 0% 处的颜色
            }, {
              offset: 1, color: this.pieColor[1] // 100% 处的颜色
            }],
          },"#000000"],
          series: [
            {
              name:'ring',
              type:'pie',
              radius: ['54%', '60%'],
              avoidLabelOverlap: false,
              hoverAnimation:false,
              label: {
                normal: {
                  show: true,
                  position: 'center',
                  formatter: function(){
                    return self.y
                  },
                  color:self.fontColor,
                  textStyle: {
                    fontSize: '20',
                    fontWeight: ''
                  }
                },
                emphasis: {
                  show: false,
                  textStyle: {
                    fontSize: '24',
                    fontWeight: 'bold'
                  }
                }
              },
              data: [
                {
                  value: self.y,
                  name:"use"
                },
                {
                  value: 100-self.y,
                  name:"no",
                  itemStyle:{
                    normal:{
                      opacity:0.15
                    }
                  }
                }
              ]
            }
          ]
        };
        self.chart.setOption(self.option);
      },
      handleResize(){
        this.chart.resize();
      }
    },
  }
</script>