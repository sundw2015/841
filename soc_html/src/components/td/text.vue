<template>
  <div>
    <template v-if="row.edit == true && thead.edit == true">
      <template v-if="thead.input == 'ys-select'">
        <ys-select :selected.sync="data" :select-url="thead.selectUrl"></ys-select>
      </template>
      <div v-else class="edit-input">
        <p></p>
        <input v-model="data"/>
      </div>
    </template>
    <template v-else>
      <span v-if="typeof data == 'string'">{{ data }}</span>
      <span v-if="typeof data == 'object'">{{ data.name }}</span>
      <span v-if="thead.typeof === 'Array'" v-for="i in data" track-by="$index">{{ i.name }}</span>
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