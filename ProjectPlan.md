# **1. Implementation Plan**

### **Step 1: Front-End Development**

1. **Implement Balance Scale Component**
    - Matter.js for physics properties and fluid balance scale animations.
    - Create a Vue component for the balance scale with adjustable settings.
    - Include animations and feedback to indicate when the scale is balanced.
2. **Design User Interface**
    - Use Vue.js to create an easy-to-use game layout.
    - Make the website mobile and desktop friendly.
3. **Add Interactivity**
    - As users engage with the balance scale, give them real-time feedback.
    

### **Step 2: Backend API Development**

1. **Set Up FastAPI Backend**
    - Set up a FastAPI project and specify the models, routes, and utility folder structures.
    - Link the backend to a mySQL database so that user information and activity settings can be stored there.
2. **Implement API Routes**
    - Connect Firebase for session management and user registration.
    - Create endpoints for fetching, updating, and deleting activities.
    - Allow educators to control the visiblity of their activities.

### **Step 3: Activity Builder**

1. Provide an easy-to-use interface for educators to build activities, define success criteria, and preview them.
2. Allow activity configurations to be saved and retrieved via FastAPI endpoints.

### **Step 4: Testing**
- Test API endpoints for correctness and security using pytest.

### **Step 5: Dockerize application**

## **2. Timeline**

| **Phase** | **Duration** | **Milestone** |
| --- | --- | --- |
| Front-End Development | 2 days | Balance Scale Component, UI ready |
| Backend API Development | 2 day | Auth & Data APIs functional |
| Activity Builder | 2 day | Builder operational, integrated with API |
| Testing & Dockerizing | 1 day | Fully tested and dockerized app |

## **3. Project Tools**

- **Frontend**: Vue.js, Matter.js, Tailwind, CSS3
- **Backend**: FastAPI, mySQL, Pytest, Firebase (for auth)
