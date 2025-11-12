<script setup lang="ts">
    import { ref } from 'vue'
    
    var numQuestions = ref("30")

    //Update count in DB
    function SetQuestionCount()
    {
        //
        console.log(numQuestions.value)
    }


</script>
<template>
    <div class="card m-4">
        <div class="card-header">
            Question Count
        </div>
        <div class="card-body">
            <h5 class="card-title">Number of questions per game {{numQuestions}}</h5>
            <input type="number" v-model.number="numQuestions" @change="SetQuestionCount"> 
            <button @click="SetQuestionCount">Set</button>
        </div>
    </div>
   

</template>