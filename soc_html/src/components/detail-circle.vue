<template>
  <div class="detail-dial">
    <input type="text" class="detail-circle" v-model="value" v-bind:style="{'border-color': color}" readonly>
    <p class="font12 p-t-10" v-bind:style="{'color': color}">{{title}}</p>
    <slot></slot>
  </div>
</template>

<script>
  export default {
    props: {
      value: {
        default: 0,
      },
      color:{
        type: String,
        default: "black"
      },
      title: {
        type: String,
        default: ""
      }
    }
  }
</script>

<style>
.detail-dial{
  height:150px;
  width:100px;
  text-align: center;
}
.detail-circle{
  width: 100px!important;
  height: 100px!important;
  border-radius: 50%!important;
  margin-top: 14px!important;
  font-size: 28px;
  background: none;
  border: 8px solid;
  text-align: center;
}
</style>
