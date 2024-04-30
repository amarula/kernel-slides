<template>
  <div class="slidev-layout cover">
    <img src="../images/amarula.svg" class="logo"/>
    <div class="my-auto w-full">
      <slot />
    </div>
  </div>
  <div class="bottompanel">
    <SlideCurrentNo />
  </div>
</template>
