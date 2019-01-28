<template>
  <div id="container-{{id}}" style="height: 300px;background:none"></div>
</template>

<script>
var Highcharts = require('highcharts')
require('highcharts/modules/exporting')(Highcharts)

Highcharts.setOptions({
  global: {
    useUTC: false
  }
});

export default {
//  props: ['title', 'container','color','yaxe'],
  props: {
    id: {
      default: 0
    },
    name:{
      default: ''
    },
    yaxe:{
      default: ''
    },
    series: {
      default: function () {
        return [
          { name: "ACK", color: "", data: [] }
        ]
      }
    },
    color: {
      default: function () {
        return []
      }
    },
    width:{
      default: "100%"
    },
    height:{
      default: "200px"
    },
    y:{
      default: function () {
        return []
      }
    },
  },
  data: function() {
    let self=this;
    var a = function (name, color,data) {
      return {
        name: name,
        data: data,
        lineWidth: 1,
        lineColor: color.lineColor,
        fillColor:{
          linearGradient:{
            x1:0,
            y1:0,
            x2:0,
            y2:1
          },
          stops:[[0,color.stopsA],[1,color.stopsB]]
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
          fillColor:color.lineColor
        },
      }
    }
    var temp = []
    this.series.forEach(function (item,index) {
      temp.push(a(item.name, self.color[index], item.data))
    })
    this.series = temp
    return {
      chart: null,
      opts: {
        chart: {
          renderTo: "container-" + this.id,
          type: 'areaspline',
          backgroundColor:""
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
          floating: true,
          backgroundColor: this.color.plotBackgroundColor
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
        plotOptions: {
        },
        tooltip: {
          backgroundColor:"rgba(0,0,0,0.25)",
          borderWidth:0,
          style: {
            padding: 10,
            color:"#9abcee"
          },
          formatter: function () {
            var date = Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x)
            var s = '<span>' + date + '</span>'
              $.each(this.points, function () {
                s += '<br/>' + this.series.name + ': ' + self.countUnit(this.y)
              })
            return s
          },
          shared: true
        },
        series: this.series
  		}
    }
  },
  created: function() {
  },
  methods: {
    initChart: function(minTime) {
      var self = this
      for(var i=0; i < this.chart.series.length; i++ ){
        this.chart.series[i].setData(self.makePoint(minTime[i]))
      }
    },
    addPoint: function(point) {
      for(var i=0; i < this.chart.series.length; i++ ){
        this.chart.series[i].addPoint(point[i], true, true)
      }
    },
    makePoint: function (num) {
      var initData = []
      var x,y = 0
      for (var i = 10; i >=1; i--) {
        x = num - i * 1000;
        initData.push([x, y])
      }
      return initData
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
      }else if (this.yaxe=="ms"){
        return  this.yaxe+":"+ val + "ms"
      }else{
        return  val + "个"
      }
    }
  },
  ready: function() {
    this.chart = new Highcharts.Chart(this.opts)
  }
}
</script>
