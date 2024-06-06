<script setup lang="ts">
import { isDark } from '@slidev/client/logic/dark.ts'

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
    <img src="../images/amarula-white.png" class="logo-topright" v-if="isDark" />
    <img src="../images/amarula.png" class="logo-topright" v-else />
      <slot />
    </div>
    <div class="my-14 mr-14" :style="style" />
  </div>
  <table class="bottompanel">
      <tr>
        <th style="text-align:left; padding-left:8px">
          <a href="https://www.amarulasolutions.com">https://www.amarulasolutions.com</a>
        </th>
        <th>
          <SlideCurrentNo />
        </th>
      </tr>
  </table>
</template>
