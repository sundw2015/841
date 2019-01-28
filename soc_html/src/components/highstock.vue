<template>
  <div :id="container" style="height: 300px;background:none"></div>
</template>
<style>
  .highcharts-title {
    font-size: 18px !important;
  }
</style>
<script>
  var Highcharts = require('highcharts')
  var Highstock = require('highcharts/highstock')
  //require('highcharts/modules/exporting')(Highcharts)

  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });


  export default {
    props: ['title', 'container', 'color', 'yaxe'],
    data: function () {
      let self = this;
      return {
        chart: null,
        opts: {
          chart: {
            renderTo: this.container,
            type: 'areaspline',
            backgroundColor: null,
          },
          title: {
            text: this.title,
            style: {
              color: "#fff"
            }
          },
          navigator: {
            adaptToUpdatedData: true,//导航条背景是否显示数据线
            xAxis: {
              minRange: 60 * 1000,// one minute
              labels: {
                formatter: function (e) {
                  return Highcharts.dateFormat('%m-%d', this.value);
                }
              }
            },
            series: {
              lineWidth: 1,
              lineColor: this.color.lineColor
            },
            maskFill: Highcharts.Color(this.color.lineColor).setOpacity(0.1).get('rgba')
          },
          scrollbar: {
            liveRedraw: true//拖动滚动条是否在显示区域动画
          },
          rangeSelector: {
            buttons: [{
              type: 'hour',
              count: 1,
              text: '1小时',
            }, {
              type: 'day',
              count: 1,
              text: '1天'
            }, {
              type: 'week',
              count: 1,
              text: '1周'
            }, {
              type: 'month',
              count: 1,
              text: '1月'
            }, {
              type: 'all',
              count: 1,
              text: '全部',
            }],
            buttonTheme: { // styles for the buttons
              fill: 'none',
              stroke: 'none',
              'stroke-width': 0,
              r: 8,
              style: {
                color: '#666',
                fill: '#666',
              },
              states: {
                hover: {
                  fill: 'none',
                  style: {
                    color: '#fff'
                  }
                },
                select: {
                  fill: 'none',
                  style: {
                    color: '#fff'
                  }
                },
                disabled: {
                  style:{
                    color: '#666',
                  },
                  fill: 'none',
                }
              }
            },
            selected: 4,//数值代表buttons的索引
            inputEnabled: false
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
            title: {
              text: "小时/分/秒",
              style: {
                color: "#fff"
              }
            },
            type: 'datetime',
            plotBands: [{ // visualize the weekend
              from: 0,
              to: 100,
              color: 'rgba(245, 245, 245, 1)'
            }],
            labels: {
              formatter: function () {
                return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.value);
              }
            }
          },
          yAxis: {
            title: {
              text: this.yaxe,
              style: {
                color: "#fff"
              }
            },
          },
          tooltip: {
            formatter: function () {
              return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + self.countUnit(this.y);
            }
          },
          plotOptions: {
            areaspline: {
              marker: {
                enabled: false, //是否显示点
                radius: 2,
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
          series: [{
            name: '',
            color: this.color.color,
            lineWidth: 1,
            lineColor: this.color.lineColor,
            fillColor: {
              linearGradient: {x1: 0, y1: 0, x2: 0, y2: 1},
              stops: [[0, this.color.stopsA], [1, Highcharts.Color(this.color.stopsB).setOpacity(0.5).get('rgba')]]
            },
            data: []//stockDataS
          }]
        }
      }
    },
    methods: {
      resetChart: function () {
        this.chart.rangeSelector.clickButton(4, {}, true);
      },
      setData: function (data) {
        this.chart.series[0].setData(data)
      },
      countUnit: function (val) {
        if (this.yaxe == "流量") {
          if (val < 1024) {
            return this.yaxe + ":" + val + "b"
          } else if (val >= 1024 && val < 1024 * 1024) {
            val = (val / 1024).toFixed(1);
            return this.yaxe + ":" + val + "Kb"
          } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
            val = (val / (1024 * 1024)).toFixed(1);
            return this.yaxe + ":" + val + "Mb"
          } else if (val >= 1024 * 1024 * 1024) {
            val = (val / (1024 * 1024 * 1024)).toFixed(1);
            return this.yaxe + ":" + val + "Gb"
          }

        } else {
          return this.yaxe + ":" + val + "个"
        }
      }
    },
    ready: function () {
      this.chart = new Highstock.StockChart(this.opts);
    }
  }
</script>
