import { createRouter, createWebHistory } from 'vue-router';
import { isAuthenticated, checkIsAuthenticated } from '@/utils/authUtils';
import LoginView from '@/views/LoginView.vue';
import DashboardView from '@/views/DashboardView.vue';
import RegisterView from '@/views/RegisterView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      beforeEnter: (_to, _from, next) => {
        checkIsAuthenticated();
        if (isAuthenticated.value) {
          next({ name: 'dashboard'});
        } else {
          next();
        }
      },
      name: 'home',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      beforeEnter: (_to, _from, next) => {
        checkIsAuthenticated();
        if (isAuthenticated.value) {
          next();
        } else {
          next({ name: 'home'});
        }
      }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    }
  ]
});

export default router;
