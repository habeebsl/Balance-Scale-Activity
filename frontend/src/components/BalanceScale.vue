<script setup>
import Matter from 'matter-js'
import { onMounted, onUnmounted, ref, reactive, defineEmits } from 'vue'
import Tooltip from '@/components/Tooltip.vue'
import { generateNumberPuzzle } from '@/utils/numberGeneration'
import NumberSelectionGrid from '@/components/NumberSelectionGrid.vue'
import { getBallRadius, getFontSize, getRandomColor } from '@/utils/helpers'

const props = defineProps({
    target: Number,
    limit: Number,
    difficulty: String,
    timeLimit: {
        type: Number,
        default: null
    },
    hint: {
        type: String,
        default: null
    }
})

const emit = defineEmits(['equivalent', 'not-equivalent', 'time-up'])

const scaleElement = ref(null)
const currentBall = ref(null)
const inputNums = ref([])
const showHints = ref(false)
const timeRemaining = ref(props.timeLimit)
const timer = ref(null)
const numberSet = ref([])

const state = reactive({
    numOfInputs: 0,
    limitReached: false,
    isEqualtoTarget: null,
})
const engine = ref(null)
const render = ref(null)
const runner = ref(null)
const targetBall = ref(null)
const ground = ref(null)

const leftPlate = ref('')
const rightPlate = ref('')

const difficulties = {
    easy: '#22c55e',
    medium: '#f59e0b',
    hard: '#ef4444' 
}

const difficultyColor = difficulties[props.difficulty]

const tooltipState = ref([
    {
        show: false,
        text: "Pick a number to start",
        position: { x: 990, y: 160 },
        direction: 'left'
    },
    {
        show: false,
        text: "The scale will tilt to show if your sum is too high or low",
        position: { x: 450, y: 450 },
        direction: 'top'
    },
    {
        show: false,
        text: "Try to match this target number",
        position: { x: 690, y: 260 },
        direction: 'top'
    },
    {
        show: false,
        text: "Keep track of your remaining moves here",
        position: { x: 230, y: 80 },
        direction: 'bottom'
    },
    {
        show: false,
        text: `Your numbers should add up to the target when you have made ${props.limit}/${props.limit} moves.`,
        position: { x: 230, y: 80 },
        direction: 'bottom'
    },
])

const startTimer = () => {
    timer.value = setInterval(() => {
        if (timeRemaining.value > 0) {
            timeRemaining.value--
        } else {
            clearInterval(timer.value)
            if (!state.limitReached) {
                emit('time-up')
            }
        }
    }, 1000)
}

const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
}

const toggleHints = () => {
    showHints.value = !showHints.value
}

const sum = () => {
    let counter = 0
    for (let item of inputNums.value) {
        counter += item.number
    }
    return counter
}

function createPlate(x, y, width, height, edgeRadius, isStatic = true, color = 'yellow') {
    const base = Matter.Bodies.rectangle(x, y, width, height, {
        isStatic: isStatic,
        render: { fillStyle: color }
    })

    const leftEdge = Matter.Bodies.circle(x - width / 2, y, edgeRadius, {
        isStatic: isStatic,
        render: { fillStyle: color }
    })

    const rightEdge = Matter.Bodies.circle(x + width / 2, y, edgeRadius, {
        isStatic: isStatic,
        render: { fillStyle: color }
    })

    const plate = Matter.Body.create({
        parts: [base, leftEdge, rightEdge],
        isStatic: isStatic,
    })

    return plate;
}

function createInputCircle(x, y, color, number) {
    let radius = getBallRadius(number)
    let ball = Matter.Bodies.circle(x, y, radius, {
        render: { 
            fillStyle: color,
            text: number 
        },
        color: color,
        number: number,
        restitution: 0.5,
        friction: 0.1
    })

    return ball
}

const leftPlateTargetY = ref(400)
const rightPlateTargetY = ref(400)

const lerp = (start, end, factor) => {
    return start + (end - start) * factor
}

const updateScalePosition = () => {
    const currentSum = sum()
    const difference = currentSum - props.target

    const maxElevation = 60
    const elevationAmount = Math.min(Math.abs(difference) / props.target, 1) * maxElevation

    if (currentSum > props.target) {
        leftPlateTargetY.value = 400 + elevationAmount
        rightPlateTargetY.value = 400 - elevationAmount
    } else if (currentSum < props.target) {
        leftPlateTargetY.value = 400 - elevationAmount
        rightPlateTargetY.value = 400 + elevationAmount
    } else {
        leftPlateTargetY.value = 400
        rightPlateTargetY.value = 400
    }
}

