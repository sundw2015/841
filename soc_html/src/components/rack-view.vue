<template>
  <div class="rack-v-page">
    <div class="rack-v-page-body">
      <div class="rack-v">
        <div class="rack-bg">
          <div class="rack_title"></div>
          <template v-for="device in devices">
            <div v-if="device.device_type == device_type && device.device_id == device_id" class="device lightSpeedIn animated show device-selected" v-bind:class="['device-'+device.u_num+'u']"></div>
            <div v-else="" class="device lightSpeedIn animated show" v-bind:class="['device-'+device.u_num+'u']"></div>
          </template>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
  import rackImg from "src/assets/images/rack/rack.png"
  import ysSelect from 'src/components/select.vue'
  export default {
    props: ['device_type', 'device_id'],
    data() {
      return {
        devices: []
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
      getRackInfo(){
        if(this.device_id && this.device_type){
          this.$http.get("/api/rack_device_view/"+ this.device_type + "/" + this.device_id).then(function (response) {
          if(response.data.status==200){
            this.devices = response.data.data.devices
          }
        })

        }
      }
    }
  }

</script>
<style scoped>

  .rack-v-page .rack-v-page-body {
    margin: 10px;
  }
  .rack-v {
    display: block;
    float: left;
    width: 300px;
    border-radius: 5px;
  }
  .rack-v .rack_title{
    height: 10px;
    width: auto;
  }
  .rack-v-page-body .rack-bg{
    display: block;
    float: left;
    margin-top: 10px;
    margin-left: 10px;
    width: 179px;
    height: 453px;
    background-size: 179px;
    background-image: url("../assets/images/rack/rack.png");
  }

  .rack-v .device {
    width: 145px;
    margin-top: 2px;
    margin-left: 16px;
    background-size: 150px;
  }
  .select-device {

  }
  .rack-v .device:hover{
    border-style: solid;
    border-width: 2px;
    border-color: #00b3ee;
    opacity: 0.5
  }
  .rack-v .device-selected{
    border-style: solid;
    border-width: 2px;
    border-color: #00b3ee;
    opacity: 0.5
  }

  .device-0u{
    margin-top: 2px;
    height: 8px !important;
  }
  .device-1u{
    height: 8px;
    background-image: url("../assets/images/rack/1U.jpg");

  }
  .device-2u{
    height: 18px;
    background-image: url("../assets/images/rack/2U.jpg");
  }
  .device-3u{
    height: 28px;
    background-image: url("../assets/images/rack/3U.jpg");
  }
  .device-4u{
    height: 38px;
    background-image: url("../assets/images/rack/4U.jpg");
  }
  .device-5u{
    height: 48px;
    background-image: url("../assets/images/rack/5U.jpg");
  }
  .device-6u{
    height: 58px;
    background-image: url("../assets/images/rack/6U.jpg");
  }
  .m-l-50 {
    margin-left: 50px !important;
  }


</style>