import components from '@/components'
import { compile } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/todos',
    name: 'todos',
    component: () => import('../views/TodoView.vue')
  },
  {
    name: 'register',
    path: '/register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    name:'404',
    path: '/:pathMatch(.*)*',
    component: () => import('../views/404NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
