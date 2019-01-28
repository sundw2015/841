<template>
  <div>
    <template v-if="row.edit == true">
      <div class="edit-input-s">
        <div style="width:30px;">
          <p></p>
          <input v-model="row.cols" />
        </div>
        <div>排 X </div>
        <div style="width:30px;">
          <p></p>
          <input v-model="row.rows"/>
        </div>
        <div>列</div>
      </div>
    </template>

    <template v-else>
      <span >{{ row.cols}}X{{row.rows }}</span>
    </template>


  </div>
</template>

<script>
  export default {
    props: {
      data: {
        default: ""
      },
      row: {
        default: []
      },
      thead:{
        default: {}
      }
    }
  }
</script>