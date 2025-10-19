<script setup lang="ts">
import { ref } from 'vue';
import QuestionComponent from './Question.vue';
import { WS } from '../services/WebSocket';
import { Question, type QuestionParams } from '../game/Question';

const hasQuestion = ref(false);
const question = ref();

WS.on('question', data => {
    question.value = new Question(data as QuestionParams);
    hasQuestion.value = true;
});

WS.on('question_ended', data => {
    hasQuestion.value = false;
});

</script>

<template>
    <h3>Game</h3>
    <div v-if="!hasQuestion">
        <p>Waiting for question...</p>
    </div>
    <div v-else>
        <QuestionComponent :question="question"></QuestionComponent>
    </div>
</template>

