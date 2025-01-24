import { defineStore } from 'pinia'
import { onAuthStateChanged, getAuth, signOut, type User } from 'firebase/auth' 

export const useAuthStore = defineStore('auth', {
    state: () => ({
        isLoggedIn: false,
        isLoading: true,
        currentUser:  null as User | null,
    }),

    actions: {
        setupAuthListener() {
            this.isLoading = true
            const auth = getAuth()
            onAuthStateChanged(auth, (user) => {
                if (user) {
                    this.currentUser = user
                    this.isLoggedIn = true
                } else {
                    this.isLoggedIn = false
                    this.currentUser = null
                }
                this.isLoading = false
            })
        },

        async signoutUser() {
            try {
                this.isLoading = true
                const auth = getAuth()
                await signOut(auth)

                this.isLoggedIn = false
                this.currentUser = null
                console.log("Signout Successful")
            } catch (error) {
                console.error(error)
            } finally {
                this.isLoading = false
            }
        }
    }
})