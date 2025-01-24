<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getIdToken } from 'firebase/auth'
import axios from 'axios';
import TemplateCard from '@/components/TemplateCard.vue'
import { useAuthStore } from '@/stores/authManager'
import { useActivity } from '@/stores/activityStore'
import EmptyState from '@/components/EmptyState.vue'
import NotificationMessage from '@/components/NotificationMessage.vue'
import LoadingScreen from '@/components/LoadingScreen.vue'


const authStore = useAuthStore()
const activityStore = useActivity()
const activities = ref([])

const showMessage = ref(false)
const message = ref('')
const messageType = ref('')
const isLoading = ref(false)

const router = useRouter()


const handleEdit = (id) => {
    router.push(`/activities/edit/${id}`)
}

const handleDelete = async (id) => {
    activityStore.isSaving = true;
    try {
		const response = await axios.delete(`http://localhost:8000/activities/${id}`, {
			headers: {
				Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
				"Content-Type": "application/json",
			}
		})
        console.log(response.status)
        if (response.status == 204) {
            activities.value.forEach((activity, index) => {
                if (activity.id === id) {
                    activities.value.splice(index, 1)
                }
            })
            message.value = "Template Deleted Successfully"
            messageType.value = "success"
            showMessage.value = true
        }
	} catch (error) {
		console.error(error)
		message.value = error.message
        messageType.value = "error"
		showMessage.value = true
	} finally {
        setTimeout(() => {
			showMessage.value = false
            activityStore.isSaving = false
		}, 3500)
	}
}

const handleCreate = () => {
    router.push("/activities/create")
}

onMounted(async () => {
    try {
        isLoading.value = true
        const response = await axios.get("http://localhost:8000/templates", {
			headers: {
				Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
				"Content-Type": "application/json",
            }
        })
        const data = response.data
        activities.value = data
        console.log(data)
    } catch (error) {
        console.error(error)
        message.value = error.message
        messageType.value = "error"
		showMessage.value = true
        setTimeout(() => {
			showMessage.value = false
		}, 3500)
    } finally {
        isLoading.value = false
    }
})

</script>

<template>
<LoadingScreen 
	:isVisible="isLoading"
/>
<div class="templates-container" v-if="!isLoading">
	<EmptyState 
		v-if="!activities.length"
		title="No Templates Found"
		description="Create your first template to get started"
		buttonText="Create Template"
		@create="handleCreate"
	/>
	<TemplateCard
		v-else
		v-for="activity in activities"
		:title="activity.name"
		:key="activity.id"
		:createdAt="new Date(activity.created_at)"
		:activityId="activity.id"
		:isPublished="activity.published"
		@delete="handleDelete"
		@edit="handleEdit"
	/>
</div>
<NotificationMessage 
	v-if="showMessage"
	:message="message"
	:type="messageType"
/>
</template>

<style scoped>
.templates-container {
	margin-top: 70px;
}
</style>