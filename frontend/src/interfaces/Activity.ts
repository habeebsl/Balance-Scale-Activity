import type { Problem } from "@/interfaces/Problem"

export interface Activity {
    title: string;
    difficulty: string;
    published: boolean;
    problemset: Problem[];
}