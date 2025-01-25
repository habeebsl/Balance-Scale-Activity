<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { defineEmits } from 'vue'
import { useAuthMetaStore } from '@/stores/authMetaStore'
import AuthContainer from '@/components/AuthContainer.vue'
import Divider from '@/components/Divider.vue'
import GoogleButton from '@/components/GoogleButton.vue'
import ButtonSpinner from '@/components/ButtonSpinner.vue' 

const emit = defineEmits(['submit'])
const authMetaStore = useAuthMetaStore()

const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const handleSubmit = () => {
    emit('submit', {
        email: email.value,
        username: username.value,
        password: password.value,
        confirmPassword: confirmPassword.value
    })
}
</script>

<template>
<AuthContainer>
    <h1>Create Account</h1>
    <form @submit.prevent="handleSubmit">
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
            :disabled="authMetaStore.isSaving"
        >
            Sign Up
            <ButtonSpinner v-if="authMetaStore.isSaving" />
        </button>
    </form>
    
    <p class="login-link">
        Already have an account? <RouterLink to="/login">Log in</RouterLink>
    </p>

    <Divider />
    <GoogleButton buttonType="up" />
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