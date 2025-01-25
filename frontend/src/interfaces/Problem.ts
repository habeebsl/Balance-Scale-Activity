export interface Problem {
    id?: string;
    step: number;
    target: number;
    limit: number;
    difficulty: string;
    time_limit: number | null;
    hint: string;
}