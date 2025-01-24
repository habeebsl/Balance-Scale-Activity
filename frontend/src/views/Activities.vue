<script setup>
import { getIdToken } from 'firebase/auth'
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import NotificationMessage from '@/components/NotificationMessage.vue'
import ActivityCard from '@/components/ActivityCard.vue'
import { useAuthStore } from '@/stores/authManager'
import LoadingScreen from '@/components/LoadingScreen.vue'
import EmptyState from '@/components/EmptyState.vue'

const authStore = useAuthStore()
const date = ref(new Date())

const showMessage = ref(false)
const message = ref('')
const messageType = ref('')
const isLoading = ref(null)
const selectedDifficulty = ref('all')

const activities = ref([])

const filteredActivities = computed(() => {
    if (selectedDifficulty.value === 'all') {
        return activities.value
    }
    return activities.value.filter(activity => 
        activity.difficulty.toLowerCase() === selectedDifficulty.value.toLowerCase()
    )
})

onMounted(async () => {
    try {
        isLoading.value = true
        const response = await axios.get("http://localhost:8000/activities", {
            headers: {
                Authorization: `Bearer ${await getIdToken(authStore.currentUser)}`,
                "Content-Type": "application/json",
            }    
        })
        const data = response.data
        activities.value = data
    } catch (error) {
        console.error(error)
        message.value = error.message
		messageType.value = "error"
		showMessage.value = true
    } finally {
        setTimeout(() => {
            showMessage.value = false
        }, 3500);
        isLoading.value = false
    }
})

</script>

<template>
<LoadingScreen 
	:isVisible="isLoading"
	loadingText="Loading Activities..."
/>
<div class="filter-container">
	<select 
		v-model="selectedDifficulty"
		class="difficulty-select"
	>
		<option value="all">All Difficulties</option>
		<option value="easy">Easy</option>
		<option value="medium">Medium</option>
		<option value="hard">Hard</option>
	</select>
</div>
<div class="activites-container" v-if="!isLoading">
	<EmptyState 
		v-if="!filteredActivities.length"
		title="No Activities Created Yet"
		description="Be on standby for now"
		:showButton="false"
		@create="handleCreate"
	/>

	<ActivityCard
		v-if="isLoading === false && filteredActivities.length"
		v-for="activity in filteredActivities"
		:title="activity.name"
		:lastModified="new Date(activity.last_modified)"
		:username="activity.username.toLowerCase()"
		:difficulty="activity.difficulty"
		:activityId="activity.id"
	/>
</div>
<NotificationMessage 
	v-if="showMessage"
	:message="message"
	:type="messageType"
/>
</template>

<style scoped>
.activities-container {
    margin-top: 20px;
}

.filter-container {
    margin-top: 90px;
    margin-bottom: 20px;
    display: flex;
    justify-content: flex-start;
    padding: 0 20px;
}

.difficulty-select {
    padding: 8px 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
    font-size: 14px;
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s;
}

.difficulty-select:hover {
    border-color: #999;
}

.difficulty-select:focus {
    border-color: #666;
    box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
}
</style>