<script setup lang="ts">
import { ref } from 'vue';
import MainMenu from './MainMenu.vue'
import Lobby from './Lobby.vue';
import type { Player } from '@/game/Player';
import { WS } from '@/services/WebSocket';
import { toast } from 'vue3-toastify';
/*
This is where EVERYTHING player related is ran from, it has multiple screens for main menu, lobby, and question. 


*/

const currentScreen = ref('mainMenu');
const player = ref();

 // This can use wither HTTP or HTTPS dependign on protocal
/*
// I'm testing a new one so its commented
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
WS.initialize(`${protocol}://${window.location.host}/ws/`, {
  onclose: () => toast("Disconnected, reconnecting in 6 seconds...", { autoClose: 4000 }),
  onopen: () => toast("Connected to WS!", { autoClose: 4000 }),
  onmessage: e => console.log(e.data),
});
*/
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
WS.initialize(`${protocol}://${window.location.host}/ws/`, {
  onopen: () => {
    console.log("[WS DEBUG] Connection opened!");
    toast("Connected to WS!", { autoClose: 4000 });
  },

  onclose: (ev: CloseEvent) => {
    console.warn("[WS DEBUG] Connection closed", {
      code: ev.code,
      reason: ev.reason,
      wasClean: ev.wasClean,
    });
    toast("Disconnected, reconnecting in 6 seconds...", { autoClose: 4000 });
  },

  onerror: (err: Event) => {
    console.error("[WS DEBUG] Connection error", err);
  },

  onmessage: (e: MessageEvent) => {
    try {
      const data = JSON.parse(e.data);
      console.log("[WS DEBUG] Message received:", data);
    } catch (err) {
      console.log("[WS DEBUG] Non-JSON message received:", e.data);
    }
  },
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
  <MainMenu v-if="currentScreen === 'mainMenu'" @join-lobby="handleJoinLobby"></MainMenu>
  <Lobby v-if="currentScreen === 'lobby'" :player="player" @leave-game="handleLeaveGame" @start-game="handleStartQuestion"></Lobby>
  <Game v-if="currentScreen === 'question'" @leave-game="handleLeaveGame"></Game>
</template>

<style>
</style>
