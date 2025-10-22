<script setup lang="ts">
import type { Player } from '../game/Player';
import { WS } from '../services/WebSocket';
const vueEmit = defineEmits(['leave-game', 'start-game']);

const props = defineProps<{player: Player}>();

function leaveLobby() {
    vueEmit('leave-game');
}

function startGame() {
    WS.emit('start_game', {room: '100000', name: props.player.name}) // TODO: unhardcode this CODE!
}

WS.on("started", () => {
    vueEmit('start-game');
});
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