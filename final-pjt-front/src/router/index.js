import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticleView from '@/views/ArticleView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path:'/article',
    name : 'ArticleView',
    component : ArticleView
  },
  {
    path : '/signup',
    name : 'SignUpView',
    component : SignUpView
  },
  {
    path : '/article/:articleId',
    name : 'ArticleDetailView',
    component : ArticleDetailView
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
