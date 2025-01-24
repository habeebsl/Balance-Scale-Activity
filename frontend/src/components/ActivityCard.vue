<script setup>
import ActivityContainer from './ActivityContainer.vue'
import { formatDate } from '@/utils/helpers'

defineProps({
    activityId: String,
    username: String,
    title: String,
    lastModified: Date,
    difficulty: {
        type: String,
        default: 'hard'
    }
})

</script>

<template>
<ActivityContainer :to="`/activities/${activityId}`">
	<div class="activity-status">
		<div class="left-status">
			<span class="status-indicator published">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M20 6L9 17l-5-5"/>
				</svg>
				Created by {{ username }}
			</span>
		</div>
		<div class="right-status">
			<span class="status-indicator difficulty" :class="difficulty.toLowerCase()">
				<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="difficulty-icon">
					<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
				</svg>
				{{ difficulty }}
			</span>
		</div>
	</div>
	<div class="activity-header">
		<h3 class="activity-title">
			{{ title }}
		</h3>
	</div>
	<div class="activity-date">
		Last updated on {{ formatDate(lastModified) }}
	</div>
</ActivityContainer>
</template>

<style scoped>
.activity-status {
    margin-bottom: 0.5rem;
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
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

.status-indicator.difficulty {
    background-color: #f3f4f6;
    color: #6b7280;
}

.status-indicator.difficulty.easy {
    background-color: #dcfce7;
    color: #22c55e;
}

.status-indicator.difficulty.medium {
    background-color: #fef3c7;
    color: #f59e0b;
}

.status-indicator.difficulty.hard {
    background-color: #fee2e2;
    color: #ef4444;
}

.activity-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
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

.activity-date {
    font-size: 0.875rem;
    color: #64748b;
    position: absolute;
    bottom: 1.1rem;
}
</style>