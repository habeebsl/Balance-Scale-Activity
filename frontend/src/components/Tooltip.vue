<script setup>
import { ref, onMounted, onUnmounted, computed, watchEffect } from 'vue'

const props = defineProps({
  text: {
    type: String,
    required: true
  },
  position: {
    type: Object,
    required: true,
    validator: (value) => {
      return typeof value.x === 'number' && typeof value.y === 'number'
    }
  },
  show: {
    type: Boolean,
    default: false
  },
  direction: {
    type: String,
    default: 'top',
    validator: (value) => ['top', 'bottom', 'left', 'right'].includes(value)
  },
  currentStep: {
    type: Number,
    default: 1
  },
  totalSteps: {
    type: Number,
    default: 1
  },
  nextButtonText: {
    type: String,
    default: 'Next'
  }
})

const emit = defineEmits(['next', 'close'])
const tooltipRef = ref(null)

const isLastStep = computed(() => props.currentStep === props.totalSteps)
const progressPercentage = computed(() => 
  ((props.currentStep - 1) / (props.totalSteps - 1)) * 100
)

// Calculate position and handle direction
const calculatePosition = () => {
  if (!tooltipRef.value) return { left: '0px', top: '0px' }
  
  const tooltip = tooltipRef.value
  const offset = 16 // Increased offset for better spacing
  const tooltipWidth = tooltip.offsetWidth
  const tooltipHeight = tooltip.offsetHeight
  
  // Get viewport dimensions
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  
  let left = 0
  let top = 0
  
  // Calculate base position based on direction
  switch(props.direction) {
    case 'top':
      left = props.position.x - (tooltipWidth / 2)
      top = props.position.y - tooltipHeight - offset
      break
    case 'bottom':
      left = props.position.x - (tooltipWidth / 2)
      top = props.position.y + offset
      break
    case 'left':
      left = props.position.x - tooltipWidth - offset
      top = props.position.y - (tooltipHeight / 2)
      break
    case 'right':
      left = props.position.x + offset
      top = props.position.y - (tooltipHeight / 2)
      break
  }
  
  // Adjust for viewport boundaries
  const padding = 10
  left = Math.max(padding, Math.min(left, viewportWidth - tooltipWidth - padding))
  top = Math.max(padding, Math.min(top, viewportHeight - tooltipHeight - padding))
  
  return {
    left: `${left}px`,
    top: `${top}px`
  }
}

// Watch for changes that should trigger position updates
watchEffect(() => {
  if (props.show && tooltipRef.value) {
    const { left, top } = calculatePosition()
    tooltipRef.value.style.left = left
    tooltipRef.value.style.top = top
  }
})

const updatePosition = () => {
  if (props.show && tooltipRef.value) {
    const { left, top } = calculatePosition()
    tooltipRef.value.style.left = left
    tooltipRef.value.style.top = top
  }
}

onMounted(() => {
  window.addEventListener('resize', updatePosition)
  window.addEventListener('scroll', updatePosition, true)
})

onUnmounted(() => {
  window.removeEventListener('resize', updatePosition)
  window.removeEventListener('scroll', updatePosition, true)
})

const handleNext = () => {
  if (isLastStep.value) {
    emit('close')
  } else {
    emit('next')
  }
}
</script>

<template>
  <Transition name="fade">
    <div 
      v-if="show" 
      ref="tooltipRef" 
      class="tooltip"
      :class="direction"
    >
      <div class="tooltip-header">
        <button 
          class="close-button"
          @click="$emit('close')"
          aria-label="Close tutorial"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M1 1L13 13M1 13L13 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
      
      <div class="tooltip-content">
        {{ text }}
      </div>
      
      <div class="tooltip-footer">
        <div class="progress-container">
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: `${progressPercentage}%` }"
            ></div>
          </div>
          <span class="step-indicator">{{ currentStep }} of {{ totalSteps }}</span>
        </div>
        
        <button 
          class="next-button"
          @click="handleNext"
        >
          {{ isLastStep ? 'Finish' : nextButtonText }}
          <svg 
            v-if="!isLastStep"
            width="16" 
            height="16" 
            viewBox="0 0 16 16" 
            fill="none"
            class="next-icon"
          >
            <path d="M6 12L10 8L6 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
      
      <div class="tooltip-arrow"></div>
    </div>
  </Transition>
</template>

<style scoped>
.tooltip {
  position: fixed;
  background: #ffffff;
  color: #0f172a;
  border-radius: 16px;
  font-size: 15px;
  max-width: 320px;
  min-width: 240px;
  z-index: 1000;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12), 
              0 0 1px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}

/* Direction-specific styles for the arrow */
.tooltip.top .tooltip-arrow {
  bottom: -7px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  border-top: none;
  border-left: none;
}

.tooltip.bottom .tooltip-arrow {
  top: -7px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  border-bottom: none;
  border-right: none;
}

.tooltip.left .tooltip-arrow {
  right: -7px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
  border-right: none;
  border-top: none;
}

.tooltip.right .tooltip-arrow {
  left: -7px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
  border-left: none;
  border-bottom: none;
}

.tooltip-arrow {
  position: fixed;
  width: 14px;
  height: 14px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tooltip-header {
  display: flex;
  justify-content: flex-end;
  padding: 12px 12px 0 12px;
  min-height: 40px;
}

.tooltip-content {
  padding: 0 20px;
  line-height: 1.6;
  font-weight: 450;
  flex-grow: 1;
}

.tooltip-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-top: 1px solid #f1f5f9;
  margin-top: 16px;
}

.progress-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-bar {
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #0f172a;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.step-indicator {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.next-button {
  background-color: #0f172a;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.next-button:hover {
  background-color: #1e293b;
  transform: translateY(-1px);
}

.next-button:active {
  transform: translateY(0);
}

.next-icon {
  transition: transform 0.2s ease;
}

.next-button:hover .next-icon {
  transform: translateX(2px);
}

.close-button {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  line-height: 0;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  background-color: #f1f5f9;
  color: #0f172a;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.96);
}
</style>