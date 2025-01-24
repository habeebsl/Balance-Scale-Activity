<script setup>
import { defineProps, defineEmits } from 'vue'
import { useActivity } from '@/stores/activityStore'
import ActivityContainer from '@/components/ActivityContainer.vue'
import { formatDate } from '@/utils/helpers'


const activityStore = useActivity()

const emit = defineEmits(['delete', 'edit'])

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    createdAt: {
        type: Date,
        required: true
    },

    activityId: String,

	isPublished: {
    type: Boolean
  }
})

const handleEdit = () => {
	emit('edit', props.activityId)
}

const handleDelete = () => {
	emit('delete', props.activityId)
}

</script>

<template>
<ActivityContainer :to="`/activities/${activityId}`">
	<div class="activity-status">
		<span class="status-indicator" :class="{ 'published': isPublished }">
			<svg v-if="isPublished" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<path d="M20 6L9 17l-5-5"/>
			</svg>
			{{ isPublished ? 'Published' : 'Draft' }}
		</span>
	</div>
	<div class="activity-header">
		<h3 class="activity-title">{{ title }}</h3>
		<div class="activity-actions">
			<button class="action-btn edit" @click="handleEdit" :disabled="activityStore.isSaving">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
				</svg>
			</button>
			<button class="action-btn delete" @click="handleDelete" :disabled="activityStore.isSaving">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M3 6h18"/>
					<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
					<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
				</svg>
			</button>
		</div>
	</div>
	<div class="activity-date">
		Created on {{ formatDate(createdAt) }}
	</div>
</ActivityContainer>
</template>

<style scoped>
.activity-status {
	margin-bottom: 1rem;
}

.status-indicator {
	display: inline-flex;
	align-items: center;
	gap: 0.25rem;
	padding: 0.25rem 0.75rem;
	border-radius: 9999px;
	font-size: 0.875rem;
	font-weight: 500;
	background-color: #f3f4f6;
	color: #6b7280;
	}

.status-indicator.published {
	background-color: #dbeafe;
	color: #2563eb;
}

.activity-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 1rem;
}

.activity-title {
	margin: 0;
	font-size: 1.25rem;
	font-weight: 600;
	color: #1e40af;
	flex: 1;
	margin-right: 1rem;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis; 
}

.activity-actions {
	display: flex;
	gap: 0.5rem;
}

.action-btn {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 32px;
	height: 32px;
	border: none;
	border-radius: 6px;
	cursor: pointer;
	transition: background-color 0.2s;
	z-index: 1;
}

.action-btn:hover {
  	background-color: #dbeafe;
}

.action-btn.edit {
  	color: #3b82f6;
}

.action-btn.delete {
  	color: #dc2626;
}

.activity-date {
	font-size: 0.875rem;
	color: #64748b;
	position: absolute;
	bottom: 1.5rem;
}
</style>