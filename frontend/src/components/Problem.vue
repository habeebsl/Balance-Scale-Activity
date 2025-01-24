<script setup>
import { ref, computed, watch, defineEmits } from 'vue'
import { useActivity } from '@/stores/activityStore'

const props = defineProps({
	step: {
		type: Number,
		required: true
	},
	initialData: Object
})

const emit = defineEmits(['remove'])

const activityStore = useActivity()

const formData = ref({ ...props.initialData })

console.log(formData.value.difficulty)

const isEditing = ref(false)

const difficulties = [
	{ value: 'easy', label: 'Easy', color: '#22c55e' },
	{ value: 'medium', label: 'Medium', color: '#f59e0b' },
	{ value: 'hard', label: 'Hard', color: '#ef4444' }
]


const selectedDifficultyColor = computed(() => {
	return difficulties.find(d => d.value === formData.value.difficulty)?.color || '#22c55e'
})

const handleFocus = () => {
	isEditing.value = true
}

const handleBlur = () => {
    isEditing.value = false
}

const handleRemove = (e) => {
	e.stopPropagation()
	emit('remove', props.step-1)
}

watch(formData, (newVal) => {
    const processedData = {
        ...newVal,
        target: newVal.target === '' ? null : Number(newVal.target),
        limit: newVal.limit === '' ? null : Number(newVal.limit),
        time_limit: newVal.time_limit === '' ? null : Number(newVal.time_limit)
    }
    console.log(processedData)
    activityStore.problems[props.step - 1] = processedData
}, { deep: true })
</script>

<template>
<div 
	class="problem-editor"
	:class="{ 'is-editing': isEditing }"
	@focus="handleFocus"
	@blur="handleBlur"
	tabindex="0"
>
	<div class="step-badge">{{ step }}</div>
	<button
			class="remove-button" 
			@click="handleRemove" 
			title="Remove problem"
		>
		<svg 
			xmlns="http://www.w3.org/2000/svg" 
			width="14" 
			height="14" 
			viewBox="0 0 24 24" 
			fill="none" 
			stroke="currentColor" 
			stroke-width="2.5" 
			stroke-linecap="round" 
			stroke-linejoin="round"
		>
			<line x1="18" y1="6" x2="6" y2="18"></line>
			<line x1="6" y1="6" x2="18" y2="18"></line>
		</svg>
	</button>

	<div class="editor-content">
		<div class="input-grid">
			<div class="input-group">
				<label for="target">Target Number *</label>
				<input
					id="target"
					v-model.number="formData.target"
					type="number"
					min="0" 
					step="1"
					placeholder="Enter target number"
					required
				/>
			</div>

			<div class="input-group">
				<label for="limit">Input Limit *</label>
				<input
				id="limit"
				v-model.number="formData.limit"
				type="number"
				min="0" 
				step="1"
				placeholder="Enter limit"
				required
				/>
			</div>
			<div class="input-group">
				<label for="difficulty">Difficulty *</label>
				<select
					id="difficulty"
					v-model="formData.difficulty"
					:style="{ borderColor: selectedDifficultyColor }"
				>
				<option
					v-for="option in difficulties"
					:key="option.value"
					:value="option.value"
				>
					{{ option.label }}
				</option>
				</select>
			</div>

			<div class="input-group">
				<label for="timeLimit">Time Limit (seconds)</label>
				<input
				id="timeLimit"
				v-model.number="formData.time_limit"
				type="number"
				min="0" 
				step="1"
				placeholder="Optional"
				/>
			</div>
		</div>

		<div class="hint-group">
			<label for="hint">Hint</label>
			<textarea
				id="hint"
				v-model="formData.hint"
				placeholder="Enter a hint for solving this problem..."
				rows="3"
			></textarea>
		</div>
	</div>
</div>
</template>

<style scoped>
.problem-editor {
	position: relative;
	background: white;
	border-radius: 16px;
	padding: 2rem;
	margin: 1.5rem;
	box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
	transition: all 0.3s ease;
	border: 2px solid transparent;
	opacity: 0.85;
	max-width: 800px;
}

.problem-editor:hover {
	opacity: 0.95;
	cursor: pointer;
}

.problem-editor.is-editing {
	opacity: 1;
	border-color: #3b82f6;
	box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1), 0 4px 6px -2px rgba(59, 130, 246, 0.05);
}

.step-badge {
	position: absolute;
	top: -12px;
	left: -12px;
	width: 36px;
	height: 36px;
	background: #3b82f6;
	color: white;
	border-radius: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: 600;
	font-size: 1.1rem;
	box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
}

.editor-content {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
}

.input-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
	gap: 1.5rem;
}

.input-group {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

label {
	font-size: 0.875rem;
	font-weight: 500;
	color: #4b5563;
}

input, select, textarea {
	padding: 0.625rem;
	border-radius: 8px;
	border: 1px solid #e5e7eb;
	background: #f9fafb;
	font-size: 0.875rem;
	transition: all 0.2s ease;
}

input:focus, select:focus, textarea:focus {
	outline: none;
	border-color: #3b82f6;
	background: white;
	box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

select {
	cursor: pointer;
	border-left-width: 4px;
}

.hint-group {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

textarea {
	resize: vertical;
	min-height: 80px;
}

input::placeholder,
textarea::placeholder {
	color: #9ca3af;
}

label:has(+ input[required])::after,
label:has(+ select[required])::after {
	content: " *";
	color: #ef4444;
}

.remove-button {
	position: absolute;
	top: -12px;
	right: -12px;
	width: 28px;
	height: 28px;
	background: #ef4444;
	color: white;
	border: none;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	transition: all 0.2s ease;
	opacity: 0;
	transform: scale(0.9);
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.problem-editor:hover .remove-button {
	opacity: 1;
	transform: scale(1);
}

.remove-button:hover {
	background: #dc2626;
	transform: scale(1.1);
}

.remove-button:active {
	transform: scale(0.95);
}
</style>