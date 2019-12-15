import 'bootstrap';
import 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import Recap from '../components/Recap.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/recap',
      name: 'Recap',
      component: Recap,
    },
    {
      path: '',
      name: 'Main',
      component: Recap,
    },
  ],
});
