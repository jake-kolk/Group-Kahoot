<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { fetchAllQuestionSets, authProvider, checkAuth } from "../services/ApiCall";
import type { QuestionSet } from "../types/types";

defineProps({
    UserId: Number
})

const questionSets = ref<QuestionSet[]>([]);
const auth = authProvider();
const router = useRouter();

function loadQuestionSets() {
    const token = auth.access_token;
    if (!checkAuth()) {
        console.log("Not logged in");
        router.push({ path: '/login' });
        return;
    }
    fetchAllQuestionSets(token)
        .then((data) => {
            questionSets.value = data;
        })
        .catch((error) => {
            console.error("Error fetching question sets:", error);
        });
}

loadQuestionSets();

</script>

<template>
    <div>
        <h2>Question Sets</h2>
        <ul>
            <span v-for="set in questionSets" :key="set.id" 
            @click="router.push({ path: `/question_sets/${auth.userid}/edit/${set.id}` })">
                {{ set.title }}
            </span>
        </ul>
    </div>

</template>