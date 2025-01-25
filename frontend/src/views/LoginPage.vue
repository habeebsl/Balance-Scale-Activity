<script setup>
import { getAuth, signInWithEmailAndPassword } from "firebase/auth"
import { useRouter } from 'vue-router'
import { getLoginErrorMessage } from '@/utils/helpers'
import { useAuthMetaStore } from "@/stores/authMetaStore"
import Login from "@/components/Login.vue"


const router = useRouter()
const authMetaStore = useAuthMetaStore()

const handleLogin = async (formData) => {
    try {
		authMetaStore.isSaving = true
		const auth = getAuth()
		await signInWithEmailAndPassword(auth, formData.email, formData.password)
		router.push("/activities")
    } catch (error) {
        console.error(error)
        authMetaStore.errorMessage = getLoginErrorMessage(error.code)
    } finally {
		authMetaStore.isSaving = false
    }
}
</script>

<template>
<Login 
	@submit="handleLogin"
/>
</template>