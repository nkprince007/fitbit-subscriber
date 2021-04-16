# Fitbit Subscriber

## Project details

This Django project involves two components:
- Backend server that fetches and stores data from Fitbit Cloud
- Frontend Web Dashboard that uses the backend server's REST API to show
meaningful graphs in d3.js

## Adding a new patient

- Visit [https://fitbit.com](https://fitbit.com) on your browser.

- Logout of any accounts you are currently logged in with on fitbit.com.

What it looks like if you are logged in:

<img width="1440" alt="Screenshot 2021-04-17 at 2 37 32 AM" src="https://user-images.githubusercontent.com/17202890/115083999-df116e80-9f25-11eb-853c-2ac5d9041350.png">

Use this logout button shown in the picture below

<img width="1552" alt="Screenshot 2021-04-17 at 2 38 12 AM" src="https://user-images.githubusercontent.com/17202890/115084077-f6505c00-9f25-11eb-9ff7-cb954bf82d9a.png">

> Note: We request you to log out from your current account on fitbit.com so that 
> you can use a new account details for the new patient you would like to add. If you
> do not logout from any accounts already linked with our dashboard, you will simply
> be updating the existing account information and nothing else. So, we urge you 
> to logout from existing accounts beforehand.

- Now proceed to your deployed instance of fitbit-subscriber. (For our UIC live instance please visit [here](https://fitbit-subscriber.herokuapp.com).

- Use the admin credentials to log in

- Once you are logged in, click the add patient button in the top right corner to add a new patient

<img width="253" alt="Screenshot 2021-04-17 at 2 40 10 AM" src="https://user-images.githubusercontent.com/17202890/115084258-3ca5bb00-9f26-11eb-950e-9f289eda4bcc.png">

> Note: If you're now redirected back to the dashboard with no input from your side, it means that you have not logged out of fitbit.com as mentioned earlier.
> Please revisit the steps and try again.

- You should now see a screen like this which lets you login to fitbit.com

<img width="1552" alt="Screenshot 2021-04-17 at 2 42 41 AM" src="https://user-images.githubusercontent.com/17202890/115084468-973f1700-9f26-11eb-9a97-36b9426e3bb0.png">

- Enter your credentials and proceed to the next page.

- You should now see a page that looks like something below

<img width="1552" alt="Screenshot 2021-04-17 at 2 44 01 AM" src="https://user-images.githubusercontent.com/17202890/115084598-c81f4c00-9f26-11eb-9a11-6c4f614f6cbc.png">
 
- Please click on the "Allow All" button and press the "Allow" button below as indicated in the picture below.

<img width="1552" alt="Screenshot 2021-04-17 at 2 45 10 AM" src="https://user-images.githubusercontent.com/17202890/115084796-ff8df880-9f26-11eb-9d30-07933e441d58.png">

- You should now be redirected back to the clinical dashboard with your new patient added.

- Use the dropdown to select the new patient and view his history which should be available shortly.

<img width="1440" alt="Screenshot 2021-04-17 at 2 48 24 AM" src="https://user-images.githubusercontent.com/17202890/115085070-73300580-9f27-11eb-9db1-20d6ad4ad0be.png">

> Note: For the scope of this project, we are only receiving updates from the point the patient is connected with our platform. 
> Any data prior to that date from Fitbit is not stored with us.
