import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import '@/assets/custom.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

axios.defaults.baseURL = 'http://localhost:8000';  
// (so all axios calls like axios.post('/api/books/add/') go to port 8000)

const app = createApp(App);
app.use(router);
app.use(store);
app.mount('#app');
