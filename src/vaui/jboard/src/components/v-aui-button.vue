<template>
  <button class="aui-button" type="button" :busy="busy">
    <slot></slot>
    <aui-spinner resolved="" size="small" v-if="busy">
      <div class="aui-spinner spinner">
        <svg focusable="false" height="20" width="20" viewBox="0 0 20 20">
          <circle cx="10" cy="10" r="9" />
        </svg>
      </div>
    </aui-spinner>
  </button>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  props: {
    busy: {
      type: Boolean,
      default: null,
    },
  },
  setup() {},
})
</script>
