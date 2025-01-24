<script setup>
import { ref, computed } from 'vue'
import { getAuth, createUserWithEmailAndPassword, getIdToken } from "firebase/auth"
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'
import Divider from '@/components/Divider.vue'
import GoogleButton from '@/components/GoogleButton.vue'
import ButtonSpinner from '@/components/ButtonSpinner.vue' 
import { getSignupErrorMessage } from '@/utils/helpers'

const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const router = useRouter()
const errorMessage = ref('')
const isSaving = ref(false)

const isPasswordValid = computed(() => {
  return password.value.length >= 8
})

const doPasswordsMatch = computed(() => {
  return password.value === confirmPassword.value
})


const handleFormSubmit = async () => {
	if (!isPasswordValid.value) {
        errorMessage.value = 'Password must be at least 8 characters long'
        return
    }

    if (!doPasswordsMatch.value) {
        errorMessage.value = 'Passwords do not match'
        return
    }

	try {
		isSaving.value = true
		const auth = getAuth()
		const userCredential = await createUserWithEmailAndPassword(auth, email.value , password.value)
		const user = userCredential.user;
		const idToken = await getIdToken(user)
		const userData = {
				username: username.value
		}
		const response = await axios.post("http://localhost:8000/users/create", userData, {
			headers: {
				Authorization: `Bearer ${idToken}`,
				"Content-Type": "application/json",
			}
		})

		const data = response.data
		console.log(data)
		router.push("/select-role")

	} catch (error) {
		console.error(error)
		errorMessage.value = getSignupErrorMessage(error.code)
	} finally {
		isSaving.value = false
	}
}
</script>

<template>
	<div class="signup-container">
		<div class="signup-card">
			<h1>Create Account</h1>
			<form @submit.prevent="handleFormSubmit">
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
					<label for="username">Username</label>
					<input 
						type="text" 
						id="username" 
						v-model="username"
						placeholder="Enter your username"
						required
					>
				</div>

				<div class="input-group">
					<label for="password">Password</label>
					<input 
						type="password" 
						id="password" 
						minlength="6"
						v-model="password"
						placeholder="Enter your password"
						required
					>
					<span class="password-requirement">
						Must be at least 8 characters
					</span>
				</div>

				<div class="input-group">
					<label for="confirm-password">Confirm Password</label>
					<input 
						type="password" 
						id="confirm-password" 
						v-model="confirmPassword"
						placeholder="Confirm your password"
						required
					>
				</div>


				<button 
					type="submit" 
					:disabled="isSaving"
				>
					Sign Up
					<ButtonSpinner v-if="isSaving" />
				</button>
			</form>
			
			<p class="login-link">
				Already have an account? <RouterLink to="/login">Log in</RouterLink>
			</p>

			<Divider />
			<GoogleButton buttonType="up" />

		</div>
	</div>
</template>

<style scoped>
.signup-container {
	min-height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	background-color: #f5f5f5;
	padding: 20px;
}

.signup-card {
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

.password-requirement {
  display: block;
  font-size: 0.75rem;
  color: #666;
  margin-top: 0.25rem;
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
}

button:disabled {
  background-color: #2563eb;
  cursor: not-allowed;
}

button:hover {
	background-color: #2563eb;
}

.login-link {
	text-align: center;
	margin-top: 1rem;
	color: #666;
	font-size: 0.9rem;
}

.login-link a {
	color: #4a90e2;
	text-decoration: none;
}

.login-link a:hover {
	text-decoration: underline;
}
</style>