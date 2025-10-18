<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import { WS } from '../services/WebSocket';
import { Player } from '../game/Player';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const vueEmit = defineEmits(['join-lobby']);
const name = ref("");
const roomID = ref("");
const log = ref<string[]>([]);
function addToLog(msg: string) {
  log.value.push(msg);
}

WS.initialize(`ws://${window.location.host}/ws/`, {
  onclose: () => toast("Disconnected, reconnecting in 6 seconds...", {autoClose: 4000}),
  onopen: () => toast("Connected to WS!", {autoClose: 4000}),
  onmessage: e => {addToLog(e.data); console.log(e.data)},
});

function handleJoin() {
  WS.emit('join', {name: name.value, room: roomID.value});
}

// confirmation from server
WS.on('joined', (data: Record<string, any>) => {
  const player = new Player(name.value, data.id)
  joinLobby(player);
});

function joinLobby(player: Player) {
  vueEmit('join-lobby', player);
}

onUnmounted(() => {
  WS.removeListener('joined');
});

</script>

<template>
  <h3>Kahoot clone - demo client</h3>
  <input id='name' placeholder='Name' v-model="name"></input><br></br>
  <input placeholder="Room Code" v-model="roomID"></input><br></br>
  <button id='join' @click="handleJoin">Join</button>
  <div id='log' style="margin-top: 1rem;">
    <div v-for="value in log">{{ value }}</div>
  </div>
</template>

<style>
#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
</style>