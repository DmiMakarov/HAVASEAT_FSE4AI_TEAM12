<template>
  <div id="app">
    <ImageUpload />
  </div>
</template>

<script>
import ImageUpload from './components/ImageUpload.vue'

export default {
  name: 'App',
  components: {
    ImageUpload
  }
}
</script>

<style>
#app {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
</style>

