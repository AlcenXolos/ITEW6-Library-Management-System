<template>
  <div :class="['alert','alert-'+type,'alert-dismissible','fade','show']" role="alert">
    <slot/>
    <button type="button" class="btn-close" @click="$emit('close')"></button>
  </div>
</template>
<script>export default { props:['type'] }</script>
