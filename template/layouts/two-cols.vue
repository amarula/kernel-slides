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
  <div class="slidev-layout two-columns grid grid-cols-2 w-full h-full">
    <img src="../images/amarula-white.png" class="logo-topright" v-if="isDark" />
    <img src="../images/amarula.png" class="logo-topright" v-else />
    <div class="col-left" :class="props.class">
      <slot />
    </div>
    <div class="col-right" :style="props.class">
      <slot name="right" />
    </div>
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
