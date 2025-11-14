<script setup lang="ts">
import { ref } from 'vue';
import type { Host } from '@/game/Host';
import { WS } from '@/services/WebSocket'
import { getUserToken } from '@/store/userStore';
import { toast } from 'vue3-toastify';

const props = defineProps<{host: Host}>();
const vueEmit = defineEmits(['addPlayer']);

function handleStartGame() {
    console.log("sent this token for start game", getUserToken())
    let token = getUserToken();
    WS.emit('start_game', {
        "auth": token,
    })
}

function handleEndGame() {
    WS.emit('end_game',{
        auth: getUserToken()
    })
}
//{"type":"player_joined","id":player.id,"name":player.name}
WS.on('player_joined', (data: Record<string, any>) => {
    vueEmit('addPlayer', data.name);
});

</script>

<template>
  <div v-if="props.host">
    <h3>Waiting for players to join...</h3>
    <p>Room Number: {{ props.host.room_num }}</p>
    <p>Players:</p>

    <div v-for="player in props.host.players" :key="player">
      {{ player }}
    </div>

    <div>
      <button @click="handleStartGame">Start Game</button>
      <button @click="handleEndGame">End Game</button>
    </div>
  </div>
</template>

