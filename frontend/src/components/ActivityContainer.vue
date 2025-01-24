<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
    to: String
})

const router = useRouter()

const handleClick = (event) => {
  if (!event.target.closest('.action-btn')) {
    router.push(props.to)
  }
}

</script>

<template>
<div 
	class="activity-container" 
	@click="handleClick"
	:class="{ 'clickable': true }"
>
	<slot></slot>
</div>
</template>

<style scoped>
.activity-container {
	width: 300px;
	height: 180px;
	padding: 1.5rem;
	background: white;
	border-radius: 12px;
	box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
	margin: 1rem;
	transition: all 0.2s;
	display: inline-block;
	vertical-align: top;
	cursor: pointer;
	user-select: none;
	border: 1px solid #e5e7eb;
	position: relative;
}

.activity-container:hover {
	transform: translateY(-2px);
	box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
	border-color: #3b82f6;
}
</style>