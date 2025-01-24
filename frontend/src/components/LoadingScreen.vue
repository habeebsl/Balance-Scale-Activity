<script setup>
import { defineProps } from 'vue'

const props = defineProps({
isVisible: {
    type: Boolean,
    default: true
},
loadingText: {
    type: String,
    default: 'Loading...'
}
})
</script>

<template>
<div class="loading-container" v-if="isVisible">
    <div class="spinner"></div>
    <p class="loading-text">{{ loadingText }}</p>
</div>
</template>

<style scoped>
.loading-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.9);
    z-index: 9999;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.loading-text {
    margin-top: 1rem;
    font-size: 1.2rem;
    color: #333;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>