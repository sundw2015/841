<template>
  <canvas id="myCanvas" width="1000" height="300" ></canvas>
  <div id="dummy"></div>
  <p id="log"></p>
</template>
<script>
  export default {
    ready: function() {
      function toRad(Value) {
        /** Converts numeric degrees to radians */
        return Value * Math.PI / 180;
      }

      function logInfo(text){
        $( "p" ).text(text);
      }

      var blueRadius = 52;
      var tickersRadius = 10;
      var tickerUpdate = 0.25;

      $( "canvas" ).mousedown(
              function() {
                $('#dummy').animate({'height':'100px'},{
                  duration: 150,
                  queue: false,
                  step: function(now){
                    blueRadius = 70 + now/3;
                    tickersRadius = 80 - now*1.25/5;
                    plusSize = 0 + now*8/100;
                    tickerUpdate = 0.35;
                    tickerColor = colYellow;
                    outerRingColor = colGrey;
                    outerRingGlow = colGrey;
                  }
                });
              }).
      mouseup(
              function() {
                $('#dummy').animate({'height':'0'},{
                  duration: 300,
                  queue: false,
                  step: function(now){
                    blueRadius = 70 + now/3;
                    tickersRadius = 80 - now/5;
                    plusSize = 2 + now*8/100;
                    tickerUpdate = 0.15;
                    tickerColor = colGrey;
                    outerRingColor = colCyan;
                    outerRingGlow = shaCyan;
                  }
                });
              }
      );
      $("#myCanvas").bind('mousemove',function(e){
        var parentOffset = $(this).parent().offset();
        //or $(this).offset(); if you really just want the current element's offset
        var relX = e.pageX - parentOffset.left;
        var relY = e.pageY - parentOffset.top;
        center.x = relX;
        center.y = relY;
        //       logInfo("e.pageX: " + relX + ", e.pageY: " + relY);
      });



      var canvas = document.getElementById('myCanvas');
      console.log(canvas);
      var context = canvas.getContext('2d');
      context.globalCompositeOperation = "lighter";

      var colYellow = "#f7b910";
      var colLightYellow = "rgba(247,185,16,.5)"
      var colCyan = "#2fede7";
      var shaCyan = "rgba(47,237,231, 0.3)";
      var colGrey = "rgba(255,255,255,0.2)";
      var center = {x:200,y:150};
      var plusSize = 2;

      var tickerColor = colGrey;
      var tickerGlow = "rgba(255,255,255,0)";

      var outerRingColor = colCyan;
      var outerRingGlow = shaCyan;

      var greyGrad = context.createLinearGradient(0, 100, 200, 190);
      greyGrad.addColorStop(0, "rgba(255,255,255,0.15)");
      greyGrad.addColorStop(1, "rgba(255,255,255,0)");

      // Animation function
      var requestAnimationFrame =
              window.requestAnimationFrame ||
              window.webkitRequestAnimationFrame ||
              window.mozRequestAnimationFrame ||
              window.msRequestAnimationFrame ||
              window.oRequestAnimationFrame ||
              function(callback) {
                return setTimeout(callback, 1);
              };


      function drawCrosshair(size){

        // Plus - horizontal
        context.strokeStyle = colYellow;
        context.lineWidth = 2;
        context.shadowColor = colYellow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;
        context.save();
        context.translate(center.x, center.y);
//context.rotate(toRad(plusAngle));
        context.beginPath();
        context.moveTo(-size, 0);
        context.lineTo(size, 0);
        context.stroke();

        context.beginPath();
        context.moveTo(0, -size);
        context.lineTo(0, size);
        context.stroke();
        context.restore();
      }

      function drawTicker(angle, radius, len, width, color, glow){
        // Plus - horizontal
        context.strokeStyle = color;
        context.lineWidth = width;
        context.shadowColor = glow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;
        context.save();
        context.beginPath();
        var aX = center.x + (radius+len)*Math.cos(toRad(angle));
        var aY = center.y + (radius+len)*Math.sin(toRad(angle));
        var bX = center.x + (radius)*Math.cos(toRad(angle));
        var bY = center.y + (radius)*Math.sin(toRad(angle));
        context.moveTo(aX, aY);
        context.lineTo(bX, bY);
        context.stroke();
        context.restore();
      }


      function drawSet(numberOfTickers, radius, len, width, color, glow, angleOffset){
        for (var i=0;i < numberOfTickers; i++){
//    drawTicker(angleOffset + i*(360/numberOfTickers), 60, 4, 2, "rgba(255,255,255,.15)", "rgba(255,255,255,.2)");
          drawTicker(angleOffset + i*(360/numberOfTickers), radius, len, width, color, glow);
        }
      }



      function drawVerticalLine(offset, lineWidth){
        // Plus - horizontal
        context.lineWidth = lineWidth;

        context.save();
        context.beginPath();

        context.moveTo(offset, 0);
        context.lineTo(offset, canvas.height);
        context.stroke();
        context.restore();
      }

      function drawHorizontalLine(offset, lineWidth){
        // Plus - horizontal
        context.lineWidth = lineWidth;


        context.beginPath();

        context.moveTo(0, offset);
        context.lineTo(canvas.width, offset);
        context.stroke();

      }

      function drawGrid(gridSize, gridThickness, color){
        var numVertical = Math.floor(canvas.width / (gridSize) );
        var numHorizontal = Math.floor(canvas.height / (gridSize));
        context.strokeStyle = color;
        context.lineWidth = gridThickness;
        context.shadowColor = "rgba(0,0,0,0)";
        context.save();

        for (var i = 1; i < numVertical+1; i++){
          drawVerticalLine(i*gridSize-3, gridThickness);
        }

        for (var i = 1; i < numHorizontal+1; i++){
          drawHorizontalLine(i*gridSize-3, gridThickness);
        }

        context.restore();

      }

      function greyRings(){
        // Outer grey ring
        context.strokeStyle = greyGrad;
        context.shadowColor = "rgba(0,255,0,1)";
        context.shadowBlur = 0;
        context.lineWidth = 4;
        context.beginPath();
        context.arc(center.x,center.y,85, 0, 2*Math.PI);
        context.stroke();

        // Inner grey ring
        context.strokeStyle = greyGrad;
        context.lineWidth = 3;
        context.beginPath();
        context.arc(center.x,center.y, 52, 0, 2*Math.PI);
        context.stroke();
      }

      function drawStaticParts(){
        // Outer Cyan - thin
        context.strokeStyle = outerRingColor;
        context.lineWidth = 2;
        context.shadowColor = outerRingGlow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;

        context.beginPath();
        context.arc(center.x,center.y,blueRadius, 0, 2*Math.PI);
        context.stroke();

        // Inner yellow - thin
        context.strokeStyle = colGrey;
        context.lineWidth = 2;
        context.shadowColor = colGrey;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;

        context.beginPath();
        context.arc(center.x,center.y,42,0, 2*Math.PI);
        context.stroke();

        /* Inner yellow - thin
         context.strokeStyle = colLightYellow;
         context.lineWidth = 2;
         context.shadowColor = colYellow;
         context.shadowBlur = 10;
         context.shadowOffsetX = 0;
         context.shadowOffsetY = 0;

         context.beginPath();
         context.arc(center.x,center.y,30, 0, 2*Math.PI);
         context.stroke(); */

      }

      function drawRotatingParts(angle){
        context.save();
        context.moveTo(center.x, center.y);

// Inner yellow - thin
        context.strokeStyle = colYellow;
        context.lineWidth = 4;
        context.shadowColor = colYellow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;

        context.beginPath();
        context.arc(center.x,center.y,42, toRad(30+angle), toRad(300+angle));
        context.stroke();




        // Outer Cyan - thick
        context.strokeStyle = outerRingColor;
        context.lineWidth = 4;
        context.shadowColor = outerRingGlow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;

        context.beginPath();
//context.arc(center.x,center.y,70, toRad(30-50*Math.sin(toRad(angle*5))), toRad(330-50*Math.sin(toRad(angle*5))));
        context.arc(center.x,center.y,blueRadius, toRad(30-angle/4), toRad(330-angle/4));
        context.stroke();

//Inner yellow - thin
        context.strokeStyle = colLightYellow;
        context.lineWidth = 2;
        context.shadowColor = colLightYellow;
        context.shadowBlur = 10;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;

        context.beginPath();
        context.arc(center.x,center.y,32-plusSize, 0, 2*Math.PI);
        context.stroke();


        context.restore();
      }



      var render = function() {
        // Clear the canvas
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Draw tickers
        drawGrid(32, 1, "rgba(75,75,75,0.2)");
        drawGrid(8, 1, "rgba(75,75,75,0.15)");
        drawSet(24,tickersRadius, 3, 3, tickerColor, tickerColor ,60*Math.sin(toRad(tickersAngle*4)));
        drawSet(24,tickersRadius+2+4*Math.sin(toRad(tickersAngle*4)), 10, 1, tickerColor, tickerGlow ,60*Math.sin(toRad(tickersAngle*4)));
//    drawSet(24,56, 6, 2, colYellow, colYellow ,45*Math.sin(toRad(tickersAngle*5)));
//    drawSet(60,56, 4, 1, "rgba(255,255,255,.5)", "rgba(255,255,255,0)" ,tickersAngle);
        drawCrosshair(plusSize);
        greyRings();
        drawStaticParts();
        drawRotatingParts(-movingPartsAngle);


        // Redraw
        requestAnimationFrame(render);
      };


      // Start the redrawing process
      $(document).ready(function(){
        $("#myCanvas").attr('height', $(document).height()-2);
        $("#myCanvas").attr('width', $(document).width()-2);
      })

      var tickersAngle = 0;
      var movingPartsAngle = 0;
      setInterval(function(){ tickersAngle += tickerUpdate; }, 20);
      setInterval(function(){ movingPartsAngle += 3;}, 20);
      render();

    },

    data() {

    },
    watch: {

    },
    methods: {

    },
    components: {

    },
  }

</script>

<style scoped>
  canvas{
    background-color: #1f1f1f;
    cursor: none;
    margin: 0 auto;
  }

  #dummy{
    display: none;
  }
</style>