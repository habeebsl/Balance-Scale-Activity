import { defineStore } from "pinia"
import { v4 as uuidv4 } from 'uuid'

interface Problem {
    id?: string;
    key: string;
    step: number;
    target: number;
    limit: number;
    difficulty: string;
    time_limit: number;
    hint: string;
}
  
export const useActivity = defineStore('activity', {
    state: () => ({
        isSaving: false,
        saveComplete: false,
        toRemove: [] as string[],
        showSavedIndicator: false,
        currentStep: 0,
        restartTrigger: 0,
        problems: [] as Problem[]
    }),
    
    actions: {
        addProblem(key: string) {
            this.problems.push({
                step: this.problems.length,
                key: key,
                target: 100,
                limit: 5,
                difficulty: 'medium',
                time_limit: 60,
                hint: ''
            })

            this.updateSteps()
        },

        nextStep() {
            if (this.currentStep < this.problems.length - 1) {
              this.currentStep++
            }
        },

        restartStep() {
            const currentActivity = this.problems[this.currentStep]
            this.problems[this.currentStep] = {
              ...currentActivity,
              key: uuidv4()
            }
        },

        restartActivity() {
            this.problems.forEach((problem, index) => {
                this.problems[index] = {
                    ...problem,
                    key: uuidv4()
                }
            })
        },

        addDbProblem({ id, key, step, target, limit, difficulty, time_limit, hint }: Problem) {
            this.problems.splice(step-1, 0, {
                id: id,
                key: key,
                step: step,
                target: target,
                limit: limit,
                difficulty: difficulty,
                time_limit: time_limit,
                hint: hint
            })
        },

        handleRemove(index: number) {
            const id = this.problems[index].id
            if (id) {
                this.toRemove.push(id)
            }
            this.problems.splice(index, 1)
            
            this.updateSteps()
        },

        updateSteps() {
            this.problems.sort((a, b) => a.step - b.step)
            this.problems = this.problems.map((problem, index) => ({
                ...problem,
                step: index + 1
            }))
        }
    }
})