const animatePlates = () => {
    const smoothing = 0.1
    
    const leftCurrentY = leftPlate.value.position.y
    const rightCurrentY = rightPlate.value.position.y

    const newLeftY = lerp(leftCurrentY, leftPlateTargetY.value, smoothing)
    const newRightY = lerp(rightCurrentY, rightPlateTargetY.value, smoothing)

    Matter.Body.setPosition(leftPlate.value, {
        x: leftPlate.value.position.x,
        y: newLeftY
    })
    Matter.Body.setPosition(rightPlate.value, {
        x: rightPlate.value.position.x,
        y: newRightY
    })
}

const removeBall = (ball) => {
    Matter.World.remove(engine.value.world, ball)
    render.value.canvas.needsUpdate = true
}

const handleSelectedNum = (item) => {
    const itemObj = {
        number: item.number,
        id: item.id
    }
    if (item.selected) {
        state.numOfInputs += 1
        inputNums.value.push(itemObj)
    } else {
        state.numOfInputs -= 1
        inputNums.value.forEach((item, index) => {
            if (item.id === itemObj.id) {
                inputNums.value.splice(index, 1)
            }
        })
    }

    if (currentBall.value) {
        removeBall(currentBall.value)
    }

    const combinedNumber = sum()

    if (!combinedNumber) {
        currentBall.value = null
        updateScalePosition()
        return;
    }

    let newColor;

    if (combinedNumber === props.target) {
        newColor = 'green'
    } else if (combinedNumber > props.target) {
        newColor = 'red'
    } else {
        newColor = 'yellow'
    }

    const newCircle = createInputCircle(
        390, 
        300, 
        newColor, 
        combinedNumber
    )
    Matter.Composite.add(engine.value.world, [newCircle])
    currentBall.value = newCircle

    updateScalePosition()

    if (state.numOfInputs === props.limit) {
        state.limitReached = true;
        if (sum() === props.target) {
            emit('equivalent')
            state.isEqualtoTarget = true;
        } else {
            console.log(sum())
            state.isEqualtoTarget = false;
            emit('not-equivalent')
        }
    } else if (sum() >= props.target) {
        console.log(sum())
        emit('not-equivalent')
    }
}

const handleTooltipNext = async (index) => {
    tooltipState.value[index].show = false
    tooltipState.value[index+1].show = true
}

const handleTooltipFinish = async (index) => {
    tooltipState.value[index].show = false
    localStorage.setItem('hasPlayedBefore', 'true')
}

const resetState = () => {
    currentBall.value = null
    inputNums.value = []
    timeRemaining.value = props.timeLimit
    clearInterval(timer.value)
    startTimer()
    state.numOfInputs = 0
    state.limitReached = false
    state.isEqualtoTarget = null
    leftPlateTargetY.value = 400
    rightPlateTargetY.value = 400

    if (engine.value) {
        Matter.Engine.clear(engine.value)
        engine.value = Matter.Engine.create()

        ground.value = Matter.Bodies.rectangle(400, 620, 2800, 60, { 
            isStatic: true,
            render: { fillStyle: 'transparent' }
        })

        rightPlate.value = createPlate(890, 400, 180, 20, 20)
        leftPlate.value = createPlate(390, 400, 180, 20, 20)
        
        targetBall.value = Matter.Bodies.circle(890, 300, getBallRadius(props.target), {
            render: { fillStyle: `#${getRandomColor()}` }
        })

        Matter.Composite.add(engine.value.world, [
            ground.value, 
            leftPlate.value, 
            rightPlate.value, 
            targetBall.value
        ])

        numberSet.value = generateNumberPuzzle({
            totalMoves: props.limit,
            target: props.target,
            difficulty: props.difficulty
        }).numbers
    }
}

defineExpose({
    resetState
})


