<script setup lang="ts">
import { isDark } from '@slidev/client/logic/dark.ts'
</script>

<template>
  <div class="slidev-layout h-full grid place-content-center last-slide">
    <img src="../images/amarula-horizontal-white.png" class="logo" v-if="isDark" />
    <img src="../images/amarula-horizontal.png" class="logo" v-else />
  </div>
  <table class="bottompanel">
    <tr>
      <th style="text-align:center; padding-left:8px">
        <a href="https://www.amarulasolutions.com">https://www.amarulasolutions.com</a>
      </th>
    </tr>
  </table>
</template>
