pipeline {
    agent any

    environment {
        ENVIRONMENT = 'development'
        DEBUG = '1'
        SECRET_KEY = 'django-insecure-+$ap&pghgqprwiio*-*m!el$9(h(i8znd^-90bj+akflpwhcz1'
        DJANGO_ALLOWED_HOSTS = 'localhost,127.0.0.1,0.0.0.0,[::1]'
        
        DATABASE_ROOT_PASSWORD = 'password@123'
        DATABASE_ENGINE = 'django.db.backends.mysql'
        DATABASE_NAME = 'djangoexperiments'
        DATABASE_USER = 'user'
        DATABASE_USER_PASSWORD = 'password@123'
        DATABASE_HOST = 'db'
        DATABASE_PORT = '3306'
        
        RABBITMQ_DEFAULT_USER = 'guest'
        RABBITMQ_DEFAULT_PASS = 'guest'
        CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
    }

    stages {
        stage('checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/develop'], [name: 'feature/*'], [name: 'fix/*']], 
                    extensions: [], 
                    userRemoteConfigs: [[url: 'https://github.com/CS5721-VonNeumann/concert-hall-booking-system.git']]
                )
            }
        }
        
        stage('build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('test') {
            steps {
                sh '/Users/adarshajit/.local/share/virtualenvs/concert-hall-booking-system-fdD0L9Df/bin/pytest -v'
            }
        }
    }
}
