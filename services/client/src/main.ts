import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = true;

Vue.use(VueAxios, axios);

/**
 * Check if the browser already has a token available
 */
const token = localStorage.getItem('token');
if (token) {
  Vue.axios.defaults.headers.common['Authorization'] = token;
}

import Component from 'vue-class-component'

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
