import { createApp } from 'vue';
import App from './app.vue';
import store from '../store';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'; // 引入整个 Element Plus 样式文件

const app = createApp(App);

app.use(ElementPlus); // 使用 Element Plus
app.use(store);

app.mount('#app');
