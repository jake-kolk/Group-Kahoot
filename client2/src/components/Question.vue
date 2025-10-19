<script setup lang="ts">
import { ref } from 'vue';
import type { Question } from '../game/Question';

const props = defineProps<{question: Question}>();

</script>

<template>
    <h3>Game</h3>
    <p>{{ props.question.text }}</p>
    <button>4</button><button>5</button><br></br>
    <button>2</button><button>3</button>
</template>

