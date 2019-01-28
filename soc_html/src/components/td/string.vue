<template>
  <div>
    <template v-if="row.edit == true && thead.edit == true">
      <div class="edit-input">
        <p></p>
        <input v-model="data"/>
      </div>
    </template>
    <template v-else>
      <span >{{ data }}</span>
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
    },
  }
</script>
