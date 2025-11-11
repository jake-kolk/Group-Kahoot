<script setup lang="ts">
import { ref } from 'vue';
import { fetchAllQuestions, fetchQuestionSet, authProvider } from "../services/ApiCall";
import type { Question } from "../types/types";

const { questionSetId } = defineProps<{ questionSetId: string }>();

const questionSetTitle = ref('');
const questions = ref<Question[]>([]);

function fetchQuestionSetTitle() {
    const token = authProvider().access_token;
    fetchQuestionSet(token, Number(questionSetId))
        .then((data) => {
            if (data) {
                questionSetTitle.value = data.title;
            }
        })
        .catch((error) => {
            console.error("Error fetching question sets:", error);
        });
}

function loadQuestions() {
    const token = authProvider().access_token;
    fetchAllQuestions(token, Number(questionSetId))
        .then((data) => {
            questions.value = data;
        })
        .catch((error) => {
            console.error("Error fetching questions:", error);
        });
}

fetchQuestionSetTitle();
loadQuestions();


</script>

<template>
    <div>
        <h2>Questions for Set: {{ questionSetTitle }}</h2>
        <ul>
            <li v-for="ques in questions" :key="ques.id">
                {{ ques.text }}
            </li>
        </ul>
    </div>
</template>