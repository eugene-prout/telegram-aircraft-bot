import { createApp } from 'vue'
import App from './App.vue'

import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Telegram from './pages/Telegram.vue'
import About from './pages/About.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/telegram', component: Telegram },
  { path: '/about', component: About },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})



const loadApp = () => {
  createApp(App)
    .use(router)
    .mount('#app')
}

loadApp()