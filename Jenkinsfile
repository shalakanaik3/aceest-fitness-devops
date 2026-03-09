pipeline {
    agent any
    stages {
        stage('VCS Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Environment Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Unit Testing (Pytest)') {
            steps {
                sh 'pytest test_app.py'
            }
        }
        stage('Docker Assembly') {
            steps {
                sh 'docker build -t aceest-gym:${BUILD_NUMBER} .'
            }
        }
    }
    post {
        success {
            echo 'Deployment Integrity Guaranteed.'
        }
    }
}