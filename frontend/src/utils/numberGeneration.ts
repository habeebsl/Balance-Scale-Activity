interface PuzzleOptions {
    totalMoves: number;
    target: number;
    difficulty: 'easy' | 'medium' | 'hard';
}

interface PuzzleResult {
    numbers: number[];
    solution: number[];
}

export function generateNumberPuzzle(options: PuzzleOptions): PuzzleResult {
    const { totalMoves, target, difficulty } = options

    const extraNumbers = {
        easy: 2,
        medium: 3,
        hard: 4
    }

    function generateSolution(): number[] {
        const solution: number[] = []
        let remainingTarget = target
        
        for (let i = 0; i < totalMoves - 1; i++) {
            const maxPossible = remainingTarget - (totalMoves - i - 1)
            const minPossible = 1
            
            if (maxPossible < minPossible) {
                throw new Error('Invalid parameters')
            }
            
            const num = Math.floor(Math.random() * (maxPossible - minPossible + 1)) + minPossible
            solution.push(num)
            remainingTarget -= num
        }
        
        solution.push(remainingTarget)
        return solution
    }

    function generateDecoys(solution: number[]): number[] {
        const decoys: number[] = [];
        const totalDecoys = extraNumbers[difficulty];
        const used = new Set(solution);

        for (let i = 0; i < totalDecoys; i++) {
            let decoy = 1
            const max = Math.max(...solution) + 2
            
            while (used.has(decoy) && decoy <= max) {
                decoy++;
            }
            
            if (!used.has(decoy)) {
                decoys.push(decoy);
                used.add(decoy);
            }
        }

        return decoys
    }

    const solution = generateSolution()
    const decoys = generateDecoys(solution)
    const allNumbers = [...solution, ...decoys].sort(() => Math.random() - 0.5)

    return {
        numbers: allNumbers,
        solution: solution
    }
}