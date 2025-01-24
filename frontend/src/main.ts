import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from './router'
import { initializeApp } from "firebase/app"


const firebaseConfig = {
	apiKey: "AIzaSyBwU6RM8ukLVBjiDL8JagRzxUTfAbn-Jwc",
	authDomain: "balance-scale-app.firebaseapp.com",
	projectId: "balance-scale-app",
	storageBucket: "balance-scale-app.firebasestorage.app",
	messagingSenderId: "969848040896",
	appId: "1:969848040896:web:5e1416fc0da62e0813ec25",
	measurementId: "G-F31PJ9HHC1"
}

initializeApp(firebaseConfig);

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
