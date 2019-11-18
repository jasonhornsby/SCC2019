<template>
  <div class="app-wrapper">
    <notification></notification>
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
  import Notification from '@/components/notification.component';

  @Component({
    components: {Navbar, Notification}
  })
  export default class App extends Vue {
  }
</script>
