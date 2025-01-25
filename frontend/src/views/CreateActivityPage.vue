<script setup>
import { onMounted, ref } from 'vue'
import { activityService } from '@/services/api'
import Problem from '@/components/Problem.vue'
import CreateActivityLayout from '@/components/CreateActivityLayout.vue'
import { useActivity } from '@/stores/activityStore'
import NotificationMessage from '@/components/NotificationMessage.vue'
import { isNegativeNumber } from '@/utils/helpers'

const activityStore = useActivity()
const showMessage = ref(false)
const message = ref('')
const messageType = ref('')

const handleSave = async (formData) => {
    activityStore.isSaving = true
    try {
		if (!activityStore.problems.length) {
	    	throw new Error("Activity must contain a problem")
    	}

		activityStore.problems.forEach((problem) => {
			const { limit, target } = problem
			if (!limit || !target) {
				throw new Error("Required inputs must contain a value")
			}
			
			if (isNegativeNumber(limit) || isNegativeNumber(target)) {
				throw new Error("Inputs cannot be assigned negative numbers")
			}
		})

		const problemset = []
        activityStore.problems.forEach(problem => {
            const { key, ...rest } = problem
            problemset.push(rest)
        })

        const activityData = {
            name: formData.title,
			difficulty: formData.difficulty,
			published: formData.isPublished,
            problemset: problemset
        }
		
        const response = await activityService.createActivity(activityData)
		const data = response.data
		activityStore.showSavedIndicator = true
        setTimeout(() => {
            activityStore.showSavedIndicator = false
        }, 2000);
		message.value = "Template Created Successfully"
		messageType.value = "success"
		showMessage.value = true
		activityStore.saveComplete = true
    } catch (error) {
		console.error(error)
		message.value = error.message
		messageType.value = "error"
		showMessage.value = true
	} finally {
		activityStore.isSaving = false
		setTimeout(() => {
			showMessage.value = false
		}, 3500)
    }
}

const handleRemove = (index) => {
    activityStore.handleRemove(index)
}

onMounted(() => {
    activityStore.problems.length = 0
})
</script>

<template>
<CreateActivityLayout 
	title="Untitled"
	:published="false"
	difficulty="medium"
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