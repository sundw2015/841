<template>
  <div class="ys-mon-table-chart">
    <div id="chart-{{ id }}" v-bind:style="{width: width,height:height}"></div>
  </div>
</template>
<style>
.ys-mon-table-chart {
}
.ys-mon-table-chart>div{
}
</style>
<script>
  let echarts =  require('echarts/lib/echarts');
  export default {
    props: {
      x: {
        default: []
      },
      y: {
        default: []
      },
      id: {
        default: 0
      },
      name:{
        default: ""
      },
      width:{
        default: "100%"
      },
      height:{
        default: "200px"
      },
      line:{
        default: true
      },
      color:{
        default: "#f1eb37"
      },
      unit:{
        default: ""
      },
    },
    data () {
      return {
        chart:"",
        option:"",
        lineOption:""
      }
    },
    ready(){
      let self=this
      self.chart = echarts.init(document.getElementById('chart-'+this.id));
      self.option = {
        tooltip : {
          trigger: 'axis',
          axisPointer:{
            lineStyle:{
              color: "#dfdfe7",
              opacity:0.2
            },
          },
          formatter: function (params) {
            if(self.unit=="band"){
              return params[0].name+"<br/>"+params[0].seriesName+":"+self.changeUnit(params[0].value)
            }else if(self.unit=="%"){
              var num = params[0].value*100
              num = num.toFixed(0)
              return params[0].name+"<br/>"+params[0].seriesName+":"+num+"%"
            }else{
              return params[0].name+"<br/>"+params[0].seriesName+":"+params[0].value
            }
          }
        },
        grid: {
          show:false,
          top:3,
          left:0,
          right:0,
          bottom:3,
          containLabel: false,
        },
        legend: {
          data:[self.name],
          show:false
        },
        toolbox: {
          show : false
        },
        calculable : true,
        xAxis : [
          {
            type : 'category',
            data : self.x,
            axisLine:{
              show:false,
            },
            axisTick: {
              show:false,
            },
            axisLabel:{
              show:false,
            },//x轴坐标的字颜色
          }
        ],
        yAxis : [
          {
            type : 'value',
            axisLine:{
              show:false,
            },
            axisTick: {
              show:false,
            },
            axisLabel:{
              show:false,
            },
            splitLine:{
              show:false,
            }
          }
        ],
        series : [
          {
            name:self.name,
            type:'line',
            data:self.y,
            smooth:true,
            itemStyle: {
              normal: {
                color: self.color,
                borderColor:self.color,
                borderWidth:"1",
              }
            },
            areaStyle:{
              normal: {
                color: self.color,
                opacity:0.4,
              }
            },
            lineStyle:{
              normal: {
                color: self.color,
                width:2,
              }
            },
          }
        ]
      };
      self.lineOption = {
        tooltip : {
          trigger: 'axis',
          axisPointer:{
            lineStyle:{
              color: "#dfdfe7",
              opacity:0.2
            },
          },
          formatter: function (params) {
            if(self.unit=="band"){
              return params[0].name+"<br/>"+params[0].seriesName+":"+self.changeUnit(params[0].value)
            }else if(self.unit=="%"){
              var num = params[0].value*100
              num = num.toFixed(0)
              return params[0].name+"<br/>"+params[0].seriesName+":"+num+"%"
            }else{
              return params[0].name+"<br/>"+params[0].seriesName+":"+params[0].value
            }
          }
        },
        grid: {
          top: '30',
          bottom:'40',
          left:20,
          right:20,
          containLabel: true
        },
        toolbox: {
          show : true
        },
        calculable : true,
        xAxis : [
          {
            type : 'category',
            data : self.x,
            axisLine:{
              show:true,
              lineStyle:{
                color:"#dfdfe7",
                opacity:"0.2"
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
                color:"#dfdfe7",
                opacity:"0.2"
              }
            },
            axisTick: {
              show:false,
            },
            splitNumber:5,
            axisLabel:{
              textStyle:{color:"#dfdfe7"},
//              formatter: function(params){
//                if(self.unit=="%"){
//                  var num = params[0].value*100
//                  num = num.toFixed(0)
//                  return params[0].name+"<br/>"+params[0].seriesName+":"+num+"%"
//                }else{
//                  return params
//                }
//              },
            },//y轴坐标的字颜色
            splitLine:{
              lineStyle:{
                color:"#dfdfe7",
                opacity:"0.2"
              }
            }
          }
        ],
        series : [
          {
            name: self.name,
            type:'line',
            smooth:true,
            itemStyle: {
              normal: {
                color: self.color,
              }
            },
            areaStyle:{
              normal: {
                color: self.color,
                opacity:0.4,
              }
            },
            data:self.y
          },
        ]
      };
      self.setChart()
    },
    methods:{
      setChart(){
        if(this.line==1){
          this.chart.setOption(this.lineOption);
        }else{
          this.chart.setOption(this.option);
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
      }
    },
    watch: {
      'x': function(){
        if(this.line == 1){
          this.lineOption.xAxis[0].data = this.x
          this.setChart()
        }
      },
      'y': function(){
        if(this.line == 1){
          this.lineOption.series[0].data = this.y
          this.setChart()
        }
      }
    }
  }
</script>