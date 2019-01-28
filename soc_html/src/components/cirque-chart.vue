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
      <div v-bind:style="{width: width, height:height}" class="pie-box">
	    <div :id="'amountOfEvents-item-circle'+id" style="width: 100%;height: 90px;"></div>
	    <div class="amountOfEvents-item-text m-t-15" v-on:resize="handleResize($event)">{{name}}</div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .pie-box{
    position:relative;
  }
  .pie-cover{
    position:absolute;
    width:85px;
    height:85px;
    top:40%;
    left:50%;
    margin-top:-42.5px;
    margin-left:-42.5px;
    background: rgba(0,0,0,0.2);
    border-radius: 50%;
    z-index:1;
  }
</style>
<script>
  let echarts =  require('echarts/lib/echarts');
  export default {
    name:"cirqueChart",
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
      rose:{
        default: false
      },
      unit:{
        default: false
      },
	    value: {
          default: 0
	    }
    },
    computed: {
      status:function(){
          this.initChart();
            return 2;
      }
    },
    data() {
      return {
        chart: "",
        option:{},
        colorData:[
          ['#00bd85','#e96157','#dabb61','#0c67ff','#4a92ff','#8375d0','#5dc962','#008974','#b06cae','#8375d0'],//配色方案1
          ['#e96157','#dabb61','#e77d4e','#8375d0','#b06cae','#815f44','#943737','#be4444'],//配色方案2
          ['#e96157','#4a92ff','#00bd85']//配色方案3
        ],
        pieColor:[]
      }
    },
    ready(){
      this.pieColor=this.colorData[this.color-1]
    },
    methods:{
      initChart(){
        let self=this;
        let repeat=setInterval(function(){
          if(document.getElementById('amountOfEvents-item-circle'+ self.id)){
            self.setChart();
            window.addEventListener('resize', self.handleResize)
            clearInterval(repeat)
          }
        },300)
        let resizeRepeat=setInterval(function(){
          if(document.getElementById('amountOfEvents-item-circle'+ self.id)){
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
            var resizeDiv = document.getElementById('amountOfEvents-item-circle'+ self.id);
            EleResize.on(resizeDiv, function(){
              self.handleResize();
            });
            clearInterval(resizeRepeat)
          }
        },300)
      },
      changeWanUnit(val){
        if(val<10000){
          return val+"条"
        }else{
          val = (val / 10000).toFixed(2);
          return val+"万条"
        }
      },
      setChart(){
        let self=this;
        self.chart = echarts.init(document.getElementById('amountOfEvents-item-circle'+ self.id));
      let dataStyle = {
        normal: {
            label: {
                show: false
            },
            labelLine: {
                show: false
            },
            shadowBlur: 40,
            borderWidth: 10,
            shadowColor: 'rgba(0, 0, 0, 0)' //边框阴影
        }
    };
    let placeHolderStyle = {
        normal: {
            color: 'rgba(57,61,80,0.5)',
            label: {
                show: false
            },
            labelLine: {
                show: false
            }
        },
        emphasis: {
            color: 'rgba(57,61,80,0.5)'
        }
    };
    let option = {
        title: {
            text: self.value+'%',
            x: 'center',
            y: 'center',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 20,
                color: "#fff",
              fontFamily: 'digi'
            }
        },
      center: ['50%', '50%'],
//        tooltip: {
//            trigger: 'item',
//            show: true,
//            formatter: "{b} : <br/>{d}%",
//            backgroundColor: 'rgba(0,0,0,0.7)', // 背景
//            padding: [8, 10], //内边距
//            extraCssText: 'box-shadow: 0 0 3px rgba(255, 255, 255, 0.4);', //添加阴影
//        },
        series: [{
                name: 'Line 1',
                type: 'pie',
                clockWise: false,
                radius: [30, 40],
                center:['50%','50%'],
                itemStyle: dataStyle,
                hoverAnimation: false,
                startAngle: 90,
                label:{
                    borderRadius:'10',
                },
                data: [{
                  value: self.value,
                  name: '四级匹配度',
                  itemStyle: {
                    normal: {
                      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color:'#E96157'
                      }, {
                        offset: 0.5,
                        color: '#dabb61'
                      },{
                        offset: 1,
                        color: '#00BD85'
                      }])
                    }
                  }
                }, {
                  value: 100 - parseInt(self.value),
                  name: '',
                  tooltip: {
                    show: false
                  },
                  itemStyle: placeHolderStyle
                }]
            }
        ]
    };
        self.chart.setOption(option);

      },
      handleResize(){
        this.chart.resize();
      }
    },
  }
</script>