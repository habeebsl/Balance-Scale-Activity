import { defineStore } from "pinia";

export const useAuthMetaStore = defineStore('auth-meta', {
    state: () => ({
        errorMessage: null,
        isSaving: false
    })
})