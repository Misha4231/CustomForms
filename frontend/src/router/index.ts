import { createRouter, createWebHistory, type NavigationGuardNext, type RouteLocationNormalized } from 'vue-router'
import {nextTick} from 'vue'

import HomeView from '@/views/HomeView.vue'
import SignInView from '@/views/auth/SignInView.vue'
import SignUpView from '@/views/auth/SignUpView.vue'
import LogoutView from '@/views/auth/LogoutView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import { useProfileStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView,
    },
    {
      path: '/profile',
      component: ProfileView,
      meta: {
        title: "Profile",
        requiresAuth: true,
      }
    },
    {
      path: '/sign-in',
      component: SignInView,
      meta: {
        title: "Sign In"
      }
    },
    {
      path: '/sign-up',
      component: SignUpView,
      meta: {
        title: "Sign Up"
      }
    },
    {
      path: '/logout',
      component: LogoutView,
      meta: {
        title: "Logout",
        requiresAuth: true,
      }
    },
  ],
})


const DEFAULT_TITLE: string = "Custom Forms"
router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const profileStorage = useProfileStore();

  if (profileStorage.id === null && to.meta.requiresAuth) { // in case page requires user session and no session is found
    next('/sign-in');
  } else {
    next();
  }
});

// setup pages titling
router.afterEach((to: RouteLocationNormalized, from: RouteLocationNormalized) => {
  nextTick(() => {
    document.title = to.meta.title || DEFAULT_TITLE;
  });
});

export default router
