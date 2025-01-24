<template>
<div class="divider">
    <span>or</span>
</div>
</template>

<style scoped>
.divider {
	display: flex;
	align-items: center;
	text-align: center;
	margin: 1rem 0;
}

.divider::before,
.divider::after {
	content: '';
	flex: 1;
	border-bottom: 1px solid #ddd;
}

.divider span {
	padding: 0 10px;
	color: #757575;
	font-size: 0.9rem;
}
</style>