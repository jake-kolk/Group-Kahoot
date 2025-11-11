<script setup>
    import { ref } from 'vue'
    import QcCard from "./HostCardsComp/QuestionCount.vue"
    import QTimer from "./HostCardsComp/QuestionTimer.vue"
    import QSet from "./HostCardsComp/QuestionSet.vue"

    
    
</script>
<template>
    <h1>Welcome, Host</h1>
   
    <qcCard></QcCard>
    <qTimer></QTimer>
    <qSet></QSet>
    
</template>