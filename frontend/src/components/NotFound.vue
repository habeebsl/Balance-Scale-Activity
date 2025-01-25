<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
<div class="not-found">
    <h1>404</h1>
    <p>Page not found</p>
    <RouterLink to="/activities" class="home-link">Go Home</RouterLink>
</div>
</template>

<style scoped>
.not-found {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

h1 {
    font-size: 48px;
    color: #333;
    margin-bottom: 16px;
}

p {
    color: #666;
    margin-bottom: 24px;
}

.home-link {
    padding: 8px 16px;
    background: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}

.home-link:hover {
    background: #0056b3;
}
</style>