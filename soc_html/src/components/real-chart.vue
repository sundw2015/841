<template>
  <div :id="id" style="height: 300px;background:none"></div>
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
    props: ['id','color','yaxe'],
    data: function() {
      let self=this;
      return {
        chart: null,
        opts: {
          chart: {
            renderTo: this.id,
            type: 'areaspline',
            backgroundColor:""
          },
          title: {
            text: null,
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
          },
          xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            title: {
              text: "小时/分/秒",
              style:{
                color:"#fff"
              }
            },
            labels:{
              style: {color:'#fff'}
            }
          },
          yAxis: {
            title: {
              text: this.yaxe,
              style:{
                color:"#fff"
              },
            },
            labels:{
              style: {color:'#fff'}
            },
            plotLines: [{
              value: 0,
              width: 1,
              color: '#000000'
            }]
          },
          plotOptions: {
            areaspline: {
              lineWidth: 2,
              lineColor: "#0f72c7",//线的颜色
              fillColor: {
                linearGradient: {
                  x1: 0,
                  y1: 0,
                  x2: 0,
                  y2: 1
                },
                stops: [[0, this.color.stopsA], [1, Highcharts.Color(this.color.stopsB).setOpacity(0.5).get('rgba')]]
              },
              marker: {
                enabled: true, //是否显示点
                radius: 4,
                states: {
                  hover: {
                    enabled: true,
                    radius: 4
                  }
                }
              },
              shadow: false
            }
          },
          tooltip: {
            backgroundColor: 'rgba(50,50,50,0.7)',
            shadow:false,
            borderWidth: 0,
            style:{
              color:"#fff",
            },
            formatter: function () {
              return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + self.countUnit(this.y);
            }
          },
          series: [{
            name: "",
            color: this.color.color,
            data: []
          }]
        },
        chartData:[]
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
        }else if (this.yaxe=="ms"){
          return  this.yaxe+":"+ val + "ms"
        }else{
          return  this.yaxe+":"+ val + "个"
        }
      },
      requestRealData: function(first) {
        first = first || 0
        this.$http.get({'url': '/api/hw/ip/realtime?hw_ip=1.1.1.1', 'timeout': 8000}).then(function (response) {
          this.chartData = response.data.data.throughput
          if (first) {
            this.initChart(this.chartData[0][0])
            this.dataTimer = setInterval(this.requestRealData.bind(this), 10000)
            this.chartTimer = setInterval(this.updateRealChart.bind(this), 1000)
          }
          this.updateRealChart()
        }, function(response){
          Api.user.requestFalse(response,this);
        })
      },
      updateRealChart: function() {
        if (this.chartData.length > 0) {
          var curpoint = this.chartData.shift()
          this.addPoint(curpoint, true, true)
        }
      },
    },
    ready: function() {
      this.chart = new Highcharts.Chart(this.opts);
      this.requestRealData(1)
    },
    watch: {
      'url': function(){
        this.requestRealData(1)
      }
    },
  }
</script>
