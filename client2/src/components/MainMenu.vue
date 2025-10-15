<script setup lang="ts">
import { ref } from 'vue';
import { WS } from '../services/WebSocket';

const name = ref("");
const log = ref<string[]>([]);
function addToLog(msg: string) {
  log.value.push(msg);
}

WS.initialize(`ws://${window.location.host}/ws/`);

function handleJoin() {
  WS.emit('join', {name: name.value, room: "100000"});
}

WS.on('joined', (data) => {
  addToLog(JSON.stringify(data));
});

WS.on('player_joined', data => {
  addToLog(JSON.stringify(data));
});

</script>

<template>
  <h3>Kahoot clone - demo client</h3>
  <input id='name' placeholder='Name' v-model="name"></input><button id='join' @click="handleJoin">Join</button>
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