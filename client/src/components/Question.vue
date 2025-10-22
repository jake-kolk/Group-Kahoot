<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import type { Question } from '../game/Question';
import { WS } from '../services/WebSocket';

const props = defineProps<{question: Question}>();
const vueEmit = defineEmits(['answered-question']);

function pickedChoice(choice: number) {
    WS.emit('answer', {
        room: '100000', // TODO: change to non hardcoded
        question_id: props.question.id,
        choice,
        time_left_ms: props.question.duration // TODO: make this actually work
    });
}

WS.on('answer_ack', () => {
    vueEmit('answered-question');
});

onUnmounted(() => {
    WS.removeListener('answer_ack');
});

</script>

<template>
    <h3>Game</h3>
    <p>{{ props.question.text }}</p>
    <button @click="pickedChoice(0)">{{ question.choices[0] }}</button>
    <button @click="pickedChoice(1)">{{ question.choices[1] }}</button><br></br>
    <button @click="pickedChoice(2)">{{ question.choices[2] }}</button>
    <button @click="pickedChoice(3)">{{question.choices[3]}}</button>
</template>