onMounted(async () => {
    engine.value = Matter.Engine.create()

    render.value = Matter.Render.create({
        element: scaleElement.value,
        engine: engine.value,
        options: {
            width: 1300,
            height: 600,
            wireframes: false,
            background: 'transparent'
        }
    })

    rightPlate.value = createPlate(890, 400, 180, 20, 20)
    leftPlate.value = createPlate(390, 400, 180, 20, 20)
    
    ground.value = Matter.Bodies.rectangle(400, 620, 2800, 60, { 
        isStatic: true,
        render: { fillStyle: 'transparent' }
    })

    targetBall.value = Matter.Bodies.circle(890, 300, getBallRadius(props.target), {
        render: { fillStyle: `#${getRandomColor()}` }
    })

    Matter.Events.on(render.value, 'afterRender', () => {
        const ctx = render.value.context;

        let fontSize = getFontSize(props.target)
        ctx.font = `${fontSize}px "Bubblegum Sans", sans-serif`
        ctx.fillStyle = 'white'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(props.target, targetBall.value.position.x, targetBall.value.position.y)

        if (currentBall.value) {
            fontSize = getFontSize(currentBall.value.number)
            ctx.font = `${fontSize}px "Bubblegum Sans", sans-serif`
            ctx.fillText(currentBall.value.number, currentBall.value.position.x, currentBall.value.position.y)
        }
    })

    Matter.Composite.add(engine.value.world, [
        ground.value, 
        leftPlate.value, 
        rightPlate.value, 
        targetBall.value
    ])

    Matter.Render.run(render.value)
    runner.value = Matter.Runner.create()
    Matter.Runner.run(runner.value, engine.value)

    Matter.Events.on(engine.value, 'beforeUpdate', () => {
        animatePlates()
    })
    if (props.timeLimit) {
        startTimer()
    }

    numberSet.value = generateNumberPuzzle({
        totalMoves: props.limit,
        target: props.target,
        difficulty: props.difficulty
    }).numbers

    const hasPlayedBefore = localStorage.getItem('hasPlayedBefore')

    if (!hasPlayedBefore  || hasPlayedBefore === "false") {
        if (props.timeLimit) {
            tooltipState.value.push({
                show: false,
                text: "Complete the puzzle before time runs out!",
                position: { x: 120, y: 80 },
                direction: 'bottom'
            })
        }
        tooltipState.value[0].show = true
    }
})

onUnmounted(() => {
    if (engine.value) {
        Matter.Events.off(engine.value)
        Matter.Engine.clear(engine.value)
        engine.value = null
    }

    if (render.value) {
        Matter.Render.stop(render.value)
        render.value.canvas.remove()
        render.value = null
    }

    if (runner.value) {
        Matter.Runner.stop(runner.value)
        runner.value = null
    }

    if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
    }

    inputNums.value = []
    targetBall.value = null
    ground.value = null
    leftPlate.value = null
    rightPlate.value = null
})
</script>

<template>
<div class="scale">
    <div class="game-status-bar">
        <div class="status-left">
            <div class="timer-box" v-if="props.timeLimit">
                <div class="timer-content">
                    <div class="timer-icon-wrapper">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                    </div>
                    <span class="timer-text">{{ formatTime(timeRemaining) }}</span>
                </div>
            </div>

            <div class="moves-box">
                <span class="moves-count">{{ state.numOfInputs }}</span>
                <span class="moves-separator">/</span>
                <span class="moves-limit">{{ limit }}</span>
            </div>
        </div>

        <div class="status-right">
            <div class="difficulty-box" :style="`border: 2px solid ${difficultyColor};`">
                <div class="difficulty-content">
                    <div class="difficulty-wrapper" :style="`color: ${difficultyColor};`">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="difficulty-icon">
                            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
                        </svg>
                    </div>
                    <span class="difficulty-text">{{ difficulty }}</span>
                </div>
            </div>
            
            <button @click="toggleHints" class="hints-button" aria-label="Show hints" v-if="hint">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="hint-icon">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
            </button>
        </div>
    </div>

    <div v-if="showHints" class="hints-popup">
        <h3>Hints</h3>
        <p v-if="props.hint">{{ hint }}</p>
    </div>
    <div ref="scaleElement" class="svg-class">
        <div class="all-svg">
            <svg class="horizontal-handle" width="800px" height="800px" viewBox="0 0 72 72" id="first-path" xmlns="http://www.w3.org/2000/svg">
                <g id="line">
                    <path fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="2" d="M15.9996,25.1697c2.6667,0.0001,8.9544-5.3333,20.0002-5.3333S50.6666,23.8365,56,25.1697"/>
                </g>
            </svg>

            <svg class="vertical-handle" width="800px" height="800px" viewBox="0 0 72 72" id="vertical-line" xmlns="http://www.w3.org/2000/svg">
                <g id="line">
                    <line x1="35.9998" x2="35.9998" y1="22.9064" y2="51.9064" fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="2"/>
                </g>
            </svg>

            <svg class="top-ornament" width="800px" height="750px" viewBox="0 0 72 72" id="circle" xmlns="http://www.w3.org/2000/svg">
                <g id="line">
                    <circle cx="35.9998" cy="13.895" r="3" fill="yellow" stroke="none" class="update-position" />
                </g>
            </svg>

            <svg class="base-shadow" width="800px" height="800px" viewBox="0 0 72 72" id="second-path" xmlns="http://www.w3.org/2000/svg">
                <g id="line">
                    <path fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="2" d="M48,61.9064c0-3.3137-5.5964-6-12.5-6s-12.5,2.6863-12.5,6"/>
                </g>
            </svg>

            <svg class="base" width="800px" height="800px" viewBox="0 0 72 72" id="yellow-bottom-path" xmlns="http://www.w3.org/2000/svg">
                <g id="color">
                    <path fill="yellow" stroke="none" d="M48.0626,62.92c0-3.3137-5.5964-6-12.5-6s-12.5,2.6863-12.5,6H48.0626z"/>
                </g>
            </svg>
        </div>
    </div>
    <Tooltip
        v-for="(tooltip, index) in tooltipState"
        :key="index"
        :text="tooltip.text"
        :position="tooltip.position"
        :show="tooltip.show"
        :direction="tooltip.direction"
        :currentStep="index+1"
        :totalSteps="tooltipState.length"
        @next="handleTooltipNext(index)"
        @close="handleTooltipFinish(index)"
    />
    <NumberSelectionGrid
        :numbers="numberSet"
        @selected="handleSelectedNum"
    />
