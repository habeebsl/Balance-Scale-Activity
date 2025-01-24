import { defineStore } from 'pinia'

export const useRoleState = defineStore('roleState', {
    state: () => ({
        selectedRole: ''
    }),

    actions: {
        selectRole(role: string) {
            this.selectedRole = role
        }
    }    
})