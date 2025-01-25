import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authManager'
import { watch } from 'vue'
import ActivitiesPage from '@/views/ActivitiesPage.vue'
import EducatorDashboard from '@/views/EducatorDashboard.vue'
import SignupPage from '@/views/SignupPage.vue'
import SelectRolePage from '@/views/SelectRolePage.vue'
import NotFoundPage from '@/views/NotFoundPage.vue'
import CreateActivityPage from '@/views/CreateActivityPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import EditActivityPage from '@/views/EditActivityPage.vue'
import StartActivityPage from '@/views/StartActivityPage.vue'
import HomePage from '@/views/HomePage.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: "/",
        name: "home",
        component: HomePage,
        beforeEnter: (to, from, next) => {
            next("/activities")
        }
    },
    {
        path: "/signup",
        name: "signup",
        component: SignupPage,
        meta: {
            userSignedIn: true
        }
    },
    {
        path: "/select-role",
        name: "select-role",
        component: SelectRolePage,
        meta: {
            requiresAuth: true,
            roleSelected: true
        }
    },
    {
        path: "/login",
        name: "login",
        component: LoginPage,
        meta: {
            userSignedIn: true
        }
    },
    {
        path: "/activities",
        name: "activities",
        component: ActivitiesPage,
        meta: {
            requiresAuth: true,
            requiresRole: true
        }
    },
    {
        path: "/activities/:id",
        name: "activity-page",
        component: StartActivityPage
    },
    {
        path: "/activities/edit/:id",
        name: "edit-activity",
        component: EditActivityPage,
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
        component: CreateActivityPage,
        meta: {
            requiresAuth: true,
            requiresRole: true,
            requiredRole: "educator"
        }
    },
    {
        path: "/:catchAll(.*)",
        name: "not-found",
        component: NotFoundPage
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

