<script setup>
import { defineEmits, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthMetaStore } from '@/stores/authMetaStore'
import AuthContainer from './AuthContainer.vue'
import Divider from '@/components/Divider.vue'
import ButtonSpinner from '@/components/ButtonSpinner.vue'
import GoogleButton from '@/components/GoogleButton.vue'


const authMetaStore = useAuthMetaStore()
const emit = defineEmits(['submit'])
const email = ref('')
const password = ref('')

const handleLogin = () => {
	emit('submit', {
		email: email.value,
		password: password.value
	})
}
</script>

<template>
<AuthContainer>
	<h1>Welcome Back</h1>
	<form @submit.prevent="handleLogin">
		<div v-if="authMetaStore.errorMessage" class="error-message">
			{{ authMetaStore.errorMessage }}
		</div>
		<div class="input-group">
			<label for="email">Email</label>
			<input 
				type="email" 
				id="email" 
				v-model="email"
				placeholder="Enter your email"
				required
			>
		</div>
	
		<div class="input-group">
			<label for="password">Password</label>
			<input 
				type="password" 
				id="password" 
				v-model="password"
				placeholder="Enter your password"
				required
			>
			<RouterLink to="/forgot-password" class="forgot-password">Forgot password?</RouterLink>
		</div>

		<button type="submit" :disabled="authMetaStore.isSaving">
			Log In
			<ButtonSpinner v-if="authMetaStore.isSaving" />
		</button>
	</form>
	
	<p class="signup-link">
		Don't have an account? <RouterLink to="/signup">Sign up</RouterLink>
	</p>

	<Divider />
	<GoogleButton />
</AuthContainer>
</template>

<style scoped>
h1 {
	color: #333;
	margin-bottom: 1.5rem;
	text-align: center;
	font-size: 1.8rem;
}

.input-group {
	margin-bottom: 1.2rem;
	position: relative;
}

label {
	display: block;
	margin-bottom: 0.5rem;
	color: #555;
	font-size: 0.9rem;
}

input {
	width: 100%;
	padding: 0.8rem;
	border: 1px solid #ddd;
	border-radius: 6px;
	font-size: 1rem;
	transition: border-color 0.2s;
}

input:focus {
	outline: none;
	border-color: #4a90e2;
	box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.forgot-password {
	position: absolute;
	right: 0;
	top: 0;
	font-size: 0.8rem;
	color: #4a90e2;
	text-decoration: none;
}

.forgot-password:hover {
	text-decoration: underline;
}

button {
	display: flex;
	justify-content: center;
	gap: 7px;
	width: 100%;
	padding: 0.8rem;
	background-color: #3b82f6;
	color: white;
	border: none;
	border-radius: 6px;
	font-size: 1rem;
	cursor: pointer;
	transition: background-color 0.2s;
	margin-top: 1rem;
}

button:disabled {
	background-color: #2563eb;
	cursor: not-allowed;
}

button:hover {
	background-color: #2563eb;
}

.signup-link {
	text-align: center;
	margin-top: 1rem;
	color: #666;
	font-size: 0.9rem;
}

.signup-link a {
	color: #4a90e2;
	text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}

.error-message {
	background-color: #fee2e2;
	border: 1px solid #fecaca;
	color: #dc2626;
	padding: 0.75rem;
	border-radius: 6px;
	margin-bottom: 1rem;
	font-size: 0.875rem;
	text-align: center;
}
</style>