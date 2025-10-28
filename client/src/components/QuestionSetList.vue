<script setup lang="ts">
import { ref } from 'vue';
import { fetchAllQuestionSets, authKey } from "../services/ApiCall";
import type { QuestionSet } from "../types/types";

const questionSets = ref<QuestionSet[]>([]);

function loadQuestionSets() {
    const token = authKey().token;
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
            <li v-for="set in questionSets" :key="set.id">
                {{ set.title }}
            </li>
        </ul>
    </div>

</template>