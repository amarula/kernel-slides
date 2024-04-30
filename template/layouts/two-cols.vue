<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  image: {
    type: String,
  },
  class: {
    type: String,
  },
})

</script>
<template>
  <div class="grid grid-cols-2 w-full h-full">
    <div class="slidev-layout default image-right" :class="props.class">
      <slot />
    </div>
    <div class="my-14 mr-14" :style="style" />
  </div>
  <div class="bottompanel">
    <SlideCurrentNo />
  </div>
</template>
