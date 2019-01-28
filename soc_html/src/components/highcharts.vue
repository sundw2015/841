<template>
  <div :id="container" style="height: 300px;background:none"></div>
</template>

<script>
var Highcharts = require('highcharts')
var Highstock = require('highcharts/highstock')
require('highcharts/modules/exporting')(Highcharts)

Highcharts.setOptions({
  global: {
    useUTC: false
  }
});

export default {
  props: ['title', 'container','color','yaxe'],
  data: function() {
    let self=this;
    return {
      chart: null,
      opts: {
        chart: {
          renderTo: this.container,
          type: 'areaspline',
          backgroundColor:"",
          style:{"fontFamily":"微软雅黑"}
        },
        title: {
          text: this.title,
          style:{
            color:"#fff"
          }
        },
        exporting:{
          enabled:false //用来设置是否显示‘打印’,'导出'等功能按钮，不设置时默认为显示
        },
        credits:{
          enabled:false
        },
        legend: {//曲线标题
          enabled: false,
          layout: 'vertical',
          align: 'left',
          verticalAlign: 'top',
          x: 0,
          y: 0,
          floating: true
        },
        xAxis: {
          type: 'datetime',
          tickPixelInterval: 50,
          title: {
            text: "小时/分/秒",
            style:{
              color:"#9abcee"
            }
          },
          lineColor:"rgba(70,87,142,0.5)",
          tickColor:"rgba(70,87,142,0.5)",
          labels:{
            style: {color:'#9abcee'},

          },
        },
        yAxis: {
          title: {
            text: this.yaxe,
            style:{
              color:"#9abcee"
            },
          },
          lineColor:"rgba(70,87,142,0.5)",
          gridLineColor:"rgba(70,87,142,0.5)",
          labels:{
            style: {color:'#9abcee'}
          },
        },
        plotOptions:{
          shadow:false
        },
        exporting:{
          enabled:false
        },
        tooltip: {
          backgroundColor:"rgba(0,0,0,0.25)",
          borderWidth:0,
          style: {
            padding: 10,
            color:"#9abcee"
          },
          formatter: function () {
            return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + self.countUnit(this.y);
          }
        },
        series: [{
          name: "",
          data: [],
          lineWidth:1,
          lineColor:this.color.lineColor,
          fillColor:{
            linearGradient:{
              x1:0,
              y1:0,
              x2:0,
              y2:1
            },
            stops:[[0,this.color.stopsA],[1,this.color.stopsB]]
          },
          marker:{
            enabled:true, //是否显示点
            radius:2,
            states:{
              hover:{
                enabled:true,
                radius:4
              }
            },
            fillColor:this.color.lineColor
          },
        }]
  		}
    }
  },
  methods: {
    initChart: function(minTime) {
      var initData = []
      var x, y = null
      for (var i = 10; i >=1; i--) {
        x = minTime - i * 1000;
        initData.push([x, y])
      }
      this.chart.series[0].setData(initData)
    },
    addPoint: function(point) {
      this.chart.series[0].addPoint(point, true, true)
    },
    countUnit:function(val){
        if(this.yaxe=="流量"){
            if(val<1024){
                return  this.yaxe+":"+ val + "b"
            }else if(val>=1024 && val<1024*1024){
                val=(val/1024).toFixed(1);
                return  this.yaxe+":"+ val + "Kb"
            }else if(val>=1024*1024 && val<1024*1024*1024){
                val=(val/(1024*1024)).toFixed(1);
                return  this.yaxe+":"+ val + "Mb"
            }else if(val>=1024*1024*1024){
                val=(val/(1024*1024*1024)).toFixed(1);
                return  this.yaxe+":"+ val + "Gb"
            }
        }else if (this.yaxe=="时间"){
          return  this.yaxe+":"+ val + "ms"
        }else{
            return  this.yaxe+":"+ val + "个"
        }
    }
  },
  ready: function() {
      this.chart = new Highcharts.Chart(this.opts);
  }
}
</script>
