import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  },
  {
    path: '/loginandregister',
    name: 'LoginAndRegister',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginAndRegister.vue')
  },
  {
    path: '/:uid/PersonalInfomation',
    name: 'PersonalInfomation',
    component: () => import(/* webpackChunkName: "about" */ '../views/PersonalInfomation.vue')
  },
  {
    path: '/:uid/Chatroom',
    name: 'Chatroom',
    component: () => import(/* webpackChunkName: "about" */ '../views/Chatroom.vue')
  },
  {
    path: '/:uid/GroupPage/:groupid',
    name: 'GroupPage',
    component: () => import(/* webpackChunkName: "about" */ '../views/GroupPage.vue')
  },
  {
    path: '/:uid/:groupid/MyProject/:projectid',
    name: 'MyProject',
    component: () => import(/* webpackChunkName: "about" */ '../views/MyProject.vue')
  },
  {
    path: '/:groupid/:projectid/:designid/DesignPage',
    name: 'DesignPage',
    component: () => import(/* webpackChunkName: "about" */ '../views/DesignPage.vue')
  },
  {
    path: '/:groupid/:projectid/:documentid/DocumentPage',
    name: 'DocumentPage',
    component: () => import(/* webpackChunkName: "about" */ '../views/DocumentPage.vue')
  },
  {
    path: '/try',
    name: 'try',
    component: () => import(/* webpackChunkName: "about" */ '../views/try')
  },
  {
    path: '/:projectid/DesignShare',
    name: 'DesignShare',
    component: () => import(/* webpackChunkName: "about" */ '../views/Share')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
