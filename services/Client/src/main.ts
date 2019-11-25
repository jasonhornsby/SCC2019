import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = true;

const token = localStorage.getItem('token');
if (token) {
  userService.setAuthHeader(token);
}

Vue.use(VueAxios, axios);

import Component from 'vue-class-component'
import { userService } from '@/services/user.service';

// Register the router hooks with their names
Component.registerHooks([
  'beforeRouteEnter',
  'beforeRouteLeave',
]);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app');
