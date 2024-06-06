<script setup lang="ts">
import { isDark } from '@slidev/client/logic/dark.ts'
</script>

<template>
  <div class="slidev-layout intro">
    <img src="../images/amarula-white.png" class="logo-topright" v-if="isDark" />
    <img src="../images/amarula.png" class="logo-topright" v-else />
    <div class="my-auto">
      <slot />
    </div>
  </div>
</template>
