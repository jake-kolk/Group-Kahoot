<script setup>
    import { ref } from 'vue'
    
    let numQuestions = ref("30")

    //Update count in DB
    function SetQuestionCount()
    {
        numQuestions = numQuestions.value;
    }

    function getQuestionCount()
    {
        return numQuestions.value;
    }

    defineExpose({
    getQuestionCount,
    SetQuestionCount
    })

</script>
<template>
    <div class="card m-4">
        <div class="card-header">
            Question Count
        </div>
        <div class="card-body">
            <h5 class="card-title">Number of questions per game is {{numQuestions}}</h5>
            <input type="number" v-model.number="numQuestions" @change="numQuestions"> 
        </div>
    </div>
   

</template>