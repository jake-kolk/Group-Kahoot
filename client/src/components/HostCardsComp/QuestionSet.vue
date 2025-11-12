<script setup lang="ts">
    import { ref } from 'vue'
    
    const currSet = ref('Sports Trivia')
    const selected = ref('') 

    function SetQuestion()
    {
        
    }

</script>
<template>
    <div class="card m-4">
        <div class="card-header">
            Questions Set
        </div>
        <div class="card-body">
            <h5 class="card-title">Current set of questions: {{currSet}}</h5>
            <select v-model="selected">
                <option disabled value="">Please select one</option>
                <option>Set 1</option>
                <option>Set 2</option>
                <option>Set 3</option>
            </select>
            <button class="m-2" @click="SetQuestion">Set</button>
        </div>
    </div>
   

</template>