import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import QuestionSetList from './components/QuestionSetList.vue'
import QuestionSetEdit from './components/QuestionSetEdit.vue'
import QuestionList from './components/QuestionList.vue'
import QuestionEdit from './components/QuestionEdit.vue'
import GamePage from './components/GamePage.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: GamePage},
        {path: '/login', component: Login},
        {path: '/signup', component: Signup},
        {path: '/question_sets/:UserId', component: QuestionSetList, props: true},
        {path: '/question_sets/:UserId/edit/:id', component: QuestionSetEdit, props: true},
        {path: '/questions/:userId/:questionSetId', component: QuestionList, props: true},
        {path: '/questions/:UserId/edit/:id', component: QuestionEdit, props: true},
    ],
})


const app = createApp(App);
app.use(router);
app.use(createPinia());
app.mount('#app');
