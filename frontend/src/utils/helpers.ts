// Helper functions
export function isNumber(value: any) {
    return typeof value === 'number' && !isNaN(value)
}

export function isNegativeNumber(value: any) {
    return typeof value === 'number' && value < 0
}

export function getRandomColor() {
    const colors = ['black', 'ff5733', 'ffc733', '33ffe6', '33d4ff', 'be33ff', 'ff33dd', 'ff33b2']
    const randomIndex = Math.floor(Math.random() * colors.length)
    return colors[randomIndex]
}

export const getFontSize = (number: number) => {
	const digitCount = Math.abs(number).toString().length
	const baseFontSize = 50
	const reductionFactor = 0.9
	const reducedSize = baseFontSize * Math.pow(reductionFactor, digitCount - 1)
	const minimumFontSize = 25
	return Math.max(reducedSize, minimumFontSize)
};


export function getBallRadius(number: number) {
    const baseRadius = 20
    const maxRadius = 100

    const radius = Math.min(
        baseRadius * (1 + Math.log(Math.abs(number) + 1) / 2),
        maxRadius
    )
    
    return radius
}

export const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
    }).format(date)
}

export const getLoginErrorMessage = (code: String) => {
	switch (code) {
	case 'auth/invalid-email':
		return 'Invalid email address format'
	case 'auth/user-disabled':
		return 'This account has been disabled'
	case 'auth/user-not-found':
		return 'No account found with this email'
	case 'auth/wrong-password':
		return 'Incorrect password'
	case 'auth/invalid-credential':
		return 'Invalid email or password'
	case 'auth/too-many-requests':
		return 'Too many failed attempts. Please try again later'
	default:
		return 'An error occurred. Please try again'
	}
}

export const getSignupErrorMessage = (code: string) => {
    switch (code) {
      case 'auth/email-already-in-use':
        return 'An account with this email already exists'
      case 'auth/invalid-email':
        return 'Please enter a valid email address'
      case 'auth/operation-not-allowed':
        return 'Email/password accounts are not enabled. Please contact support'
      case 'auth/weak-password':
        return 'Password should be at least 8 characters long'
      default:
        return 'An error occurred during signup. Please try again'
    }
}