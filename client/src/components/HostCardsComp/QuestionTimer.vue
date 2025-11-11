<script setup>
    import { ref } from 'vue'
    
    const duration = ref(15*1000)

    // function setQuestionTimeLimit(newDuration)
    // {
    //     duration = newDuration
    // }
    // function SetQuestionTimer()
    // {

    // }
    
</script>
<template>
    <div class="card m-4">
        <div class="card-header">
            Time per Question
        </div>
        <div class="card-body">
            <h5 class="card-title">Current time per question is {{ (duration / 1000).toFixed(1) }} seconds</h5>
            <!-- <input type="number" :value="numQuestions" @change="SetQuestionCount">  -->
            <div>
                Duration:
                <input
                type="range"
                v-model.number="duration"
                min="1000"
                max="60000"
                step="1000"
                >
            </div>
            <button @click="setQuestionTimeLimit">Set</button>
        </div>
    </div>
   

</template>