<template>
  <div class="slidev-layout cover">
    <img src="../images/amarula-horizontal.png" class="logo"/>
    <div class="my-auto w-full">
      <slot />
    </div>
  </div>
  <table class="bottompanel">
      <tr>
        <th style="text-align:left; padding-left:8px; font-weight:400">
          <a href="https://www.amarulasolutions.com">https://www.amarulasolutions.com</a>
        </th>
        <th>
          <SlideCurrentNo class="" style="font-weight:400"/>
        </th>
      </tr>
  </table>
</template>
