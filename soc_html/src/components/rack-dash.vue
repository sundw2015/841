<template>
  <div class="rack-dash" style="height:800px;">
    <table>
      <tr>
        <td class="dash-left"><div class="dash-left" id="rackLeft"></div></td>
        <td>
          <div class="dash-mid" id="rackMid">
            <div class="dash-con-top">
              <p class="line1"></p>
              <p class="line2"></p>
              <p class="line3"></p>
            </div>
            <div class="dash-con-box">
              <template v-for="device in devices">
                <div v-if="device.device_type == device_type && device.device_id == device_id"
                     class="device show device-selected"
                     v-bind:class="['device-'+device.u_num+'u']"
                     @click="clickDevices($index, device)"
                     @mouseover="mouseOver(device)">
                </div>
                <div v-else
                     class="device show"
                     v-bind:class="['device-'+device.u_num+'u']"
                     @click="clickDevices($index, device)"
                     @mouseover="mouseOver(device)">

                </div>
              </template>
            </div>
            <div class="dash-con-bottom">
              <p style="height:2px;"></p>
              <p class="line1"></p>
              <p style="height:12px;"></p>
              <p class="line2"></p>
              <div class="dash-foot dash-foot-left"></div>
              <div class="dash-foot dash-foot-right"></div>
            </div>
          </div>
        </td>
        <td class="dash-right"></td>
      </tr>
    </table>
    <div class="num-con">
      <div style="height:10px;"></div>
      <div class="rack-num">
        <p v-for="list in devices" class="num-list">
          <span @click="clickDevices($index, list)"
                v-bind:class="[checkNumber(devLength-$index) ? 'ys-white-color' : 'ys-info-color']">{{devLength - $index}}</span>
        </p>
      </div>
      <div style="height:20px;"></div>
    </div>
  </div>
</template>
<style scoped>
  .rack-dash{
    display: inline-block;
    position:relative;
  }
  .num-con{
    position:absolute;
    right:-20px;
    top:0px;
  }
  .rack-num{
    padding:10px 0px 6px 0px;
  }
  .rack-num p{
    line-height:10px;
    height:10px;
    margin-bottom:2px;
  }
  .rack-num p span{
    display:inline-block;
    font-size:10px;
    font-weight:100;
    font-family: Arial;
    -webkit-transform:scale(0.8);
  }
  .dash-left{
    width:10px;
    height:100%;
    border-left:1px solid rgba(129,159,208,0.28);
    background:linear-gradient(to right, #273856,#1f263d);
  }
  .dash-mid{
    width:156px;
    background:#52698e;
  }
  .dash-right{
    width:10px;
    border-left:1px solid #182239;
    background:linear-gradient(to right, #273856,#1f263d);
  }
  .dash-con-top{
    height:12px;
    background:linear-gradient(to right, #273a57,#1e253c);
  }
  .dash-con-top .line1{
    width:100%;
    height:2px;
    background:rgba(129,159,208,0.28);
  }
  .dash-con-top .line2{
    width:100%;
    height:6px;
  }
  .dash-con-top .line3{
    width:100%;
    height:4px;
    background:rgba(33,44,72,0.5);
  }
  .dash-con-bottom{
    height:20px;
    background:linear-gradient(to right, #273a57,#1e253c);
    position:relative;
  }
  .dash-con-bottom .line1{
    width:100%;
    height:4px;
    background:rgba(129,159,208,0.23);
  }
  .dash-con-bottom .line2{
    width:100%;
    height:2px;
    background:rgba(33,44,72,0.3);
  }
  .dash-foot{
    position:absolute;
    top:20px;
    width:23px;
    height:7px;
    background:linear-gradient(to right, #273856,#1f263d);
    border-left:1px solid rgba(129,159,208,0.28);
    border-right:1px solid #182239;
  }
  .dash-foot-left{
    left:10px;
  }
  .dash-foot-right{
    right:10px;
  }
  .dash-con-box{
    padding:8px 8px 6px 8px;
  }

  .device{
    margin-bottom: 2px;
  }
  .device:hover{
    border:1px solid #00bc85;
  }
  .device-selected{
    border:1px solid #00bc85;
  }
  .device-0u{
    height: 10px;
    background: #435b81;
  }
  .device-1u{
    height: 10px;
    background-image: url("../assets/images/rack/1U.jpg");
    background-size:100% 100%;

  }
  .device-2u{
    height: 22px;
    background-image: url("../assets/images/rack/2U.jpg");
    background-size:100% 100%;
  }
  .device-3u{
    height: 34px;
    background-image: url("../assets/images/rack/3U.jpg");
    background-size:100% 100%;
  }
  .device-4u{
    height: 46px;
    background-image: url("../assets/images/rack/4U.jpg");
    background-size:100% 100%;
  }
  .device-5u{
    height: 58px;
    background-image: url("../assets/images/rack/5U.jpg");
    background-size:100% 100%;
  }
  .device-6u{
    height: 70px;
    background-image: url("../assets/images/rack/6U.jpg");
    background-size:100% 100%;
  }
</style>
<script>
  import rackImg from "src/assets/images/rack/rack.png"
  export default {
    props: {
      devices: {
        twoWay: true,
        type: Array,
        default () {
          return []
          }
        },
      device_id: {
        default: 0
      },
      device_type: {
        default: 0
      },
      readOnly: {
        default: true
      }
    },
    data() {
      return {
        nums:[],
      }
    },
    computed: {
      devLength: function () {
        return this.devices.length
      }
    },
    ready: function () {
      this.getRackInfo()
    },
    watch: {
      'device_id': function (val, oldval) {
        this.getRackInfo()
      }
    },
    methods: {
      clickDevices(index, device){
        let data = {
          index: index,
          device: device
        }
        this.$dispatch('click-device', data)
      },
      getRackInfo(){
        if(!this.readOnly){
          return true
        }
        if(this.device_id==false){return false}
        if(this.device_id && this.device_type){
          this.$http.get("/api/rack_device_view/"+ this.device_type + "/" + this.device_id).then(function (response) {
            if(response.data.status==200){
              this.devices = response.data.data.devices;
              this.devLength=this.devices.length;
            }
          })
        }
      },
      mouseOver(device){
        this.nums=[];
        for(var a=device.u_location;a<device.u_num+device.u_location;a++){
          this.nums.push(a);
        }
      },
      checkNumber(num){
        if(collect(this.nums).contains(num)){
          return true
        }else{
          return false
        }

      }
    }
  }

</script>