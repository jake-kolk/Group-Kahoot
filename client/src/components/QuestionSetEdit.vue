<script setup lang="ts">
import { ref } from 'vue';
import { createQuestionSet, fetchQuestionSet, updateQuestionSet, deleteQuestionSet, authKey } from "../services/ApiCall";

const questionSetId = defineProps<{
    id?: number;
}>();

const questionSet = ref({
    id: 0,
    title: '',
    description: '',
    userId: 0,
});

function loadQuestionSet() {
    const token = authKey().token;
    if (questionSetId) {
        fetchQuestionSet(token, Number(questionSetId))
            .then((data) => {
                if (data) {
                    questionSet.value = data;
                }
            })
            .catch((error) => {
                console.error("Error fetching question set:", error);
            });
    }
}

loadQuestionSet();

</script>

<template>
<div>
    <h2>Question Set Edit</h2>
    <form>
        <input v-model="questionSet.title" placeholder="Title" />
        <input v-model="questionSet.description" placeholder="Description" />
        <button type="submit">Save Question Set</button>
    </form>
</div>


</template>