<template>
  <div id="his-chart-{{ id }}" v-bind:style="{width: width,height:height}" class="his-chart"></div>
</template>
<style>
  .his-chart{
    margin:0px auto;
  }
</style>
<script>
  let echarts =  require('echarts/lib/echarts');
  export default {
    props: {
      id: {
        default: 0
      },
      name:{
        default: ""
      },
      width:{
        default: "95%"
      },
      height:{
        default: "200px"
      },
      color:{
        default: '#e7e4f1'
      },
      unit: {
        default: ''
      },
      x:{
        default: []
      },
      x_type: {
        default: 'category'
      },
      y:{
        default: []
      },
      smooth: {
        default: false
      }
    },
    ready(){

    },
    methods:{
      setChart(){
        let self=this
        self.chart = echarts.init(document.getElementById('his-chart-'+this.id));
        this.option = {
          tooltip : {
            trigger: 'axis',
            axisPointer:{
              lineStyle:{
                color: "#dfdfe7",
                opacity:0.2
              },
            },
            formatter: function (params) {
              let str=params[0].name
              for(var i=0;i<params.length;i++){
                if(self.unit=="band"){
                  str += "<br/>"+params[i].seriesName+":"+self.changeUnit(params[i].value)
                }
                else if(self.unit=='kw'){
                  str += "<br/>"+params[i].seriesName+":"+self.KWUnit(params[i].value)
                }
                else if(self.unit=='kwe'){
                  str += "<br/>"+params[i].seriesName+":"+self.KWEUnit(params[i].value)
                }else{
                  str += "<br/>"+params[i].seriesName+":"+params[i].value
                }
              }
              return str
              },
          },
          grid: {
            top: '10',
            bottom:'40',
            left:20,
            right:20,
            containLabel: true
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
              fillerColor: 'rgba(167,183,204,0.15)',
              handleStyle: {
                color: self.color,
              },
              zoomOnMouseWheel:false
//              borderColor: 'rgb(255,255,255,0)'
            },
            {
              type: 'inside',
              realtime: true,
              start: 65,
              end: 85,
              zoomOnMouseWheel:false
            }
          ],
          calculable : true,
          connectNulls:true,
          xAxis : [{
            type : self.x_type,
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
            axisLabel:{textStyle:{color:"#dfdfe7"}}
          }],
          yAxis : [{
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
              formatter: function(value){
                if(self.unit=="band"){
                  return self.changeUnit(value)
                }else if(self.unit=='kw'){
                  return self.KWUnit(value)
                }else if(self.unit=='kwe'){
                  return self.KWEUnit(value)
                }else{
                  return value
                }
              },
            },//y轴坐标的字颜色
            splitLine:{
              lineStyle:{
                color:"#dfdfe7",
                opacity:"0.2"
              }
            }
          }],
          series : [{
            name: self.name,
            type:'line',
            itemStyle: {
              normal: {
                color: self.color,
                borderColor:self.color
              },
              emphasis:{
                color: "rgba(78,66,167,1)",
                borderColor:self.color
              }
            },
            smooth: self.smooth,
            lineStyle: {
              normal: {
                color: self.color,
              }
            },
            areaStyle:{
              normal: {
                color: self.color,
                opacity:0.3,
              }
            },
            data:self.y
          },]
        };
        self.chart.setOption(self.option);
        window.onresize = function () {
          self.chart.resize();
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
      },
      KWUnit(val){
        // 中文书写
        if(val<1000){
          return  val + "个"
        }else if(val>=100 && val<1000){
          val=(val/100).toFixed(1);
          return  val + "百"
        }else if(val>=1000 && val<10000){
          val=(val/1000).toFixed(1);
          return  val + "千"
        }else if(val>=10000){
          val=(val/(10000)).toFixed(1);
          return  val + "万"
        }
      },
      KWEUnit(val){
        // 英文缩写
        if(val<1000){
          return  val
        }else if(val>=1000 && val<1000*1000){
          val=(val/1000).toFixed(1);
          return  val + "K"
        }else if(val>=1000*1000 && val<1000*1000*1000){
          val=(val/(1000*1000)).toFixed(1);
          return  val + "M"
        }else if(val>=1000*1000*1000){
          val=(val/(1000*1000*1000)).toFixed(1);
          return  val + "G"
        }
      }
    },
    watch: {
      'y': function(){
        this.setChart()
      }
    }
  }
</script>