<script setup>
import { useRouter } from 'vue-router'
import { defineEmits } from 'vue'

defineProps({
    description: String
})

const emit = defineEmits(['next'])

const router = useRouter()

const handleBackClick = () => {
    router.push("/activities")
}

const handleStartClick = () => {
    emit('next')
}
</script>

<template>
<div class="start-activity-container">
    <p class="description">
		{{ description }}
    </p>
    <div class="buttons-container">
		<button class="back-button" @click="handleBackClick">
			Go Back
		</button>
		<button class="start-button" @click="handleStartClick">
			Let's go
		</button>
    </div>
</div>
</template>

<style scoped>
.start-activity-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
    text-align: center;
}

.description {
    font-size: 1.25rem;
    color: #333;
    margin-bottom: 2rem;
    max-width: 600px;
    line-height: 1.5;
}

.buttons-container {
    display: flex;
    gap: 20px;
    align-items: center;
}

.start-button, .back-button {
    padding: 15px 32px;
    font-size: 1.1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: none;
}

.start-button {
    background-color: #3b82f6;
    color: white;
}

.back-button {
    background-color: #6c757d;
    color: white;
}

.start-button:hover {
    background-color: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.back-button:hover {
    background-color: #5a6268;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.start-button:active, .back-button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>