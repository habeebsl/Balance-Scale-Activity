<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/authManager'
import NavBar from '@/components/NavBar.vue'
import LoadingScreen from './components/LoadingScreen.vue'

const authStore = useAuthStore()
authStore.setupAuthListener()

</script>

<template>
<NavBar />
<RouterView />
<LoadingScreen 
:isVisible="authStore.isLoading"
/>
</template>