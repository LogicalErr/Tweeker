# Tweeker

Tweeker is a dynamic web application inspired by X (formerly Twitter), skillfully crafted using the robust combination of Django and React.

## Table of Contents
- [General Info](#general-info)
- [Setup](#setup)

## General Info
Tweeker represents a web platform reminiscent of X, where user-friendly features have been meticulously implemented, including:

- **User Registration:**
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/registration.gif" alt="Registration gif">

- **Login/Logout Functionalities:**
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/login.gif" alt="Login gif">
  <hr>
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/logout.gif" alt="Logout gif">


- **Tweet and Retweet Capabilities:**
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/tweet.gif" alt="Tweet gif">


- **User Profile Features:**
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/profile_detail.gif" alt="Profile detail gif">
  <hr>
  <img src="https://github.com/amirNourani/Tweeker/blob/master/assets/profile_detail.gif" alt="Profile update gif">


The backend logic is fortified by Django (Django REST), providing a solid foundation, while React ensures a dynamic and engaging frontend experience. User authentication is seamlessly executed through JWT for enhanced security. The platform is further optimized with the integration of MySQL and Redis Docker images – MySQL serves as the primary data storage solution, while Redis contributes to an efficient and responsive caching system.



## Setup
During the development of this project, Ubuntu Linux was the chosen distribution. If you're using macOS or one of the Linux distributions, you can run this project locally on your machine with the "make" command. Ensure [Docker](https://docs.docker.com/get-docker/), [Docker Compose](https://docs.docker.com/compose/install/), and [Node.js](https://nodejs.org/en/download) are installed in your machine. Follow these steps:

1. **Clone the project files from GitHub:**
    ```bash
    git clone https://github.com/amirNourani/Tweeker.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Tweeker/
    ```
    
3. **Then you must be able to see "docker-compose.yaml" and "Makefile" files. Run one of the following command to pull and run the specified images from the "docker-compose.yaml" file (depending on images you don't have locally in your system, this could take a while):**
    ```bash
    docker-compose up -d
    # or
    docker compose up -d
    # or
    make compose_up
    ```
    
4. **Install the required Python packages(in a virtual env) and node dependencies, and run the project on your local machine (downloading dependencies and run the project might take some minutes):**
    ```bash
    make run
    ```

visit http://localhost:3000 and create an account, edit your profile and tweet some posts.


5. **don't forget to stop and remove containers that you started docker-compose.yaml:**
    ```bash
    make compose_down
    ```

Feel free to contribute to the development and submit pull requests at any time. Your feedback and collaboration are highly appreciated.
Best regards.