</div>
</template>

<style scoped>
.scale {
    display: grid;
    margin: 0;
    width: calc(100vw - 450px);
    height: 300px;
    justify-content: center;
}

.game-status-bar {
    position: absolute;
    top: 24px;
    left: 0;
    right: 250px;
    display: flex;
    justify-content: space-between;
    padding: 0 40px;
    z-index: 30;
    width: calc(100vw - 450px);
}

.status-left {
    display: flex;
    gap: 20px;
    align-items: center;
}

.timer-box {
    background-color: #ffffff;
    border: 2px solid #3b82f6;
    border-radius: 12px;
    padding: 10px 20px;
    min-width: 120px;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.timer-content {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 12px;
    width: 100%;
}

.timer-icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    color: #3b82f6;
    flex-shrink: 0;
}

.timer-text {
    font-size: 15px;
    font-weight: 600;
    color: #2c3e50;
    display: inline-block;
    text-align: left;
    flex-grow: 1;
}

.moves-box {
    background-color: #ffffff;
    border: 2px solid #3b82f6;
    border-radius: 12px;
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-width: 100px;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.moves-count {
    color: #3b82f6;
    font-weight: 700;
    font-size: 15px;
}

.moves-separator {
    color: #96a2b3;
    margin: 0 4px;
    font-size: 15px;
}

.moves-limit {
    color: #2c3e50;
    font-weight: 600;
    font-size: 15px;
}

.status-right {
    display: flex;
    gap: 20px;
    align-items: center;
}

.difficulty-box {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 10px 20px;
    min-width: 120px;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.difficulty-content {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 12px;
    width: 100%;
}

.difficulty-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.difficulty-text {
    font-size: 15px;
    font-weight: 600;
    color: #2c3e50;
    display: inline-block;
    text-align: left;
    flex-grow: 1;
}
.difficulty-box:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.hints-button {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 23px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 52px;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
    transition: all 0.2s ease;
}

.hint-icon {
    color: white;
}

.timer-box:hover,
.moves-box:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.hints-button:hover {
    background-color: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.hints-button:active {
    transform: translateY(0);
}

.hints-popup {
    position: absolute;
    top: 80px;
    right: 490px;
    background-color: white;
    border: 2px solid #3b82f6;
    border-radius: 12px;
    padding: 20px;
    z-index: 40;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    max-width: 300px;
    animation: slideIn 0.2s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hints-popup h3 {
    margin: 0 0 16px 0;
    color: #2c3e50;
    font-size: 18px;
    font-weight: 600;
}

.hints-popup p {
    margin-bottom: 12px;
    color: #4a5568;
    line-height: 1.5;
    font-size: 14px;
}

.hints-popup li:last-child {
    margin-bottom: 0;
}

.svg-class {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column-reverse;
}

.all-svg {
    display: flex;
    margin: -300px 0px 0px 0px;
    scale: 0.8;
    justify-content: center;
    align-items: center;
    z-index: -1;
}

svg { 
    position: absolute;
}

.form-container {
    max-width: 600px;
    padding: 20px;
    width: 100%;
    margin: 0px auto;
    margin-top: 250px;
    z-index: 20;
}

.number-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #c9c8c8;
    border-radius: 4px;
    font-size: 16px;
    outline: none;
    transition: border-color 0.3s ease;
}

.number-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.2);
}

.submit-button {
    width: 100%;
    padding: 12px;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.submit-button:hover {
    background-color: #2563eb;
}

.submit-button:active {
    transform: scale(0.98);
}
</style>