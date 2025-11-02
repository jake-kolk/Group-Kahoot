<script setup lang="ts">
import { ref } from 'vue';
import MainMenu from './components/MainMenu.vue'
import Lobby from './components/Lobby.vue';
import type { Player } from './game/Player';
import Game from './components/Game.vue';
import { WS } from './services/WebSocket';
import { toast } from 'vue3-toastify';
import Host from "./components/Host.vue";

const currentScreen = ref('mainMenu');
const player = ref();

WS.initialize(`ws://${window.location.host}/ws/`, {
  onclose: () => toast("Disconnected, reconnecting in 6 seconds...", {autoClose: 4000}),
  onopen: () => toast("Connected to WS!", {autoClose: 4000}),
  onmessage: e => console.log(e.data),
});

function handleJoinLobby(plyr: Player) {
  currentScreen.value = 'lobby';
  player.value = plyr;
}

function handleLeaveGame() {
  currentScreen.value = 'mainMenu';
  WS.emit('player_leave', { room: '100000', player: player.value.name });
}

function handleStartQuestion() {
  currentScreen.value = 'question';
}

// TODO: change all these handles to one big handle with a parameter for next destination

</script>

<template>
  <!-- <RouterView /> -->
  <MainMenu v-if="currentScreen === 'mainMenu'" @join-lobby="handleJoinLobby"></MainMenu>
  <Lobby v-if="currentScreen === 'lobby'" :player="player" @leave-game="handleLeaveGame" @start-game="handleStartQuestion"></Lobby>
  <Game v-if="currentScreen === 'question'" @leave-game="handleLeaveGame"></Game>
  <Host v-if="currentScreen === 'host'"></Host>

</template>

<style>
</style>
