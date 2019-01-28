<template>
</template>

<script>
  export default {
    props: {
      row: Object,
      column: Object,
      index: Number,
    },
    data () {
      return {
        content: this.$parent.content
      }
    },
    ready () {
      this.compile()
    },
    beforeDestroy () {
        this.destroy()
    },
    watch: {
      naturalIndex () {
        this.destroy()
        this.compile()
      }
    },

    methods: {
      compile () {
        const $parent = this.content
        const template = this.column.render(this.row, this.column, this.index)
        const cell = document.createElement('div')
        cell.innerHTML = template
        const _oldParentChildLen = $parent.$children.length
        $parent.$compile(cell)
        const _newParentChildLen = $parent.$children.length
        if (_oldParentChildLen !== _newParentChildLen) {    // if render normal html node, do not tag
            this.uid = $parent.$children[$parent.$children.length - 1]._uid    // tag it, and delete when data or columns update
        }
        this.$el.innerHTML = ''
        this.$el.appendChild(cell)
      },
      destroy () {
        const $parent = this.content
        for (let i = 0; i < $parent.$children.length; i++) {
          if ($parent.$children[i]._uid === this.uid) {
              $parent.$children[i].$destroy()
          }
        }
      },
    },
    components: {}

  }
</script>