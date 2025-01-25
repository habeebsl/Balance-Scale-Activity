import { defineStore } from 'pinia'

export const useRoleStore = defineStore('roleState', {
    state: () => ({
        selectedRole: '',
        isSaving: false
    }),

    actions: {
        selectRole(role: string) {
            this.selectedRole = role
        }
    }    
})