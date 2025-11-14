<script setup>
import { ref, onMounted } from 'vue' 
import QcCard from "./HostCardsComp/QuestionCount.vue"
import QTimer from "./HostCardsComp/QuestionTimer.vue"
import QSet from "./HostCardsComp/QuestionSet.vue"
import { checkAuth } from '@/services/ApiCall'
import { useRouter } from 'vue-router'
import { setUserToken, getUserToken } from "@/store/userStore";
import { getGameServerToken } from '@/services/ApiCall'
import { WS } from '@/services/WebSocket'
import { toast } from 'vue3-toastify';
import { nextTick } from 'vue';

const qcCardRef = ref()
const qTimerRef = ref()
const qSetRef = ref()
const router = useRouter()

var token;

const vueEmit = defineEmits(['createHost', 'enterLobby']);



WS.on('game_created', (response) => {
  console.log('Server response:', response);
  let room_code = response.room_number; // if server sends JSON with room_code

  if (response.success) {
        console.log("code + token", room_code, token);
        vueEmit('createHost', room_code, token); //create Host obj in parent
        nextTick(() => {
            vueEmit('enterLobby'); // now safe to switch screen
        });   // Switch screen to join_players
  } else {
    toast("Could not start game: " + response.error, { autoClose: 3000 });
  }
});

async function createGame(question_set, time_limit, question_count, auth_token) // All of type int
{
    try{
        WS.emit('create_game', { 
        auth: auth_token,
        question_set: question_set,
        time_limit: time_limit,
        question_count: question_count
        });
    }
    catch(except){
        console.log(except)
    }
}


async function handleCreateGame()
{
    // Get and save game server auth token
    //{question_set_id, question_duration, number_question})
    // tell db server to get an auth token from game sevrer
    token = await getGameServerToken();
    console.log("CreateGame: getGameServerToken: Got token, ", token);
    setUserToken(token);
    try{
        let room_num = createGame(
            qSetRef.value.getQuestionSet(),
            qTimerRef.value.getQuestionTimeLimit(),
            qcCardRef.value.getQuestionCount(),
            token
        )
    }
        catch (error){
        toast("Could not start game, please try again later", { autoClose: 3000 });
    }
}

onMounted(async () => {
    const authenticated = await checkAuth() // Check auth with db sevver
    if (!authenticated){
        router.push({
            path: '/login',
            query: { redirect: '/host' }  // remember where the user was going
        })
    }
})

</script>
<template>
  <h1>Welcome, Host</h1>
   
  <QcCard ref="qcCardRef" />
  <QTimer ref="qTimerRef" />
  <QSet ref="qSetRef" />
  
  <button @click="handleCreateGame">Start Game</button>

</template>
