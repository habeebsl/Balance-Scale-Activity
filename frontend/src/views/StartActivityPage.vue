<script setup>
import { v4 as uuidv4 } from 'uuid'
import { ref, computed, onMounted, reactive, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useActivity } from '@/stores/activityStore'
import { activityService } from '@/services/api'
import Popup from '@/components/Popup.vue'
import ActivityIntro from '@/components/ActivityIntro.vue'
import LoadingScreen from '@/components/LoadingScreen.vue'
import BalanceScale from '@/components/BalanceScale.vue'


const balanceScaleRef = ref(null)
const showIntro = ref(true)
const activityStore = useActivity()
const currentProblem = computed(() => {
    return activityStore.problems[activityStore.currentStep] || {}
})

console.log(currentProblem.time_limit)
const isLastStep = computed(() => activityStore.currentStep >= activityStore.problems.length - 1)

const router = useRouter()
const route = useRoute()
const fullPath = route.path
const endingSegment = fullPath.split('/').filter(Boolean).pop()

const data = ref('')
const isLoading = ref(false)

const state = reactive({
    isEqualtoTarget: ""
})

const handleStartClick = () => {
    showIntro.value = false
}

const handleNextStep = () => {
    state.isEqualtoTarget = ""
    activityStore.nextStep()
}

const handleRestartStep = async () => {
    state.isEqualtoTarget = ""
    await nextTick()
    if (balanceScaleRef.value) {
        balanceScaleRef.value.resetState()
    }
    activityStore.restartStep()
}

const handleRestartActivity = () => {
    state.isEqualtoTarget = ""
    activityStore.currentStep = 0 
}

const handleExitClick = () => {
    activityStore.currentStep = 0 
    router.push("/activities")
}

const equalToTarget = () => {
    state.isEqualtoTarget = true
}

const notEqualToTarget = () => {
    state.isEqualtoTarget = false
}

onMounted(async () => {
    try {
        isLoading.value = true
        const response = await activityService.getActivity(endingSegment)
        
        data.value = response.data.activity
        activityStore.problems.length = 0

        data.value.problemset.forEach((problem) => {
            activityStore.addDbProblem({
                id: problem.id,
                key: uuidv4(),
                step: problem.step,
                target: problem.target,
                limit: problem.limit,
                difficulty: problem.difficulty,
                time_limit: problem.time_limit,
                hint: problem.hint
            })
        })
        activityStore.updateSteps()

    } catch (error) {
        console.error(error.message)
        if (error.response && error.response.status === 404 || 403) {
            router.push("/404-not-found")
        }
    } finally {
        isLoading.value = false
    }
})
</script>

<template>
<LoadingScreen 
    :isVisible="isLoading"
/>

<ActivityIntro 
    v-if="showIntro && !isLoading"
    :description="`Hello there, you're about to start a ${data.difficulty} problem are you ready?`"
    @next="handleStartClick"
/>

<BalanceScale 
	v-if="!isLoading && !showIntro"
	ref="balanceScaleRef"
	:key="currentProblem.key"
	:target="currentProblem.target"
	:limit="currentProblem.limit"
	:timeLimit="currentProblem.time_limit"
	:hint="currentProblem.hint"
	:difficulty="currentProblem.difficulty"
	@time-up="notEqualToTarget"
	@equivalent="equalToTarget"
	@not-equivalent="notEqualToTarget"
/>

<Popup 
    v-if="state.isEqualtoTarget && !isLastStep" 
    primaryText="Next" 
    @primary="handleNextStep"
>
	You did it, Let's move on to the next step
</Popup>
<Popup 
    v-else-if="state.isEqualtoTarget === false"
    primaryText="Try Again" 
    @primary="handleRestartStep"
>
You're not quite there yet!
</Popup>
<Popup 
    v-if="state.isEqualtoTarget && isLastStep"
    primaryText="Play Again"
    secondaryText="Go back"
    :showSecondaryButton="true"
    @primary="handleRestartActivity"
    @secondary="handleExitClick"
>
	You've completed the activity
</Popup>
</template>

<style scoped>

</style>