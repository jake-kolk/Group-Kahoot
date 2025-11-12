<script setup>
    import { ref } from 'vue'
    import qcCard from "./HostCardsComp/QuestionCount.vue"
    import qTimer from "./HostCardsComp/QuestionTimer.vue"
    import qSet from "./HostCardsComp/QuestionSet.vue"

    
    
</script>
<template>
    <h1>Welcome, Host</h1>
   
    <qcCard></qcCard>
    <qTimer></qTimer>
    <qSet></qSet>
    <button>Play</button>
    
</template>