import { createApp } from 'vue'
import App from "./App.vue";
import router from "./routes/index.js";
import './assets/content.css'
import './assets/dashboard.css'
import './assets/sidebar.css'
import './assets/login.css'
import './assets/agent.css'
// import emailjs from "emailjs-com";

const app = createApp(App);

app.use(router)
app.mount("#app")