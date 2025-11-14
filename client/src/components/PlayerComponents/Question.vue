<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import { reactive } from 'vue'
import type { Question } from '@/game/Question';
import { WS } from '@/services/WebSocket';


const vueEmit = defineEmits(['answered-question', 'answerQuestion']);

function pickedChoice(choice: number) {
    vueEmit('answerQuestion', question.question_id, choice, question.duration_ms)
}

WS.on('answer_ack', () => {
    vueEmit('answered-question');
});

interface Question {
  text: string;
  choices: string[];
  type: "question";
  question_id: number;
  duration_ms: number;
}

const question = reactive<Question>({
  text: "",
  choices: [],
  type: "question",
  question_id: 0,
  duration_ms: 0
});

WS.on('question', (data: string | Record<string, any>) => {
    const incoming: Question = typeof data === 'string' ? JSON.parse(data) : data;

    // Update reactive object
    question.text = incoming.text;
    question.choices = incoming.choices;
    question.question_id = incoming.question_id;
    question.duration_ms = incoming.duration_ms;
    question.type = incoming.type;
});


</script>

<template>
    <h3>Game</h3>
    <p>{{ question.text }}</p>
    <button @click="pickedChoice(0)">{{ question.choices[0] }}</button>
    <button @click="pickedChoice(1)">{{ question.choices[1] }}</button><br></br>
    <button @click="pickedChoice(2)">{{ question.choices[2] }}</button>
    <button @click="pickedChoice(3)">{{question.choices[3]}}</button>
</template>

