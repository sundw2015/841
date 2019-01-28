<template>
  <div class="ys-loader" v-if="show">
    <span class="circle1"></span>
    <span class="circle2"></span>
    <span class="circle3"></span>
    <span class="circle4"></span>
  </div>
</template>
<script>
  export default {
    name:"loading-normal",
    props: {
      show: {
        default: false
      }
    },
    data () {
      return {
        //visible:false
      };
    },
  };
</script>
<style scoped>
  .ys-loader{
    display:inline-block;
  }
  .ys-loader>span{
    display:inline-block;
    width: 6px;
    height: 6px;
    border-radius: 5px;
    margin-right:5px;
  }
  .ys-loader .circle1{
    -webkit-animation: loader1 1.2s ease-in-out infinite;
    animation: loader1 1.2s ease-in-out infinite;
  }
  .ys-loader .circle2{
    -webkit-animation: loader2 1.2s ease-in-out infinite;
    animation: loader2 1.2s ease-in-out infinite;
  }
  .ys-loader .circle3{
    -webkit-animation: loader3 1.2s ease-in-out infinite;
    animation: loader3 1.2s ease-in-out infinite;
  }
  .ys-loader .circle4{
    -webkit-animation: loader4 1.2s ease-in-out infinite;
    animation: loader4 1.2s ease-in-out infinite;
  }

  @-webkit-keyframes loader1{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(255, 255, 255, 1);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }
  @keyframes loader1{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(0, 189, 133, 1);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }

  @-webkit-keyframes loader2{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(0, 189, 133, 1);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }
  @keyframes loader2{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(0, 189, 133, 1);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }

  @-webkit-keyframes loader3{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(0, 189, 133, 1);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }
  @keyframes loader3{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(0, 189, 133, 1);}
    100%{background-color: rgba(74, 146, 255, .4);}
  }

  @-webkit-keyframes loader4{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(0, 189, 133, 1);}
  }
  @keyframes loader4{
    0%{background-color: rgba(74, 146, 255, .4);}
    25%{background-color: rgba(74, 146, 255, .4);}
    50%{background-color: rgba(74, 146, 255, .4);}
    75%{background-color: rgba(74, 146, 255, .4);}
    100%{background-color: rgba(0, 189, 133, 1);}
  }

</style>