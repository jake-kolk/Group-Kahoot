<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { authProvider } from "../services/ApiCall";

const username = ref('');
const password = ref('');

const auth = authProvider();
const router = useRouter();

function handleLogin() {
    auth.login({username: username.value, password: password.value})
        .then(response => {
            console.log("Login successful:", response);
            // Handle successful login (e.g., redirect to another page)
            router.push({path: `/question_sets/${auth.userid}` })
        })
        .catch(error => {
            console.error("Login failed:", error);
            // Handle login failure (e.g., show error message)

        });
}

</script>

<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <input v-model="username" placeholder="Username" />
            <input v-model="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
        </form>
        <router-link to="/signup">Don't have an account? Register</router-link>
    </div>
</template>