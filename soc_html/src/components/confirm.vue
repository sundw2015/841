<template>
  <div id="del-confirm" class="modal fade">
    <div class="modal-dialog confirm-dialog">
      <div class="modal-content">
        <div class="modal-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    props: {
      status: {
        default: false
      }
    },
    data() {
      return {
      }

    },
    ready: function () {
      var self = this
      $('#del-confirm').bind('hidden.bs.modal', function () {
        self.status = false
      });
    },
    watch:{
      'status':function(){
        if(this.status){
          $("#del-confirm").modal()
        }else{
          $("#del-confirm").modal("hide")
        }
      }
    }
  }
</script>
<style>

</style>