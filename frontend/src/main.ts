import "bootstrap/dist/css/bootstrap.css"
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useProfileStore } from "./stores/auth"

const app = createApp(App)
const pinia = createPinia();
app.use(pinia);

const profileStorage = useProfileStore(pinia);
await profileStorage.loadUser();

app.use(router)

app.mount('#app')
