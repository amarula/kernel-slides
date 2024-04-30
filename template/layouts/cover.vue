<template>
  <div class="slidev-layout cover">
    <img src="../images/amarula.svg" class="logo"/>
    <div class="my-auto w-full">
      <slot />
    </div>
  </div>
  <table class="bottompanel">
      <tr>
        <th style="text-align:left; padding-left:8px;">
          <a href="https://www.amarulasolutions.com">www.amarulasolutions.com</a>
        </th>
        <th>
          <SlideCurrentNo class="" />
        </th>
      </tr>
  </table>
</template>
