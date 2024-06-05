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
    <img src="../images/amarula.svg" class="logo-topright"/>
      <slot />
    </div>
    <div class="my-14 mr-14" :style="style" />
  </div>
  <table class="bottompanel">
      <tr>
        <th style="text-align:left; padding-left:8px; font-weight:400">
          <a href="https://www.amarulasolutions.com">https://www.amarulasolutions.com</a>
        </th>
        <th>
          <SlideCurrentNo style="font-weight:400"/>
        </th>
      </tr>
  </table>
</template>
