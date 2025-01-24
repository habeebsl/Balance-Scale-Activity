<script setup>
import { ref, nextTick, defineEmits, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'
import { useActivity } from '@/stores/activityStore'
import ButtonSpinner from './ButtonSpinner.vue'


const props = defineProps({
	title: {
		type: String,
		required: true,
	},
	difficulty: {
		type: String,
		required: true
	},
	published: {
		type: Boolean,
		required: true
	}
})

const activityStore = useActivity()
const isEditing = ref(false)
const inputRef = ref(null)

const titleInput = ref(props.title)
const isPublished = ref(props.published)
const selectedDifficulty = ref(props.difficulty)


const difficulties = [
	{ value: 'easy', label: 'Easy', color: '#22c55e' },
	{ value: 'medium', label: 'Medium', color: '#f59e0b' },
	{ value: 'hard', label: 'Hard', color: '#ef4444' }
]

const selectedDifficultyColor = computed(() => {
	return difficulties.find(d => d.value === selectedDifficulty.value)?.color || '#22c55e'
})

const emit = defineEmits(['save'])

const startEditing = async () => {
	isEditing.value = true
	await nextTick()
	inputRef.value?.focus()
}

const handleTitleChange = () => {
	if (!titleInput.value.trim()) {
		titleInput.value = props.title
	} 
	isEditing.value = false
}

const handleTitleKeydown = (e) => {
	if (e.key === 'Enter') {
		isEditing.value = false
	} else if (e.key === 'Escape') {
		isEditing.value = false
		titleInput.value = props.title
	}
}

const handleSave = async () => {
	emit('save', {
    title: titleInput.value, 
    difficulty: selectedDifficulty.value, 
    isPublished: isPublished.value,
  })
}

const handleDashboardClick = () => {
  activityStore.saveComplete = false
}

</script>

<template>
<div class="page-container">
	<header class="header">
		<div class="header-content">
			<div class="title-container">
				<input
					v-if="isEditing"
					v-model="titleInput"
					@blur="handleTitleChange"
					@keydown="handleTitleKeydown"
					class="title-input"
					type="text"
					ref="inputRef"
					:placeholder="title"
				/>
				<div 
					v-else 
					class="title-wrapper"
					@click="startEditing"
					role="button"
					tabindex="0"
					@keydown.enter="startEditing"
				>
					<h1 class="title">{{ titleInput }}</h1>
					<span class="edit-hint">✎</span>
				</div>
			</div>
			<div class="save-section">
				<select 
					v-model="selectedDifficulty"
					:style="{ borderColor: selectedDifficultyColor }"
				>
					<option
						v-for="option in difficulties"
						:value="option.value"
						:key="option.value"
					>
					{{ option.label }}
					</option>
				</select>

				<div class="publish-control">
					<span class="publish-label">Publish</span>
						<label class="switch">
						<input
							type="checkbox"
							v-model="isPublished"
						>
						<span class="switch-slider"></span>
					</label>
				</div>

				<span 
					v-if="activityStore.showSavedIndicator" 
					class="saved-indicator"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
						<path d="M20 6L9 17l-5-5"/>
					</svg>
					Saved!
				</span>
				<button @click="activityStore.addProblem(uuidv4())" :disabled="activityStore.isSaving">
					<svg 
					xmlns="http://www.w3.org/2000/svg" 
					width="20" 
					height="20" 
					viewBox="0 0 24 24" 
					fill="none" 
					stroke="currentColor" 
					stroke-width="2" 
					stroke-linecap="round" 
					stroke-linejoin="round"
					>
						<line x1="12" y1="5" x2="12" y2="19"/>
						<line x1="5" y1="12" x2="19" y2="12"/>
					</svg>
					Add Problem
				</button>
				<button 
					v-if="!activityStore.saveComplete"
					@click="handleSave" 
					class="save-button"
					:disabled="activityStore.isSaving"
				>
					<svg 
						v-if="!activityStore.isSaving"
						xmlns="http://www.w3.org/2000/svg" 
						width="20" 
						height="20" 
						viewBox="0 0 24 24" 
						fill="none" 
						stroke="currentColor" 
						stroke-width="2"
						stroke-linecap="round" 
						stroke-linejoin="round"
					>
						<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
						<polyline points="17 21 17 13 7 13 7 21"/>
						<polyline points="7 3 7 8 15 8"/>
					</svg>
						<ButtonSpinner v-else />
					<span>{{ activityStore.isSaving ? 'Saving...' : 'Save' }}</span>
				</button>
				<RouterLink class="dashboard-link" to="/dashboard" @click="handleDashboardClick" v-else>
					Go to Dashboard
				</RouterLink>
			</div>
		</div>
	</header>

	<main class="main-content">
		<slot></slot>
	</main>
</div>
</template>

<style scoped>
.page-container {
	min-height: 100vh;
	background-color: #f8fafc;
	padding-bottom: 2rem;
}

.header {
	background-color: white;
	border-bottom: 1px solid #e2e8f0;
	position: sticky;
	top: 0;
	z-index: 50;
	padding: 1rem 0;
	box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.header-content {
	max-width: 1200px;
	margin: 0 auto;
	padding: 0 1.5rem;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.title-container {
	flex: 1 1 auto;
	max-width: fit-content;
	border-bottom: 2px solid #e2e8f0;
	transition: border-color 0.2s ease;
}

.title-container:hover {
	border-bottom-color: #94a3b8;
}

.title-wrapper {
	display: flex;
	gap: 10px;
	align-items: center;
	cursor: text;
	padding: 0.25rem 0;
}

.title {
    width: 200px;
    font-size: 1.5rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.edit-hint {
	color: #94a3b8;
	font-size: 1.25rem;
	margin-left: auto;
}

.title-input {
	font-size: 1.5rem;
	font-weight: 600;
	color: #1e293b;
	width: inherit;
	padding: 0.25rem 0;
	border: none;
	outline: none;
	background-color: transparent;
}

.title-input:focus {
	border: none;
	box-shadow: none;
}

.save-section {
	display: flex;
	align-items: center;
	gap: 1rem;
}

.save-section button {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 1rem;
	border-radius: 8px;
	font-weight: 500;
	cursor: pointer;
	transition: all 0.2s ease;
}

.save-section button:not(.save-button) {
	background-color: white;
	color: #3b82f6;
	border: 1px solid #3b82f6;
}

.save-section button:not(.save-button):hover:not(:disabled) {
	background-color: #f0f7ff;
	transform: translateY(-1px);
}

.save-section button:not(.save-button):disabled {
	opacity: 0.7;
	cursor: not-allowed;
	border-color: #94a3b8;
	color: #94a3b8;
}

.saved-indicator {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	color: #16a34a;
	font-weight: 500;
	animation: fadeIn 0.3s ease-out;
}

.save-button {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 1rem;
	background-color: #3b82f6;
	color: white;
	border: none;
	border-radius: 8px;
	font-weight: 500;
	cursor: pointer;
	transition: all 0.2s ease;
}

.dashboard-link {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 1rem;
	background-color: #3b82f6;
	color: white;
	border: none;
	border-radius: 8px;
	font-weight: 500;
	cursor: pointer;
	transition: all 0.2s ease;
}

.dashboard-link:hover {
	background-color: #2563eb;
	transform: translateY(-1px);
}

.save-button:hover:not(:disabled) {
	background-color: #2563eb;
	transform: translateY(-1px);
}

.save-button:disabled {
	opacity: 0.7;
	cursor: not-allowed;
}

.main-content {
	max-width: 1200px;
	margin: 0 auto;
	padding: 2rem 1.5rem;
}

@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(-10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

select {
	padding: 0.625rem;
	width: 160px;
	border-radius: 8px;
	border: 1px solid #e5e7eb;
	background: #f9fafb;
	font-size: 0.875rem;
	transition: all 0.2s ease;
	cursor: pointer;
	border-left-width: 4px;
}

select:focus {
	outline: none;
	border-color: #3b82f6;
	background: white;
	box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.publish-control {
	display: flex;
	align-items: center;
	gap: 0.5rem;
}

.publish-label {
	font-size: 0.875rem;
	color: #64748b;
	font-weight: 500;
}

.switch {
	position: relative;
	display: inline-block;
	width: 48px;
	height: 24px;
}

.switch input {
	opacity: 0;
	width: 0;
	height: 0;
}

.switch-slider {
	position: absolute;
	cursor: pointer;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background-color: #e2e8f0;
	transition: .4s;
	border-radius: 34px;
}

.switch-slider:before {
	position: absolute;
	content: "";
	height: 20px;
	width: 20px;
	left: 2px;
	bottom: 2px;
	background-color: white;
	transition: .4s;
	border-radius: 50%;
}

input:checked + .switch-slider {
	background-color: #3b82f6;
}

input:checked + .switch-slider:before {
	transform: translateX(24px);
}
</style>