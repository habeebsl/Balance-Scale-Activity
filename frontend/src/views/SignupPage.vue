<script setup>
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth"
import { useRouter } from 'vue-router'
import { useAuthMetaStore } from '@/stores/authMetaStore'
import { getSignupErrorMessage } from '@/utils/helpers'
import { userService } from "@/services/api"
import Signup from '@/components/Signup.vue'

const router = useRouter()
const authMetaStore = useAuthMetaStore()


const handleFormSubmit = async (formData) => {
	if (!formData.password.length >= 8) {
        authMetaStore.errorMessage = 'Password must be at least 8 characters long'
        return
    }

    if (!formData.password === formData.confirmPassword) {
        authMetaStore.errorMessage = 'Passwords do not match'
        return
    }

	try {
		authMetaStore.isSaving = true
		const auth = getAuth()
		await createUserWithEmailAndPassword(auth, formData.email, formData.password)
		const userData = {
				username: formData.username
		}
		const response = await userService.createUser(userData)

		const data = response.data
		router.push("/select-role")

	} catch (error) {
		console.error(error)
		authMetaStore.errorMessage = getSignupErrorMessage(error.code)
	} finally {
		authMetaStore.isSaving = false
	}
}
</script>

<template>
<Signup 
	@submit="handleFormSubmit"
/>
</template>
