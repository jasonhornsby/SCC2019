<template>
  <div class="app-wrapper">
    <div class="app">
      <navbar></navbar>
      <router-view/>
    </div>
  </div>
</template>
<style src="./styles.scss" lang="scss"></style>
<script lang="ts">
  import Vue from "vue";
  import Component from 'vue-class-component';
  import Navbar from '@/components/navbar.component.vue';
  @Component({
    components: {Navbar}
  })
  export default class App extends Vue {
  }
</script>
