<template>
<div class="container">
    <div class="card">
        <slot></slot>
    </div>
</div>
</template>

<style scoped>
.container {
	min-height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	background-color: #f5f5f5;
	padding: 20px;
	max-width: 100%;
}

.card {
	background: white;
	padding: 2rem;
	border-radius: 10px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	width: 100%;
	max-width: 400px;
}
</style>