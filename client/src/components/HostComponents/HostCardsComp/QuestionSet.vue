<script setup>
    import { useRouter } from 'vue-router'
    import { ref, onMounted } from 'vue' 

    const router = useRouter()

    let currSet = 0;

    function getQuestionSet(){
        return currSet;
    }

    function setQuestionSet(){
        currSet = currSet;
    }

    function handleCreateNewSet()
    {
        router.push({
            path: '/question_sets/:UserId/edit/:id', // This is almost certainly broken, TODO fix ts
            query: { redirect: '/create_game' }  // remember where the user was going
        })
    }

    defineExpose({
    setQuestionSet,
    getQuestionSet
    })

</script>
<template>
    <div class="card m-4">
        <div class="card-header">
            Questions Set
        </div>
        <div class="card-body">
            <h5 class="card-title">Current set of questions: {{currSet}}</h5> 
            <select v-model="selected">
                <option>Please select one</option>
                <option>Set 1</option>
                <option>Set 2</option>
                <option>Set 3</option>
            </select>
             <button @click="handleCreateNewSet">Cretae new set</button>
        </div>
    </div>
   

</template>