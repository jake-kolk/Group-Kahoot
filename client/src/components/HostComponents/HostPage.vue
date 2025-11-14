<script setup lang="ts">
import { ref } from 'vue';
import PlayersJoin from './PlayersJoin.vue'
import CreateGame from './CreateGame.vue'
// import RunGame from './RunGame.vue'
//import { WS } from '@/services/WebSocket'
import { Host } from "@/game/Host";
import { WS } from '@/services/WebSocket';
import { toast } from 'vue3-toastify';

//import { toast } from 'vue3-toastify';

// This is where EVERYTHING host related is ran from, it has multiple screens for create game, players join, and run game. 
const currentScreen = ref('CreateGame');
//var host: Host;
const host = ref<Host | null>(null);
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

function createHost(room_num: number, token: string) {
  host.value = new Host(room_num, token);
  console.log("Host created!", host.value);
}

function enterLobby(){
  currentScreen.value = "PlayersJoin";
}

function addPlayer(name: string){
  host.value.addPlayer(name);
  console.log("Added player ", name)
}

function handleEndGame(){
  
}
</script>

<template>
  <CreateGame v-if="currentScreen === 'CreateGame'" @createHost="createHost" @enterLobby="enterLobby"></CreateGame>
  <PlayersJoin v-if="currentScreen === 'PlayersJoin'" :host="host" @addPlayer="addPlayer" />
  <Game v-if="currentScreen === 'RunGame'" @leave-game="handleLeaveGame"></Game>
</template>

<style>
</style>
