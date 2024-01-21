# Tweeker

Tweeker is a dynamic web application inspired by X (formerly Twitter), skillfully crafted using the robust combination of Django and React.

## Table of Contents
* [General Info](#general-info)
* [Setup](#setup)

## General Info
Tweeker represents a web platform reminiscent of X, where I meticulously implemented user-friendly features. These include user registration, login/logout functionalities, tweet and retweet capabilities, as well as a variety of user profile features. The backend logic is fortified by Django, providing a solid foundation, while React ensures a dynamic and engaging frontend experience. User authentication is seamlessly executed through JWT for enhanced security. The platform is further optimized with the integration of MySQL and Redis Docker images – MySQL serves as the primary data storage solution, while Redis contributes to an efficient and responsive caching system. ~For a quick demonstration, you can visit the [DEMO](https://tweeker-fm8dmq290-amirnourani.vercel.app/), although it is recommended to run it locally until any issues are resolved.~

## Setup
During the development of this project, Ubuntu Linux was the chosen distribution. To run this project locally on your machine, follow these steps:

1. Clone the project files from GitHub:
    ```bash
    git clone https://github.com/amirNourani/Tweeker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Tweeker/
    ```

3. Ensure Docker and Docker Compose are installed. Run the following command to pull and run the specified images from the docker-compose.yaml file:
    ```bash
    docker compose up -d
    ```

4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the project on your local machine:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

Feel free to contribute to the development and submit pull requests at any time. Your feedback and collaboration are highly appreciated.

Best regards.
