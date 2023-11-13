import { createApp } from 'vue'
import App from "./App.vue";
import VueApexCharts from 'vue3-apexcharts'

import router from "./routes/index.js";
import './assets/content.css'
import './assets/dashboard.css'
import './assets/sidebar.css'
import './assets/login.css'
import './assets/agent.css'

const app = createApp(App);

app.use(router)
app.use(VueApexCharts)
app.mount("#app")