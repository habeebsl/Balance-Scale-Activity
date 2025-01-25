<script setup>
import { defineEmits } from 'vue'
import RoleCard from '@/components/RoleCard.vue'
import ButtonSpinner from './ButtonSpinner.vue'
import { useRoleStore } from '@/stores/roleStore'


const emit = defineEmits(['finish'])
const roleStore = useRoleStore()

</script>

<template>
<div class="role-selection">
    <h2 class="title">Select your role</h2>
    
    <div class="role-container">
        <RoleCard role="student">
            <svg class="role-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                    <path d="M23.3 8.40007L21.82 6.40008C21.7248 6.27314 21.6009 6.17066 21.4583 6.10111C21.3157 6.03156 21.1586 5.99693 21 6.00008H11.2C11.0556 6.00007 10.9128 6.03135 10.7816 6.09177C10.6504 6.15219 10.5339 6.24031 10.44 6.35007L8.72 8.35008C8.57229 8.53401 8.49437 8.76424 8.5 9.00008V16.2901C8.50264 18.0317 9.19568 19.7013 10.4272 20.9328C11.6588 22.1644 13.3283 22.8574 15.07 22.8601H16.93C18.6717 22.8574 20.3412 22.1644 21.5728 20.9328C22.8043 19.7013 23.4974 18.0317 23.5 16.2901V9.00008C23.5 8.7837 23.4298 8.57317 23.3 8.40007Z" fill="#FFCC80"></path>
                    <path d="M29.78 28.38L25.78 23.38C25.664 23.2321 25.5087 23.1198 25.3318 23.0562C25.1549 22.9925 24.9637 22.98 24.78 23.02L16 25L7.22 23C7.03633 22.96 6.84509 22.9725 6.66822 23.0362C6.49134 23.0998 6.336 23.2121 6.22 23.36L2.22 28.36C2.10393 28.5064 2.03117 28.6823 2.00996 28.8679C1.98875 29.0534 2.01994 29.2413 2.1 29.41C2.17816 29.5839 2.30441 29.7319 2.46387 29.8364C2.62333 29.9409 2.80935 29.9977 3 30H29C29.1885 29.9995 29.373 29.9457 29.5322 29.8448C29.6915 29.744 29.819 29.6002 29.9 29.43C29.9801 29.2613 30.0112 29.0734 29.99 28.8879C29.9688 28.7023 29.8961 28.5264 29.78 28.38Z" fill="#01579B"></path>
                    <path d="M29.29 6.00003L16.29 2.00003C16.0999 1.95002 15.9001 1.95002 15.71 2.00003L2.71 6.00003C2.49742 6.06422 2.31226 6.19735 2.1837 6.37841C2.05515 6.55947 1.99052 6.77817 2 7.00003C1.9917 7.22447 2.0592 7.44518 2.19163 7.62659C2.32405 7.80799 2.5137 7.93954 2.73 8.00003L15.73 11.6C15.906 11.6534 16.094 11.6534 16.27 11.6L29.27 8.00003C29.4863 7.93954 29.6759 7.80799 29.8084 7.62659C29.9408 7.44518 30.0083 7.22447 30 7.00003C30.0095 6.77817 29.9448 6.55947 29.8163 6.37841C29.6877 6.19735 29.5026 6.06422 29.29 6.00003Z" fill="#01579B"></path>
                    <path d="M11.22 6C11.0756 5.99999 10.9328 6.03127 10.8016 6.09169C10.6704 6.15211 10.5539 6.24023 10.46 6.35L8.74 8.35C8.58509 8.53114 8.49998 8.76166 8.5 9V16.29C8.50264 18.0317 9.19569 19.7012 10.4272 20.9328C11.6588 22.1643 13.3283 22.8574 15.07 22.86H16V6H11.22Z" fill="#FFE0B2"></path> <path d="M7.22 23C7.03633 22.96 6.84509 22.9725 6.66822 23.0362C6.49134 23.0998 6.336 23.2121 6.22 23.36L2.22 28.36C2.10393 28.5064 2.03117 28.6823 2.00996 28.8679C1.98875 29.0534 2.01994 29.2413 2.1 29.41C2.17816 29.5839 2.30441 29.7319 2.46387 29.8364C2.62333 29.9409 2.80935 29.9977 3 30H16V25L7.22 23Z" fill="#0277BD"></path>
                    <path d="M15.71 2.00002L2.71 6.00002C2.49742 6.06422 2.31226 6.19734 2.1837 6.3784C2.05515 6.55947 1.99052 6.77817 2 7.00002C1.9917 7.22447 2.0592 7.44518 2.19163 7.62658C2.32405 7.80799 2.5137 7.93954 2.73 8.00002L15.73 11.6C15.8194 11.6146 15.9106 11.6146 16 11.6V2.00002C15.9039 1.98469 15.8061 1.98469 15.71 2.00002Z" fill="#0277BD"></path> 
                </g>
            </svg>
            <span class="role-text">Student</span>
        </RoleCard>

        <RoleCard role="educator">
            <svg class="role-icon" height="200px" width="200px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 297 297" xml:space="preserve" fill="#000000">
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                <g id="SVGRepo_iconCarrier">
                    <g>
                        <circle style="fill:#FFDB77;" cx="148.5" cy="62.821" r="55.321"></circle>
                        <path style="fill:#13829B;" d="M210.948,174.042H86.052c-6.93,0-12.958,4.748-14.582,11.485l-20.601,85.458 c-2.275,9.436,4.876,18.515,14.582,18.515h166.098c9.706,0,16.857-9.079,14.582-18.515l-20.601-85.458 C223.906,178.79,217.878,174.042,210.948,174.042z"></path>
                        <g>
                            <polygon style="fill:#28D2E4;" points="168.166,174.042 148.5,174.042 128.833,174.042 118.166,249.5 148.5,289.5 178.833,249.5 "></polygon>
                            <g>
                                <path style="fill:#22313F;" d="M148.5,125.642c34.64,0,62.821-28.181,62.821-62.821S183.139,0,148.5,0 S85.679,28.181,85.679,62.821S113.86,125.642,148.5,125.642z M148.5,15c26.369,0,47.821,21.452,47.821,47.821 s-21.452,47.821-47.821,47.821s-47.821-21.452-47.821-47.821S122.131,15,148.5,15z"></path>
                                <path style="fill:#22313F;" d="M253.422,269.227l-20.601-85.458c-2.445-10.143-11.439-17.227-21.874-17.227 c-13.085,0-113.2,0-124.896,0c-10.434,0-19.429,7.084-21.874,17.227l-20.601,85.458C40.166,283.375,50.88,297,65.45,297h166.099 C246.101,297,256.839,283.395,253.422,269.227z M161.652,181.542l9.318,65.915l-22.47,29.631l-22.47-29.631l9.318-65.915 L161.652,181.542L161.652,181.542z M58.159,272.743l20.601-85.459c0.815-3.381,3.813-5.742,7.292-5.742h34.146l-9.458,66.908 c-0.28,1.98,0.242,3.989,1.45,5.581L133.4,282H65.45C60.6,282,57.021,277.464,58.159,272.743z M231.549,282H163.6l21.209-27.968 c1.208-1.593,1.73-3.602,1.45-5.581l-9.458-66.908h34.146c3.478,0,6.477,2.361,7.292,5.743l20.601,85.458 C239.977,277.46,236.404,282,231.549,282z"></path>
                            </g>
                        </g>
                    </g>
                </g>
            </svg>
            <span class="role-text">Educator</span>
        </RoleCard>
    </div>

    <button 
        class="next-button"
        @click="emit('finish')"
        v-if="roleStore.selectedRole"
        :disabled="roleStore.isSaving"
    >
    Finish
    <ButtonSpinner v-if="roleStore.isSaving" />
    </button>
</div>
</template>
  

<style scoped>
.role-selection {
	max-width: 800px;
	margin: 0 auto;
	padding: 2rem;
	position: relative;
}

.title {
	font-size: 1.5rem;
	font-weight: 600;
	margin-bottom: 2rem;
	text-align: center;
	color: #333;
}

.role-container {
	display: flex;
	gap: 2rem;
	justify-content: center;
	margin-bottom: 3rem;
}

.role-icon {
	width: 48px;
	height: 48px;
	margin-bottom: 1rem;
	color: #4f46e5;
}

.role-text {
	font-size: 1.25rem;
	font-weight: 500;
	color: #333;
}

.next-button {
    display: flex;
    gap: 6px;
    position: absolute;
    right: 2rem;
    padding: 0.75rem 2rem;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.next-button:hover {
	background-color: #4338ca;
}

.next-button:disabled {
	background-color: #9ca3af;
	cursor: not-allowed;
}
</style>