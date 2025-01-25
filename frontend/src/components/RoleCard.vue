<script setup>
import { useRoleStore } from '@/stores/roleStore'

defineProps({
    role: {
        type: String,
        required: true,
        validator: (value) => ['student', 'educator'].includes(value)
    }
})

const roleStore = useRoleStore()

</script>

<template>
<div 
    class="role-card" 
    :class="{ active: roleStore.selectedRole === role }"
    @click="roleStore.selectRole(role)"
>
    <slot></slot>
</div>
</template>

<style scoped>
.role-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 2rem;
	border: 2px solid #e2e8f0;
	border-radius: 12px;
	cursor: pointer;
	transition: all 0.3s ease;
	width: 200px;
}

.role-card:hover {
	transform: translateY(-4px);
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.role-card.active {
	border-color: #4f46e5;
	background-color: #f5f3ff;
}
</style>