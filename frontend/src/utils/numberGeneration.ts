interface NumberGenerationParams {
    currentNumber: number;
    targetNumber: number;
    inputsRemaining: number;
    difficulty: string;
}

export function generateNumberSet(params: NumberGenerationParams): number[] {
    const { currentNumber, targetNumber, inputsRemaining, difficulty } = params
    const distanceToTarget = targetNumber - currentNumber
    const numbers: number[] = []
    const usedNumbers = new Set<number>()

    function generateOptimalNumber(): number {
        return Math.ceil(distanceToTarget / inputsRemaining);
    }

    function generateNearOptimalNumber(optimal: number): number {
        let factor = null
        switch (difficulty) {
            case 'easy':
                factor = 0.5
                break
            case 'medium':
                factor = 0.7
                break
            case 'hard':
                factor = 0.9
                break
            default:
                factor = 0.6
                break
        }
        const variation = Math.max(1, Math.floor(optimal * (Math.random() * factor)))
        return optimal + (Math.random() < 0.5 ? -variation : variation)
    }

    function generateOvershootNumber(): number {
        return distanceToTarget + Math.ceil(Math.random() * (inputsRemaining * 2));
    }

    function generateTrickyNumber(optimal: number): number {
        return optimal + Math.floor(Math.random() * 3) * inputsRemaining;
    }

    if (inputsRemaining > 1) {
        const optimal = generateOptimalNumber();
        let factor = null
        switch (difficulty) {
            case 'easy':
                factor = 0.5
                break
            case 'medium':
                factor = 0.7
                break
            case 'hard':
                factor = 0.9
                break
            default:
                factor = 0.6
                break
        }
        if (Math.random() < factor) {
            numbers.push(optimal);
            usedNumbers.add(optimal);
        }

        while (numbers.length < 5) {
            let num;
            if (numbers.length === 1) num = generateNearOptimalNumber(optimal);
            else if (numbers.length === 2) num = generateTrickyNumber(optimal)
            else if (numbers.length === 3 && Math.random() < 0.3) num = generateTrickyNumber(optimal);
            else num = generateOvershootNumber();

            if (!usedNumbers.has(num) && num > 0) {
                numbers.push(num)
                usedNumbers.add(num)
            }
        }
    } else {
        numbers.push(distanceToTarget);
        usedNumbers.add(distanceToTarget);

        let addedOvershoot = false;

        while (numbers.length < 5) {
            let num;
            if (!addedOvershoot && numbers.length >= 3) {
                num = generateOvershootNumber();
                addedOvershoot = true;
            } else {
                num = distanceToTarget + (Math.random() < 0.5 ? 1 : -1) * Math.ceil(Math.random() * 5);
            }

            if (!usedNumbers.has(num) && num > 0) {
                numbers.push(num);
                usedNumbers.add(num);
            }
        }
    }

    return numbers.sort(() => Math.random() - 0.5);
}
