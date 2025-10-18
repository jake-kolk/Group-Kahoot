<script setup lang="ts">
import type { Player } from '../game/Player';
const vueEmit = defineEmits(['leave-game', 'start-game']);

const props = defineProps<{player: Player}>();

function leaveLobby() {
    vueEmit('leave-game');
}

function startGame() {
    vueEmit('start-game');
}
</script>

<template>
<h3>LOBBY</h3>
<p>Name: {{ props.player.name }}</p>
<p>ID: {{ props.player.id }}</p>
<button @click="startGame">Start</button>
<button @click="leaveLobby">Leave</button>
</template>

<style>
</style>