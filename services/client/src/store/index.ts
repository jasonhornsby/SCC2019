import Vue from 'vue';
import Vuex from 'vuex';
import Auth from '@/store/auth.store';
import Title from '@/store/title.store';
import User from '@/store/user.store';
import Notification from '@/store/notification.store';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    Auth, Title, User, Notification
  }
})
