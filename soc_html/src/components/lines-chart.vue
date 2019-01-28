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
        default: ""
      },
      unit:{
        default: ""
      }
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
      self.lineOption = {
        tooltip : {
          trigger: 'axis',
          axisPointer:{
            lineStyle:{
              color: "#dfdfe7",
              opacity:0.2
            },
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
            axisLabel:{textStyle:{color:"#dfdfe7"},},//y轴坐标的字颜色
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
        if(typeof this.y[0] == 'object'){
          for(var i in this.y){
            var name = this.name[i]
            this.lineOption.series[i] = {
              name: name,
              type:'line',
              smooth:true,
              itemStyle: {
                normal: {
                  color: this.color[i]
                }
              },
              areaStyle:{
                normal: {
                  color: this.color[i],
                  opacity:0.4
                }
            },
            data: this.y[i]
          }
          }
          this.chart.setOption(this.lineOption);
        }else {
          this.chart.setOption(this.lineOption);
        }
      },
      setData(time, data){
        this.lineOption.xAxis[0].data = time
        this.lineOption.series[0].data = data
        this.setChart()
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
    /*
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
    */
  }
</script>