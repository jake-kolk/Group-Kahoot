<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authProvider } from "../services/ApiCall";
import { useRoute } from 'vue-router'

const username = ref('');
const password = ref('');

const auth = authProvider();
const router = useRouter();
const route = useRoute()

function handleLogin() {
    auth.login({username: username.value, password: password.value})
        .then(response => {
            console.log("Login successful:", response);
            auth.userid = response.user_id;
            if (route.query.redirect) {
                router.push(route.query.redirect as string) // go to the page user wanted (sent as query: <destination>)
        } else {
            router.push('/host') // default page if no redirect
        }
        })
        .catch(error => {
            console.error("Login failed:", error);
            // Handle login failure (e.g., show error message) (usually fails from bad creds)
        });
}

</script>

<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <input v-model="username" placeholder="Email" />
            <input v-model="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
        </form>
        <router-link to="/signup">Don't have an account? Register</router-link>
    </div>
</template>