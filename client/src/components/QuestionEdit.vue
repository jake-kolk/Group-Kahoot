<script setup lang="ts">
import { ref } from 'vue';
import { createQuestion, fetchQuestion, updateQuestion, deleteQuestion, authKey } from "../services/ApiCall";


const questionId = defineProps<{
    questionId?: number;
}>();

const question = ref({
    id: 0,
    text: '',
    choices: [] as string[],
    correctAnswerIndex: 0,
    questionSetId: 0,
});

function loadQuestion() {
    const token = authKey().token;
    if (questionId) {
        fetchQuestion(token, Number(questionId))
            .then((data) => {
                if (data) {
                    question.value = data;
                }
            })
            .catch((error) => {
                console.error("Error fetching question:", error);
            });
    }
}

loadQuestion();

</script>

<template>
    <div>
        <h2>Question Edit</h2>
        <form>
            <input v-model="question.text" placeholder="Question Text" />
            <div v-for="(choice, index) in question.choices" :key="index">
                <input v-model="question.choices[index]" :placeholder="`Choice ${index + 1}`" />
            </div>
            <input v-model.number="question.correctAnswerIndex" type="number" placeholder="Correct Answer Index" />
            <button type="submit">Save Question</button>
        </form>
    </div>
</template>