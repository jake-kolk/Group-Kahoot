<script setup lang="ts">
import { ref } from 'vue';

const question = ref("What is 2 + 2?");

</script>

<template>
    <h3>Game</h3>
    <p>{{ question }}</p>
    <button>4</button><button>5</button><br></br>
    <button>2</button><button>3</button>
</template>

