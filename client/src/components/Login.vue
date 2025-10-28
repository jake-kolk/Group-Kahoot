<script setup lang="ts">
import { ref } from 'vue';
import { loginUser } from "../services/ApiCall";

const username = ref('');
const password = ref('');

function handleLogin() {
    loginUser(username.value, password.value)
        .then(response => {
            console.log("Login successful:", response);
            // Handle successful login (e.g., redirect to another page)
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
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button @click="handleLogin">Login</button>
    </div>
</template>