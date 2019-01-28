<template>
  <div>
    <p>
      <i class="ys-icon icon-lock-shield font22 ys-success-color verticalM m-r-5"></i>
      <span class="verticalM">操作保护</span>
    </p>
    <div class="admin-pwd-box">
      <span class="verticalM ys-info-color">管理员密码 : </span>
      <input class="ys-input" type="password"
             placeholder="管理员密码"
             v-model="adminPassword"/>
    </div>
  </div>
</template>
<style>
  .admin-pwd-box{
    display: inline-block;
    padding:16px;
    border:1px solid rgba(0, 189, 133, 0.3);
    border-radius: 3px;
    background:rgba(0, 189, 133, 0.05);
    margin-top:6px;
  }
</style>
<script>
  import icon from 'src/components/icon.vue'
  export default {
    name: 'admin-password',
    props: {
      adminPassword: {
        type: String,
      }
    },
    data () {
      return {}
    },
    ready: function () {
    },
    methods: {},
    components: {
      "icon": icon
    }
  }
</script>