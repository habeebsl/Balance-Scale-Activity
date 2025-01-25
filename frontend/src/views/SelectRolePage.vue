<script setup>
import { watch, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authManager'
import { useRoleStore } from '@/stores/roleStore'
import { userService } from '@/services/api'
import RoleSelection from '@/components/RoleSelection.vue'
import NotificationMessage from '@/components/NotificationMessage.vue'


const authStore = useAuthStore()
const router = useRouter()
const roleStore = useRoleStore()

const showMessage = ref(false)
const message = ref('')
const messageType = ref('')

const handleButtonClick = async () => {
    roleStore.isSaving = true

    if (authStore.isLoggedIn) {
        try {
            const roleData = { role: roleStore.selectedRole }
            const response = await userService.setUserRole(roleData)
            const data = response.data
            if (data.error) {
                throw new Error(data.error)
            } else {
                await authStore.currentUser?.getIdToken(true)
                router.push("/activities")
            }
        } catch (error) {
            console.error(error)
            message.value = error.message
            messageType.value = "error"
            showMessage.value = true
        } finally {
            roleStore.isSaving = false
        }
    }
}
</script>

<template>
<RoleSelection 
    @finish="handleButtonClick"
/>
<NotificationMessage 
    v-if="showMessage" 
    :message="message"
    :type="messageType" 
/>
</template>