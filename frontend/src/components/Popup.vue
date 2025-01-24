<script setup>
import { ref, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
    primaryText: String,
    showSecondaryButton: {
        type: Boolean,
        default: false
    },
    secondaryText: {
        type: String,
        default: "Cancel"
    }
})

const emit = defineEmits(['primary', 'secondary'])

const router = useRouter()
const visible = ref(true);

const handlePrimaryClick = () => {
    visible.value = false
    emit('primary')
}

const handleSecondaryClick = () => {
    visible.value = false
    emit('secondary')
}
</script>

<template>
<Transition name="fade">
    <div v-if="visible" class="popup-overlay">
        <div class="popup">
            <h2 class="popup-title"><slot></slot></h2>
            <div class="popup-actions" :class="{ 'popup-actions--single': !showSecondaryButton }">
                <button class="popup-button popup-button--primary" @click="handlePrimaryClick">
                    {{ primaryText }}
                </button>
                <button 
                    v-if="showSecondaryButton"
                    class="popup-button popup-button--secondary" 
                    @click="handleSecondaryClick"
                >
                    {{ secondaryText }}
                </button>
            </div>
        </div>
    </div>
</Transition>
</template>

<style scoped>
.popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
}

.popup {
    background-color: #ffffff;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    text-align: center;
    width: 90%;
    max-width: 440px;
    animation: popup-appear 0.3s ease-out;
}

.popup-title {
    font-size: 1.75rem;
    color: #1a1a1a;
    margin-bottom: 2rem;
    font-weight: 600;
    line-height: 1.4;
}

.popup-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.popup-actions--single .popup-button {
    width: 100%;
}

.popup-button {
    flex: 1;
    padding: 0.875rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
}

.popup-button--primary {
    background-color: #2563eb;
    color: white;
}

.popup-button--primary:hover {
    background-color: #1d4ed8;
    transform: translateY(-1px);
}

.popup-button--secondary {
    background-color: #f3f4f6;
    color: #4b5563;
}

.popup-button--secondary:hover {
    background-color: #e5e7eb;
    transform: translateY(-1px);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

@keyframes popup-appear {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@media (max-width: 640px) {
    .popup {
        padding: 2rem;
        width: 95%;
    }
    
    .popup-title {
        font-size: 1.5rem;
    }
}
</style>