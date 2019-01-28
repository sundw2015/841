<template>
  <div id="multi-his-chart-{{ id }}" v-bind:style="{width: width,height:height}" class="his-chart"></div>
</template>
<style>
  .his-chart {
    margin: 0px auto;
  }
</style>
<script>
  let echarts = require('echarts/lib/echarts');
  export default {
    props: {
      id: {
        default: 0
      },
      name: {
        default: ""
      },
      width: {
        default: "95%"
      },
      height: {
        default: "500px"
      },
      color: {
        default: '#e7e4f1'
      },
      unit: {
        default: ''
      },
      x: {
        default: []
      },
      y: {
        default: []
      },
    },
    ready(){

    },
    methods: {
      setChart(){
        let self = this
        self.chart = echarts.init(document.getElementById('multi-his-chart-' + this.id));
          for(let idx in self.y){
          self.y[idx] = {
            smooth:true,
            name: self.name[idx],
            type:'line',
            xAxisIndex: idx,
              yAxisIndex: idx,
            itemStyle: {
              normal: {
                color: self.color[idx],
                borderColor:self.color[idx]
              },
              emphasis:{
                color: "rgba(70,66,67,1)",
                borderColor:self.color[idx]
              }
            },
            lineStyle: {
              normal: {
                color: self.color[idx],
              }
            },
            areaStyle:{
              normal: {
                color: self.color[idx],
                opacity:0.3,
              }
            },
            data:self.y[idx]
          }
        }
        this.option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: "#dfdfe7",
                opacity: 0.2
              },
            },
            formatter: function (params) {
              let str = params[0].name
              for (var i = 0; i < params.length; i++) {
                if (self.unit == "band") {
                  str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                }
                else if (self.unit == 'kw') {
                  str += "<br/>" + params[i].seriesName + ":" + self.KWUnit(params[i].value)
                } else {
                  str += "<br/>" + params[i].seriesName + ":" + params[i].value
                }
              }
              return str
            },
          },
          dataZoom: [
            {
              show: true,
              realtime: true,
              start: 0,
              end: 100,
              dataBackground:{
                lineStyle:{
                  color:self.color,
                  width:1
                },
                areaStyle:{
                  color:self.color
                }
              },
              xAxisIndex: [0, 1]
            },
            {
              type: 'inside',
              realtime: true,
              start: 65,
              end: 85
            }
          ],
          calculable : true,
          connectNulls:true,
          grid: [{
            left:10,
            right:10,
            containLabel: true,
            height: '40%',
            top: 20,
          }, {
            left:10,
            right:10,
            containLabel: true,
            top: '50%',
            height: '40%'
          }],
          xAxis: [
            {
              type: 'category',
              data: self.x,
              axisLine: {
                show: true,
                lineStyle: {
                  color: "#dfdfe7",
                  opacity: "0.2"
                }
              },
              axisTick: {
                show: false,
              },
              axisLabel: {textStyle: {color: "#dfdfe7"}}
            },
            {
              gridIndex: 1,
              type: 'category',
              data: self.x,
              axisLine: {
                show: true,
                lineStyle: {
                  color: "rgba(55, 200, 118, 1)",
                  opacity: "0.2"
                }
              },
              axisTick: {
                show: false,
              },
              axisLabel: {textStyle: {color: "#dfdfe7"}}
            }
          ],
          yAxis: [
            {
              type: 'value',
              axisLine: {
                show: true,
                lineStyle: {
                  color: "#dfdfe7",
                  opacity: "0.2"
                }
              },
              axisTick: {
                show: false,
              },
              splitNumber: 5,
              axisLabel: {
                textStyle: {color: "#dfdfe7"},
                formatter: function (value) {
                  if (self.unit == "band") {
                    return self.changeUnit(value)
                  } else if (self.unit == 'kw') {
                    return self.KWUnit(value)
                  } else {
                    return value
                  }
                },
              },//y轴坐标的字颜色
              splitLine: {
                lineStyle: {
                  color: "#dfdfe7",
                  opacity: "0.2"
                }
              }
            },
            {
              gridIndex: 1,
              type: 'value',
              axisLine: {
                show: true,
                lineStyle: {
                  color: "rgba(55, 200, 118, 1)",
                  opacity: "0.2"
                }
              },
              axisTick: {
                show: false,
              },
              splitNumber: 5,
              axisLabel: {
                textStyle: {color: "#dfdfe7"},
                formatter: function (value) {
                  if (self.unit == "band") {
                    return self.changeUnit(value)
                  } else if (self.unit == 'kw') {
                    return self.KWUnit(value)
                  } else {
                    return value
                  }
                },
              },//y轴坐标的字颜色
              splitLine: {
                lineStyle: {
                  color: "#dfdfe7",
                  opacity: "0.2"
                }
              }
            }
          ],
          series: self.y
        };
        self.chart.setOption(self.option);
        window.onresize = function () {
          self.chart.resize();
        }
      },
      changeUnit(val){
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
      KWUnit(val){
        if (val < 1000) {
          return val + "个"
        } else if (val >= 100 && val < 1000) {
          val = (val / 100).toFixed(1);
          return val + "百"
        } else if (val >= 1000 && val < 10000) {
          val = (val / 1000).toFixed(1);
          return val + "千"
        } else if (val >= 10000) {
          val = (val / (10000)).toFixed(1);
          return val + "万"
        }
      }
    },
    watch: {
      'y': function () {
        this.setChart();
      }
    }
  }
</script>