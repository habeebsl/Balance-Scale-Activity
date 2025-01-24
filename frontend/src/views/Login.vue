<script setup>
import { ref } from 'vue'
import { getAuth, signInWithEmailAndPassword } from "firebase/auth"
import { RouterLink, useRouter } from 'vue-router'
import Divider from '@/components/Divider.vue'
import ButtonSpinner from '@/components/ButtonSpinner.vue'
import GoogleButton from '@/components/GoogleButton.vue'
import { getLoginErrorMessage } from '@/utils/helpers'


const email = ref('')
const password = ref('')
const router = useRouter()
const isSaving = ref(false)
const errorMessage = ref('')


const handleLogin = async () => {
    try {
		isSaving.value = true
		const auth = getAuth()
		const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value)
		const user = userCredential.user;
		console.log(user)
		console.log(auth.currentUser)
		router.push("/activities")
    } catch (error) {
        console.error(error)
        errorMessage.value = getLoginErrorMessage(error.code)
    } finally {
		isSaving.value = false
    }
}
</script>

<template>
<div class="login-container">
	<div class="login-card">
		<h1>Welcome Back</h1>
		<form @submit.prevent="handleLogin">
			<div v-if="errorMessage" class="error-message">
				{{ errorMessage }}
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

			<button type="submit" :disabled="isSaving">
				Log In
				<ButtonSpinner v-if="isSaving" />
			</button>
		</form>
		
		<p class="signup-link">
			Don't have an account? <RouterLink to="/signup">Sign up</RouterLink>
		</p>

		<Divider />
		<GoogleButton />
	</div>
</div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

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