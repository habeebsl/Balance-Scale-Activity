<script setup>
import { useRouter, useRoute } from 'vue-router'
import { RouterLink } from 'vue-router'
import { ref, watch, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authManager'
 

const router = useRouter()
const authStore = useAuthStore()
const route = useRoute()

const isEducatorStatus = ref(false)

const checkEducatorStatus = async () => {

  if (authStore.isLoading) {
      await new Promise(resolve => {
          const unsubscribe = watch(
              () => authStore.isLoading,
              (loading) => {
                  if (!loading) {
                      unsubscribe()
                      resolve()
                  }
              },
              { immediate: true }
          )
      })
  }

  const tokenResult = await authStore.currentUser?.getIdTokenResult()
  isEducatorStatus.value = tokenResult?.claims.role === "educator"
}

watch(() => authStore.currentUser, checkEducatorStatus, { immediate: true })

const handleSignOut = () => {
    authStore.signoutUser()
    router.push("/login")
}

const shouldShowNavbar = computed(() => {
  const navbarRoutes = ['/dashboard', '/dashboard/', '/activities', '/activities/']
  return navbarRoutes.includes(route.path)
})

onMounted(() => {
	checkEducatorStatus()
})
</script>

<template>
  <nav class="navbar" 
  v-if="authStore.currentUser && shouldShowNavbar"
  >
    <div class="nav-container">
		<div class="nav-brand">
			<h1>Balance Scale</h1>
		</div>
		
		<div class="nav-links">
			<RouterLink 
				v-if="isEducatorStatus"
				to="/dashboard" 
				class="btn nav-link"
				active-class="active"
			>
				Dashboard
			</RouterLink>

			<RouterLink 
				to="/activities" 
				class="btn nav-link"
				active-class="active"
			>
				Activities
			</RouterLink>
			
			<RouterLink 
				v-if="isEducatorStatus"
				class="btn nav-link"
				to="/activities/create"
				active-class="active"
			>
				Create
			</RouterLink>
			
			<button @click="handleSignOut" class="btn signout-btn">
				<span class="btn-text">Sign Out</span>
			</button>
		</div>
    </div>
  </nav>
</template>
  
<style scoped>
.navbar {
	background-color: #ffffff;
	padding: 0.75rem 2rem;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	position: fixed;
	top: 0;
	width: 100%;
	z-index: 1000;
}

.nav-container {
	display: flex;
	justify-content: space-between;
	align-items: center;
	max-width: 1400px;
	margin: 0 auto;
}

.nav-brand h1 {
	margin: 0;
	font-size: 1.5rem;
	color: #333;
}

.nav-links {
	display: flex;
	align-items: center;
	gap: 1.5rem;
}

.btn {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	padding: 0.5rem 1rem;
	border-radius: 6px;
	font-weight: 500;
	border: none;
	cursor: pointer;
	transition: all 0.2s ease;
	text-decoration: none;
}

.btn-text {
 	margin: 0 0.25rem;
}

.nav-link {
	background-color: #3b82f6;
	color: white;
}

.nav-link:hover {
	background-color: #2563eb;
	transform: translateY(-1px);
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link.active {
	background-color: #1a57da;
	box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signout-btn {
	background-color: #fff;
	color: #f44336;
	border: 1px solid #f44336;
}

.signout-btn:hover {
	background-color: #f44336;
	color: white;
	transform: translateY(-1px);
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.signout-btn:active {
	transform: translateY(0);
}

@media (max-width: 640px) {
	.navbar {
		padding: 0.75rem 1rem;
	}

	.nav-links {
		gap: 0.75rem;
	}

	.btn {
		padding: 0.5rem 0.75rem;
	}
}
</style>