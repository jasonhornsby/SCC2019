import Vue from 'vue';
import Vuex from 'vuex';
import Auth from '@/store/auth.store';
import Title from '@/store/title.store';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    Auth, Title
  }
})
