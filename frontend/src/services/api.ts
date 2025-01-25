import axios from 'axios'
import { useAuthStore } from '@/stores/authManager'
import type { Activity } from '@/interfaces/Activity'
import type { CreateUser } from '@/interfaces/CreateUser'
import type { RemoveProblem } from '@/interfaces/RemoveProblem'
import type { SetRole } from '@/interfaces/SetRole'

const apiClient = axios.create({
	baseURL: 'http://localhost:8000/api',
	headers: {
		'Content-Type': 'application/json'
	}
})


apiClient.interceptors.request.use(async (config) => {
	const authStore = useAuthStore()
	if (!authStore.currentUser) {
		throw new Error('No user logged in');
	}
	const token = await authStore.currentUser.getIdToken()
	config.headers.Authorization = `Bearer ${token}`
	return config;
})


export const activityService = {
	createActivity(activityData: Activity) {
		return apiClient.post('/activities/create', activityData)
	},

	getActivity(endingSegment: string) {
		return apiClient.get(`/activities/${endingSegment}`)
	},

	updateActivity(endingSegment: string, activityData: Activity) {
		return apiClient.put(`/activities/${endingSegment}`, activityData)
	},

	deleteActivity(id: string) {
		return apiClient.delete(`/activities/${id}`)
	},

	getActivities() {
		return apiClient.get("/activities")
	},

	getTemplates() {
		return apiClient.get("/templates")
	}
}

export const problemService = {
	deleteProblem(problemData: RemoveProblem[]) {
		return apiClient.delete("/problems/delete", {
			data: problemData
		})
	}
}

export const userService = {
	createUser(userData: CreateUser) {
		return apiClient.post("/users/create", userData)
	},

	setUserRole(roleData: SetRole) {
		return apiClient.post("/users/set-user-role", roleData)
	}
}