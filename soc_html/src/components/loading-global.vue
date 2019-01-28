<template>
  <div class="ys-loader" v-if="show">
    <div class="loader1">
      <div class="loader-con">
        <div class="rotate-circle">
          <?xml version="1.0" encoding="utf-8"?>
          <!-- Generator: Adobe Illustrator 18.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
          <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
          <svg version="1.1" id="图层_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 80 80" enable-background="new 0 0 80 80" xml:space="preserve">
<path fill-rule="evenodd" clip-rule="evenodd" fill="#273141" d="M3.2,24.3C12,4,35.5-5.3,55.8,3.5C76.1,12.2,85.4,35.7,76.7,56
	c-8.8,20.3-32.3,29.6-52.6,20.9C3.8,68.1-5.5,44.6,3.2,24.3z"/>
<g>
	<g>
		<linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="39.9479" y1="73.94" x2="39.9479" y2="6.3933">
			<stop  offset="0" style="stop-color:#4A92FF"/>
			<stop  offset="1" style="stop-color:#00BD85"/>
		</linearGradient>
		<path fill="url(#SVGID_1_)" d="M39.9,6.4C21.3,6.4,6.2,21.5,6.2,40.2c0,18.7,15.1,33.8,33.8,33.8c18.7,0,33.8-15.1,33.8-33.8
			C73.7,21.5,58.6,6.4,39.9,6.4z M39.9,68.9c-15.9,0-28.8-12.9-28.8-28.8c0-15.9,12.9-28.8,28.8-28.8c15.9,0,28.8,12.9,28.8,28.8
			C68.7,56.1,55.8,68.9,39.9,68.9z"/>
	</g>
</g>
<radialGradient id="SVGID_2_" cx="39.9479" cy="15.2513" r="7.0625" gradientTransform="matrix(1.2509 0 0 1.2509 -10.0215 -10.0764)" gradientUnits="userSpaceOnUse">
	<stop  offset="0.1925" style="stop-color:#71FFD5"/>
	<stop  offset="1" style="stop-color:#71FFD5;stop-opacity:0"/>
</radialGradient>
<circle fill="url(#SVGID_2_)" cx="39.9" cy="9" r="8.8"/>
<circle fill="#A9FFE2" cx="39.9" cy="8.9" r="2.5"/>
</svg>

        </div>
        <div class="loading-text ys-info-color">loading...</div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    props: {
      show: {
        default: false
      },
    },
    data () {
      return {

      };
    },
    methods: {
      handleShowPopper() {

      }
    },
    watch: {
      show(val) {
        let self=this;
//        setTimeout(function(){
//          if(self.show){
//            self.show=false;
//          }
//        },15000)
      }
    },
  };
</script>
<style scoped>
  /* -------------- Loader1 -------------- */
  .ys-loader{
    width:100%;
  }
  .ys-loader:before{
    content: '';
    width:100%;
    height:100%;
    position:fixed;
    top:0px;
    left:0px;
    background:rgba(0,0,0,0.1);
    z-index: 99;
  }
  .loader1{
    position: fixed;
    z-index: 100;
    height: 80px;
    width: 80px;
    top: 28%;
    top: -webkit-calc(50% - 80px);
    top: calc(50% - 80px);
    left: 35%;
    left: -webkit-calc(50% - 0px);
    left: calc(50% - 0px);
    -webkit-transform-origin: 50% 50%;
    transform-origin: 50% 50%;
  }
  .loader-con{
    position: relative;
  }
  .rotate-circle{
    position:absolute;
    top:0px;
    left:0px;
    height: 80px;
    width: 80px;
    border-radius: 50%;
    -webkit-animation: loader1 1.5s linear infinite;
    animation: loader1 1.5s linear infinite;
    box-shadow:0px 0px 200px rgba(255,255,255,0.5);
    -moz-box-shadow:0px 0px 200px rgba(255,255,255,0.5);
    -webkit-box-shadow:0px 0px 200px rgba(255,255,255,0.5);
  }
  .loading-text{
    position:absolute;
    top:0px;
    left:0px;
    height: 80px;
    width: 80px;
    text-align:center;
    line-height:80px;
    font-size:10px;
    font-weight:100;
    font-family: Arial;
    -webkit-transform:scale(0.9);

  }
  @-webkit-keyframes loader1{
    0%{-webkit-transform:rotate(0deg);}
    100%{-webkit-transform:rotate(360deg);}
  }

  @keyframes loader1{
    0%{transform:rotate(0deg);}
    100%{transform:rotate(360deg);}
  }

</style>