<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  setup() {
    return {}
  },
})
</script>

<style>
.aui-page-panel {
  margin-top: 30px;
  margin-bottom: 30px;
  min-height: calc(100vh - 40px - 30px - 30px);
}
</style>
