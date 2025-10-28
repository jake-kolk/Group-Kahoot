<script setup lang="ts">
import { ref } from 'vue';
import { registerUser } from "../services/ApiCall";

const username = ref('');
const email = ref('');
const password = ref('');

function handleSignup() {
    registerUser({username: username.value, email: email.value, password: password.value})
        .then(response => {
            console.log("Signup successful:", response);
            // Handle successful signup (e.g., redirect to login page)
        })
        .catch(error => {
            console.error("Signup failed:", error);
            // Handle signup failure (e.g., show error message)
        });
}

</script>

<template>
    <div>
        <h2>Signup</h2>
        <form @submit.prevent="handleSignup">
            <input v-model="username" placeholder="Username" />
            <input v-model="email" type="email" placeholder="Email" />
            <input v-model="password" type="password" placeholder="Password" />
            <button type="submit">Signup</button>
        </form>
    </div>
</template>