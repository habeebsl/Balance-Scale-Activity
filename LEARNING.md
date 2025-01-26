
# Technical Challenges I Faced

## 1. Balance Scale Mechanics

 I decided to use Matter.js to implement this. There are several reasons why I chose this:

- Easy to use compared to other libraries
- Allows addition of physics properties to the scale, such as falling animations and scale balancing motion.
- Overall, with Matter.js, I can avoid writing overly complex logic, making the code maintainable and easier to understand.

- **Challenge 1:**
    
    Matter js doesn’t offer a lot functionality for creating sprites, so it was really tough creating the          balance scale and balancing plates for the scale.
    
    **Solution**:
    
    - Matter js does allow you to create objects with specific shapes, so for the balancing plates, I combined a rectangle with two circles at the sides to form a make shift plate.
    - For the balance scale, I just modified a balance scale svg and fixed it between the two makeshift balancing plates.
    
- **Challenge 2:**
    
    In my initial implementation, the scale balancing wasn’t too good. The balancing mechanism relied on matter js gravity properties, which wasn’t bad, it just wasn’t a very good implementation. The issue was that relying on gravity, needed the ball to fall in just the right spot for the scaling to work properly, If the ball rolls a little to the right or left in the plate, the balancing mechanism would be inaccurate visually. 
    
    **Solution:**
    
    - Initially the two plates are at the same level horizontally. When the user adds an input we check if the input is less than, equal to or greater than the target value. The y-position of each plate is then moved up or down depending on the result.
    - For the inputs, the input numbers will be placed in balls which fall into the plate, if there was another ball within the plate, when the falling ball makes contact with the ball in the plate, the two balls combine into a bigger ball which contains the combination of the input numbers, and the position of the plates are then updated.
    - The number within the ball is used to calculate size of the ball, so if the input (or combined inputs) and the target are the same, then the size of the balls will be equal and the scale will be balanced.
    
- **Challenge 3:**
    
    The ball gets bigger as the input increases, so in theory the ball could get bigger and bigger, which could be an issue.
    
    **Solution**:
    
    - I defined a limit to how big the ball can get, so now the values can increase as much as it wants, but the ball will stop growing after the limit is reached.
    
- **Challenge 4**:
    
    In my initial implementation, the position updates for the plates are not fluid, so it appears as though the plates are disappearing and reappearing, which is not very visually appealing.
    
    **Solution**:
    
    - When the size of the input ball changes, the new positions of the plates are calculated based on the values. The plates are then moved a little closer to the new positions with each frame until the plates reaches their target positions, which makes the movement of the plates smoother and visually pleasing.

## 2. Authentication with Firebase

- **Challenges Faced**:
    
    Using firebase for authentication was a good choice but combining firebase with the API backend while verifying the user took me some time to figure out.
    
    **Solution**:
    
    - After the user is authenticated with firebase,  an ID token is generated which we can use to access the user details. We use this ID token to verify the user in the backend for each request, before actually processing the request. Here’s a flowchart:

![Auth Flow](https://github.com/habeebsl/Balance-Scale-Activity/blob/main/images/AuthFlow.png)

## 3. Allowing Educators to Build Activities

- **Challenge 1**:
    
    I needed to find way to identify educators from students, so that educators would be given appropriate access. 
    
    **Solution**:
    
    - I added a page to allow users select their roles after signing up or if the user role is not set. After the user has selected their role and api request will be sent to the backend to add the user role to the database.
    - Regular users won’t be able to create or edit activities nor do they have access to those pages. If a regular user tries to access the create or edit activity page, the user will be redirected back to the activities page which displays the activities published by educators.

- **Challenge 2:**
    
    Sending a request to the database each time a user tries to access a page (create, edit, dashboard) to verify the user’s role could lead to performance issues. 
    
    **Solution:**
    
    - Instead of relying on API requests to verify the user role, we add the user role to the firebase user claims when a role is selected. So that when the user tries to access a page that requires role verification, we get the role from the auth claims improving the app performance.

## 4. Authentication with Google Implementation

- **Challenge 1**:
    
    Initial implementation involved creating a signup-with-google button on the sign up page and a signin-with-google button on the login in page. When the user clicks the sign up with google button, the user is verified with firebase and will be added to the database and upon clicking the signin-with-google button the user is only verified with firebase. 
    The problem with this implementation is that, a user would expect that after clicking the signin-with-google button on the login page, they would be signed in even if they hadn’t signed up prior, but in actuality the user will get signed in but the user wouldn’t be saved to the database which could lead to issues.
    
    **Solution**:
    
    - To solve this, I went with another implementation idea. So when the user clicks the sign in with google button on either of the pages, the user is verified by firebase auth, then frontend makes an initial request to the api, to verify that the user exists in the database. If so, the user is redirected to the activities page, and if not the user is added to the database, before being redirected. Here’s a flow chart for visualization:
    
![Google Auth Flow](https://github.com/habeebsl/Balance-Scale-Activity/blob/main/images/GoogleAuthFlow.png)    

## 5. Activity Structure

- **Challenge 1**:
    
    I had to implement a way for educators to add multiple problems to an activity and be able to choose the hierarchy to which the problems will be solved.
    
    **Solution**:
    
    - For the models structure, I defined a One to many relationship in the models between an activity and the problems, allowing many problems to be associated with a specific activity.
    - Each problem has a step which is a number that details the hierarchy of the problem in the activity.

- **Challenge 2**:
    
    When an activity is gotten from the database along with its problem set, the problems are not going to be structured based on the steps. So step 3 can come before step 1 and so forth.
    
    **Solution**:
    
    - Sort the problems based on the steps in the frontend, so that upon user action like starting an activity with multiple problems, the problems are organized and presented the way the creator (educator) wants.

# What I learned?

1. How to use FastAPI, Vue, Matter.js, and Firebase Auth.
2. How to dockerize an application.
3. How to build an interactive game using matter.js.
4. How to write tests for FastAPI endpoints using Testclient and pytest.
5. How to modularize my application.

# Things I’d do differently next time

1. Style application using Tailwind: It’s faster and easier to maintain.
2. Start modularizing my application from the very beginning: To avoid restructuring project later on.
3. Use a Postgres Database: For more complex database queries and table modeling.
