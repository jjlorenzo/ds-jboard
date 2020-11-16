<template>
  <select class="select full-width-field" v-model="value">
    <option v-if="nullable" :value="null">Select</option>
    <option v-for="value in options" :key="value" :value="value">{{ value }}</option>
  </select>
</template>

<script lang="ts">
import { computed } from "vue"
import { defineComponent } from "vue"

export default defineComponent({
  props: {
    modelValue: {
      type: String,
      default: null,
    },
    nullable: {
      type: Boolean,
      default: true,
    },
    options: {
      type: Array,
      default: () => [],
    },
  },
  setup(props, { emit }) {
    return {
      value: computed({
        get: () => props.modelValue,
        set: value => emit("update:modelValue", value),
      }),
    }
  },
})
</script>
