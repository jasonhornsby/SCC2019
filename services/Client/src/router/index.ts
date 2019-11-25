import Vue from 'vue';
import VueRouter from 'vue-router'
import HomeView from '@/views/home.view.vue';
import LoginView from '@/views/login.view.vue';
import RegisterView from '@/views/register.view.vue';
import FileView from '@/views/file.view.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/file/:id',
    name: 'file',
    component: FileView,
    props: true,
    meta: {
      requiresAuth: false
    }
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  // make sure you can only access the login and register screen when you arent logged in
  if (to.name === 'login' || to.name === 'register') {
    const loggedIn = localStorage.getItem('user');
    if (loggedIn) {
      next('');
      return;
    }
  }

  // Check if the current route need Authentication
  if ( to.matched.some(record => record.meta.requiresAuth) ) {
    const loggedIn = localStorage.getItem('user');
    if (!loggedIn) {
      next('/login');
      return;
    }
  }

  // else proceed as normal
  next();
});

export default router;
