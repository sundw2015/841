<template>
  <div>
    <template v-if="row.edit == true && thead.edit == true">
      <ys-select :selected.sync="data" :select-url="thead.selectUrl" :multiple="false"></ys-select>
    </template>
    <template v-else>
      <span >{{ data.name }}</span>
    </template>

  </div>
</template>

<script>
 import ysSelect from '../../components/select.vue'
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
    components: {
      ysSelect
    }
  }
</script>