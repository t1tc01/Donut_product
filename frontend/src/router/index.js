import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ButtonView from '../components/ButtonView'
import InferenceView from '../components/InferenceView'
import UploadFileTest from '../components/UploadFileTest'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/test-button-view',
    name: 'test-button-view',
    component: ButtonView
  },
  {
    path: '/test-upload',
    name: 'test-upload',
    component: UploadFileTest
  },
  {
    path:'/inference',
    name: 'inference',
    component: InferenceView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
