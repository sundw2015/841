<template>
  <div>
    <template v-if="row.edit == true">
        <ys-select :selected.sync="data" :select-url="thead.selectUrl" :multiple="true"></ys-select>
    </template>
    <template v-else>
      <span v-for="i in data" track-by="$index">{{ i.name }}</span>
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