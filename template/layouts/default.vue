<template>
  <div class="slidev-layout default">
    <img src="../images/amarula.svg" class="logo-topright"/>
    <div class="my-auto">
      <slot />
    </div>
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
