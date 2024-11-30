# concert-hall-booking-system

A web-platform for requesting concert hall for organising a show and booking tickets for scheduled shows.


## Getting started

Step 1. Ensure you have python 3.12 and pip installed.

Step 2. Install pipenv to create virtual environment and act as a package manager
`pip install pipenv`

Step 3. Clone the Github repo and `cd concert-hall-booking-system`

Step 4. Run `pipenv install` to create a virtual environment and install dependencies in requirements.txt

Step 5. Run `pipenv shell` to activate the virtual environment 

(To avoid doing this step everytime you want to run the server, use VSCode Command Pallette to select the Python interpreter to the virtual enviroment created for this folder.)

![Python: Select interpreter](./images/interpreter.png)

Step 6. Populate .env.local file.

Step 7. Run `ENV=local python manage.py runserver`. This will pick environment variables from .env.local file.

## To run Celery for asynchronous processing,

Step 1. Install RabbitMq (for Macos, `brew install rabbitmq && brew services start rabbitmq`)

Step 2. Run `ENV=local celery -A config worker --loglevel=INFO` on another terminal.

Step 3. For monitoring, run `ENV=local celery -A config flower` on another terminal


## To run the app using Docker

Step 1. Populate .env.development file.

Step 2. Run `docker compose --env-file .env.development up --build`


## Additional useful commands

1. `django-admin startproject config .` was used to create the Django project which holds the settings.py and urls.py

2. `python manage.py startapp <app_name>` is used to create a new application in the project (also need to add it to config.settings.py)

3. ` pipenv requirements > requirements.txt` to freeze dependencies and write them to a requirements.txt file

## Run Sonarqube

1. Run this command to generate the latest report: 
  ```bash
  sonar-scanner \
  -Dsonar.projectKey=concert-hall-booking-system \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9001 \
  -Dsonar.login=sqp_c29bad0740d36d8524fac64204170f8b5cf6b0c0
  ```

## Resources

[Python Django Tutorial for Beginners - Programming with Mosh, YouTube](https://www.youtube.com/watch?v=rHux0gMZ3Eg)

[Dockerizing a Django and MySQL Application: A Step-by-Step Guide](https://medium.com/@akshatgadodia/dockerizing-a-django-and-mysql-application-a-step-by-step-guide-d4ba181d3de5)