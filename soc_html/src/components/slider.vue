<template>
  <div class="fLeft d-i-b" v-bind:style="{width: width}">
    <div class="ys-slider ">
      <p class="slider-line" v-el:line @click="sliderMove">
        <span class="slider-selected" v-bind:style="{width: slider.width}" v-el:selected></span>
        <a class="slider-btn" @mousedown="sliderDown">
          <i class="ys-icon icon-arrow-right"></i>
        </a>
      </p>
    </div>
  </div>
  <input class="ys-input fLeft d-i-b"
         style="width: 80px; margin-left: 30px"
         type="number"
         v-model.number="value"
         @input="changeValue"
         v-bind:max="range[1]"
         v-bind:min="range[0]">
  <span class="m-l-5" style="line-height:30px;">{{unit}}</span>
</template>

<style>
  .ys-slider p.slider-line {
    padding: 0;
    margin: 10px auto;
    height: 6px;
    text-align: left;
    border-radius: 8px;
    background:#46578e;
    /*background: linear-gradient(left,#f6587c,#2c7edc 100%);*/
    /*background: -o-linear-gradient(left,#f6587c,#2c7edc 100%);*/
    /*background: -ms-linear-gradient(left,#f6587c,#2c7edc 100%);*/
    /*background: -moz-linear-gradient(left,#f6587c,#2c7edc 100%);*/
    /*background: -webkit-linear-gradient(left,#f6587c,#2c7edc 100%);*/
  }
  .ys-slider .slider-selected {
    color: #fff;
    background: #00bd85;
    display: block;
    width: 80%;
    height: 6px;
    line-height: 6px;
    text-align: right;
    float: left;
    border-radius: 8px;
  }
  .ys-slider .slider-btn {
    background:linear-gradient(to bottom, #ffffff, #c1d4f1);
    opacity: 1;
    width: 12px;
    height: 12px;
    font-size: 12px \9;
    font-size: .75rem;
    line-height: 0;
    position: absolute;
    border:none;
    border-radius: 1.5em;
    margin-top: -0.25em;
    text-align: center;
    margin-left: -0.5em;
    display: inline-block;
    float: left;
  }
  .ys-slider .slider-line:hover .slider-btn{
    opacity: 1;
  }
  .ys-slider .slider-btn i{
    transform: scale(1,1);
    margin-left:0.5px;
  }
</style>

<script>
  export default {
    props: {
      value: {
        default: 0
      },
      range: {
        default: [0,100]
      },
      width: {
        default: '400px'
      },
      unit:{
        default:""
      }
    },
    data () {
      return {
        slider: {
          width: '0%',
          _range: [],
        }
      }
    },
    ready: function () {
      this.slider._range = this._range(this.range)
      $(document).on("mouseup","body", function () {
          $(document).off("mousemove")
        })
      this.slider.ml = $(this.$els.line).offset().left
      this.slider.all_width = $(this.$els.line).width()
    },

    methods: {
      _range (range) {
        let l = []
        for(let i =0; i<range[1]; i++){
          if(i>range[0]){
            l.push(i)
          }
        }
        return l
      },
      sliderDown(e){
        $(document).on("mousemove",e, this.sliderMove)
      },
      sliderMove(e){
        e = event || e
        let mouseX = e.pageX
        let p = (mouseX - this.slider.ml) / this.slider.all_width * 100
        if(p >= 100){
          this.slider.width = '100%'
          this.value = this.range[1]
          return
        }
        if(p <= 0){
          this.slider.width = '0%'
          this.value = this.range[0]
          return
        }

        this.slider.width = p + '%'
        if(p == 100){
          this.value = this.range[1]
          return
        }
        let a = parseInt(p / (100 / this.slider._range.length))
        this.value = this.slider._range[a]
      },
      changeValue(){
        this.value = parseInt(this.value)
        if(this.value >= this.range[1]){
          this.slider.width = '100%';
          this.value=this.range[1];
        }else if(this.value <= this.range[0]){
          this.slider.width = '0%'
          this.value=this.range[0];
        }else{
          let index = this.slider._range.indexOf(parseInt(this.value))

          this.slider.width = (index / this.slider._range.length * 100) + '%'
        }
      }
    },
    components: {},

    watch: {
      value: function () {
        this.changeValue()
      }
    }

  }
</script>