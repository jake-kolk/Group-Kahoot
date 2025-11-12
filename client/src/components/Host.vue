<script setup>
    import { ref } from 'vue'
    import QcCard from "./HostCardsComp/QuestionCount.vue"
    import QTimer from "./HostCardsComp/QuestionTimer.vue"
    import QSet from "./HostCardsComp/QuestionSet.vue"

    
    
</script>
<template>
    <h1>Welcome, Host</h1>
   

    <qcCard></qcCard>
    <qTimer></qTimer>
    <qSet></qSet>
    <button>Play</button>

    
</template>