<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
    numbers: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['selected'])

const numberItems = computed(() => {
    return props.numbers.map((number, index) => ({
        id: `${number}-${index}`,
        value: number
    }))
})

const selectedIds = ref([])

const toggleSelection = (item) => {
    const index = selectedIds.value.indexOf(item.id)
    if (index === -1) {
        selectedIds.value.push(item.id)
        emit('selected', { number: item.value, selected: true, id: item.id })
    } else {
        selectedIds.value.splice(index, 1)
        emit('selected', { number: item.value, selected: false, id: item.id })
    }
}
</script>

<template>
  <div class="number-selection-panel">
    <div class="number-grid">
      <div
        v-for="item in numberItems"
        :key="item.id"
        class="number-box"
        :class="{ 'selected': selectedIds.includes(item.id) }"
        @click="toggleSelection(item)"
      >
        {{ item.value }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.number-selection-panel {
    position: fixed;
    top: 0;
    right: 0;
    width: 450px;
    height: 100vh;
    background-color: #ffffff;
    box-shadow: -4px 0 10px rgba(0, 0, 0, 0.1);
    z-index: 40;
    padding: 25px;
    overflow-y: auto;
}

.number-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding-top: 10px;
}

.number-box {
    background-color: #E8F4F8;
    border: 3px solid #A0D8EF;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: #2B87B3;
    cursor: pointer;
    transition: transform 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
    height: 80px;
}

.number-box:hover {
    transform: translateY(-3px);
    background-color: #F0F8FC;
}

.number-box.selected {
    background-color: #D1F2D1;
    border-color: #86C786;
    color: #2E8B57;
}

@media (max-width: 768px) {
    .number-selection-panel {
        width: 100%;
    }
    
    .number-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }
    
    .number-box {
        height: 70px;
        font-size: 20px;
    }
}
</style>