<script setup lang="ts">
import { ref } from 'vue';
import MainMenu from './components/MainMenu.vue'
import Lobby from './components/Lobby.vue';
import type { Player } from './game/Player';
import Question from './components/Question.vue';

const currentScreen = ref('mainMenu');
const player = ref();

function handleJoinLobby(plyr: Player) {
  currentScreen.value = 'lobby';
  player.value = plyr;
}

function handleLeaveGame() {
  currentScreen.value = 'mainMenu';
}

function handleStartQuestion() {
  currentScreen.value = 'question';
}

</script>

<template>

  <MainMenu v-if="currentScreen === 'mainMenu'" @join-lobby="handleJoinLobby"></MainMenu>
  <Lobby v-if="currentScreen === 'lobby'" :player="player" @leave-game="handleLeaveGame" @start-game="handleStartQuestion"></Lobby>
  <Question v-if="currentScreen === 'question'"></Question>
</template>

<style>
</style>
