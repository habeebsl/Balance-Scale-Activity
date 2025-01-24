import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authManager'
import { watch } from 'vue'
import Activities from '@/views/Activities.vue'
import EducatorDashboard from '@/views/EducatorDashboard.vue'
import Signup from '@/views/Signup.vue'
import SelectRole from '@/views/SelectRole.vue'
import PageNotFound from '@/views/PageNotFound.vue'
import CreateActivity from '@/views/CreateActivity.vue'
import Login from '@/views/Login.vue'
import EditActivity from '@/views/EditActivity.vue'
import StartActivity from '@/views/StartActivity.vue'
import Home from '@/views/Home.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: "/",
        name: "home",
        component: Home,
        beforeEnter: (to, from, next) => {
            next("/activities")
        }
    },
    {
        path: "/signup",
        name: "signup",
        component: Signup,
        meta: {
            userSignedIn: true
        }
    },
    {
        path: "/select-role",
        name: "select-role",
        component: SelectRole,
        meta: {
            requiresAuth: true,
            roleSelected: true
        }
    },
    {
        path: "/login",
        name: "login",
        component: Login,
        meta: {
            userSignedIn: true
        }
    },
    {
        path: "/activities",
        name: "activities",
        component: Activities,
        meta: {
            requiresAuth: true,
            requiresRole: true
        }
    },
    {
        path: "/activities/:id",
        name: "activity-page",
        component: StartActivity
    },
    {
        path: "/activities/edit/:id",
        name: "edit-activity",
        component: EditActivity,
        meta: {
            requiresAuth: true,
            requiresRole: true,
            requiredRole: "educator"
        }
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: EducatorDashboard,
        meta: {
            requiresAuth: true,
            requiresRole: true,
            requiredRole: "educator"
        }
    },
    {
        path: "/activities/create",
        name: "create-activity",
        component: CreateActivity,
        meta: {
            requiresAuth: true,
            requiresRole: true,
            requiredRole: "educator"
        }
    },
    {
        path: "/:catchAll(.*)",
        name: "not-found",
        component: PageNotFound
    }
  ],
})

router.beforeEach(async (to, from, next) => {

    const authStore = useAuthStore()

    if (authStore.isLoading) {
        await new Promise<void>(resolve => {
            const unsubscribe = watch(
                () => authStore.isLoading,
                (loading) => {
                    if (!loading) {
                        unsubscribe()
                        resolve()
                    }
                },
                { immediate: true }
            )
        })
    }

    if (to.meta.requiresAuth) {
        if (!authStore.isLoggedIn) {
            next("/login")
            return
        } else {
            if (to.meta.requiresRole) {
                const tokenResult = await authStore.currentUser?.getIdTokenResult()
                if (tokenResult?.claims.role) {
                    if (to.meta.requiredRole) {
                        if (to.meta.requiredRole !== tokenResult?.claims.role) {
                            next("/activities")
                            return
                        } 
                    }
                } else {
                    next("/select-role")
                    return
                }
            }
            
            if (to.meta.roleSelected) {
                const tokenResult = await authStore.currentUser?.getIdTokenResult()
                if (tokenResult?.claims.role) {
                    next("/activities")
                    return
                }
            }

            next()
        }
        return
    }

    if (to.meta.userSignedIn) {
        if (authStore.isLoggedIn) {
            next("/activities")
        } else {
            next()
        }
        return
    }

    next()
})

export default router

