<script setup lang="ts">
import { isDark } from '@slidev/client/logic/dark.ts'
</script>

<template>
  <div class="slidev-layout cover">
    <img src="../images/amarula-horizontal-white.png" class="logo" v-if="isDark" />
    <img src="../images/amarula-horizontal.png" class="logo" v-else />
    <div class="my-auto w-full">
      <slot />
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
