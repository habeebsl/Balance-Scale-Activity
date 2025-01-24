<script setup>
import { useRoute, useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import axios from 'axios'
import { getIdToken } from 'firebase/auth'
import { useAuthStore } from '@/stores/authManager'
import { useActivity } from '@/stores/activityStore'
import { isNegativeNumber } from '@/utils/helpers'
import LoadingScreen from '@/components/LoadingScreen.vue'
import CreateActivityLayout from '@/components/CreateActivityLayout.vue'
import Problem from '@/components/Problem.vue'
import NotificationMessage from '@/components/NotificationMessage.vue'

const route = useRoute()
const fullPath = route.path
const endingSegment = fullPath.split('/').filter(Boolean).pop()

const router = useRouter()
const authStore = useAuthStore()
const activityStore = useActivity()

const dbActivity = ref('')
const isLoading = ref(null)

const showMessage = ref(false)
const message = ref('')
const messageType = ref('')

const handleRemove = (index) => {
    activityStore.handleRemove(index)
}

const handleSave = async (formData) => {
    activityStore.isSaving = true;
    try {
        if (!activityStore.problems.length) {
	    	throw new Error("Activity must contain a problem")
    	}

        activityStore.problems.forEach((problem) => {
            const { limit, target } = problem;
            if (!limit || !target) {
                throw new Error("Required inputs must contain a value")
            }
            if (isNegativeNumber(limit) || isNegativeNumber(target)) {
                throw new Error("Inputs cannot be assigned negative numbers")
            }

        });

        if (activityStore.toRemove.length > 0) {
            const problemData = []
            activityStore.toRemove.forEach((problem) => {
                problemData.push({id: problem})
            })

            const response = await axios.delete(`http://localhost:8000/problems/delete`, {
                data: problemData,
                headers: {
                    Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
                    "Content-Type": "application/json",
                }
            })
            console.log(response.status)
        }

        const problemset = []
        activityStore.problems.forEach(problem => {
            const { key, ...rest } = problem
            problemset.push(rest)
        });

        const activityData = {
            name: formData.title,
            published: formData.isPublished,
            difficulty: formData.difficulty,
            problemset: problemset
        }

        const response = await axios.put(`http://localhost:8000/activities/${endingSegment}`, activityData, {
            headers: {
                Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
                "Content-Type": "application/json",
            }
        })
        console.log(response)
        activityStore.showSavedIndicator = true
        setTimeout(() => {
            activityStore.showSavedIndicator = false
        }, 2000)
        messageType.value = "success"
		message.value = "Template Saved Successfully"
		showMessage.value = true
        activityStore.saveComplete = true
    } catch (error) {
        console.error(error)
        messageType.value = "error"
		message.value = error.message
		showMessage.value = true
    } finally {
        activityStore.isSaving = false
        setTimeout(() => {
            showMessage.value = false
        }, 3500)
    }
}

onMounted(async () => {
    try {
        isLoading.value = true
        const response = await axios.get(`http://localhost:8000/activities/${endingSegment}`, {
			headers: {
				Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
				"Content-Type": "application/json",
            }
        })
        const data = response.data
        console.log(data)
        if (!data.can_edit) {
            router.push("/404-not-found")
        }
        dbActivity.value = data.activity
        console.log(data)
        activityStore.problems.length = 0

        dbActivity.value.problemset.forEach((problem) => {
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
        if (error.response && error.response.status === 404 || 403) {
            router.push("/404-not-found")
        } else {
            console.log(error)
        }
    } finally {
        isLoading.value = false
    }
})
</script>

<template>
<LoadingScreen 
    :isVisible="isLoading"
    loadingText="Loading Activity..."
/>
<CreateActivityLayout
    v-if="isLoading === false"
    :title="dbActivity.name"
    :difficulty="dbActivity.difficulty"
    :published="dbActivity.published"
    @save="handleSave"
>
<Problem 
    v-for="problem in activityStore.problems"
    :key="problem.key"
    :step="problem.step"
    :initial-data="problem"
    @remove="handleRemove"
/>
</CreateActivityLayout>
<NotificationMessage 
    v-if="showMessage"
    :message="message"
    :type="messageType"
/>
</template>