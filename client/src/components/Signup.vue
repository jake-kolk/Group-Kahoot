<script setup lang="ts">
import { ref } from 'vue';
import { authProvider } from "../services/ApiCall";
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');

const auth = authProvider();
const router = useRouter();

function handleSignup() {
    auth.register({username: username.value, email: email.value, password: password.value})
        .then(response => {
            console.log("Signup successful:", response); // <--- .data
            router.push({path: `/question_sets/${auth.userid}` })
        })
        .catch(error => {
            console.error("Signup failed:", error.response?.data || error.message);
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